from django.db import transaction
from django.utils import timezone

from ..models import Application, ApplicationDecisionHistory, PlannedDistribution


class WorkflowService:
    """
    Централизованная orchestration-логика workflow trials.
    """

    TRIAL_COMPLETED_STATUSES = {
        'completed_008',
        'lab_sample_sent',
        'lab_completed',
        'completed',
    }
    FINAL_DECISIONS = {'approved', 'continue', 'rejected'}

    @classmethod
    def ensure_application_states(cls, application):
        application.ensure_oblast_states()

    @classmethod
    def set_oblast_state(
        cls,
        application,
        oblast,
        status,
        *,
        trial_plan=None,
        trial=None,
        decision_date=None,
        decision_justification=None,
        decided_by=None,
        decision_year=None,
        save_application_status=True,
    ):
        return application.update_oblast_status(
            oblast=oblast,
            new_status=status,
            trial_plan=trial_plan,
            trial=trial,
            decision_date=decision_date,
            decision_justification=decision_justification,
            decided_by=decided_by,
            decision_year=decision_year,
            save_application_status=save_application_status,
        )

    @classmethod
    @transaction.atomic
    def distribute_application(cls, application, validated_distributions, user):
        PlannedDistribution.objects.filter(application=application).delete()

        created_distributions = []
        touched_oblasts = set()

        for validated in validated_distributions:
            planned_dist = PlannedDistribution.objects.create(
                application=application,
                region=validated['region'],
                trial_type=validated['trial_type'],
                planting_season=validated['planting_season'],
                created_by=user,
            )
            created_distributions.append(planned_dist)
            touched_oblasts.add(validated['region'].oblast)

        for oblast in touched_oblasts:
            cls.set_oblast_state(
                application,
                oblast,
                'planned',
                save_application_status=False,
            )

        application._update_overall_status()
        return created_distributions

    @classmethod
    @transaction.atomic
    def distribute_trial_plan(cls, trial_plan, created_distributions):
        touched_application_ids = set()

        for planned_dist in created_distributions:
            cls.set_oblast_state(
                planned_dist.application,
                planned_dist.region.oblast,
                'planned',
                trial_plan=trial_plan,
                save_application_status=False,
            )
            touched_application_ids.add(planned_dist.application_id)

        for application in Application.objects.filter(id__in=touched_application_ids):
            application._update_overall_status()

    @classmethod
    def _planned_distribution_status_for_trial(cls, trial):
        if trial.decision in {'approved', 'rejected'}:
            return trial.decision
        return 'in_progress'

    @classmethod
    def _oblast_state_for_trial(cls, trial):
        if trial.decision == 'approved':
            return 'approved'
        if trial.decision == 'rejected':
            return 'removed'
        return 'in_trial'

    @classmethod
    @transaction.atomic
    def sync_trial_progress(cls, trial):
        application_ids = set(
            trial.participants.filter(
                application__isnull=False,
                is_deleted=False,
            ).values_list('application_id', flat=True)
        )
        state_status = cls._oblast_state_for_trial(trial)
        trial_year = trial.year or (trial.start_date.year if trial.start_date else None)

        for application in Application.objects.filter(id__in=application_ids):
            cls.set_oblast_state(
                application,
                trial.region.oblast,
                state_status,
                trial_plan=trial.trial_plan,
                trial=trial,
                decision_date=trial.decision_date,
                decision_justification=trial.decision_justification,
                decided_by=trial.decided_by,
                decision_year=trial_year,
                save_application_status=False,
            )
            application._update_overall_status()

            planned_dist = PlannedDistribution.objects.filter(
                application=application,
                region=trial.region,
            ).first()
            if not planned_dist:
                continue

            planned_dist.status = cls._planned_distribution_status_for_trial(trial)
            if planned_dist.year_started is None and trial_year is not None:
                planned_dist.year_started = trial_year
            if trial.decision in {'approved', 'rejected'} and trial_year is not None:
                planned_dist.year_completed = trial_year
            planned_dist.save(update_fields=['status', 'year_started', 'year_completed', 'updated_at'])

    @classmethod
    @transaction.atomic
    def record_trial_decision(
        cls,
        trial,
        *,
        decision,
        justification='',
        recommendations='',
        decision_date=None,
        decided_by=None,
    ):
        decision_date = decision_date or timezone.now().date()
        decision_year = trial.year or (trial.start_date.year if trial.start_date else decision_date.year)

        trial.decision = decision
        trial.decision_justification = justification
        trial.decision_recommendations = recommendations
        trial.decision_date = decision_date
        trial.decided_by = decided_by
        trial.status = decision
        trial.save(
            update_fields=[
                'decision',
                'decision_justification',
                'decision_recommendations',
                'decision_date',
                'decided_by',
                'status',
                'updated_at',
            ]
        )

        touched_applications = {}
        participants = trial.participants.filter(
            application__isnull=False,
            is_deleted=False,
        ).select_related('application')
        for participant in participants:
            application = participant.application
            if application is None or application.id in touched_applications:
                continue

            years_tested = ApplicationDecisionHistory.objects.filter(
                application=application,
                oblast=trial.region.oblast,
                year__lte=decision_year,
            ).exclude(year=decision_year).count() + 1

            ApplicationDecisionHistory.objects.update_or_create(
                application=application,
                oblast=trial.region.oblast,
                year=decision_year,
                defaults={
                    'decision': decision,
                    'decision_date': decision_date,
                    'decision_justification': justification,
                    'decided_by': decided_by,
                    'average_yield': None,
                    'years_tested_total': years_tested,
                },
            )
            touched_applications[application.id] = application

        cls.sync_trial_progress(trial)
        return trial
