from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from trials_app.models import (
    Application,
    ApplicationDecisionHistory,
    ApplicationOblastState,
    ClimateZone,
    Culture,
    Oblast,
    PlannedDistribution,
    Region,
    SortRecord,
    Trial,
    TrialParticipant,
    TrialPlan,
    TrialType,
)
from trials_app.services.workflow import WorkflowService


class WorkflowServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username='workflow-user',
            password='workflow-pass',
        )
        cls.oblast = Oblast.objects.create(name='Akmola', code='AKM')
        cls.climate_zone = ClimateZone.objects.create(name='Steppe', code='steppe')
        cls.region = Region.objects.create(
            name='Shortandy GSU',
            oblast=cls.oblast,
            climate_zone=cls.climate_zone,
        )
        cls.culture = Culture.objects.create(
            culture_id=1001,
            name='Spring Wheat',
            code='WHEAT',
        )
        cls.sort_record = SortRecord.objects.create(
            sort_id=5001,
            name='Astana 1',
            culture=cls.culture,
        )
        cls.trial_type = TrialType.objects.create(
            code='competitive',
            name='Competitive',
            name_full='Competitive trial',
        )

    def create_application(self, suffix):
        application = Application.objects.create(
            application_number=f'APP-2026-{suffix}',
            submission_date=date(2026, 1, 15),
            sort_record=self.sort_record,
            applicant='KazNIIZiR',
            created_by=self.user,
        )
        application.target_oblasts.add(self.oblast)
        return application

    def create_trial(self, application, *, year, status='active', trial_plan=None):
        trial = Trial.objects.create(
            region=self.region,
            trial_type=self.trial_type,
            culture=self.culture,
            start_date=date(year, 5, 1),
            year=year,
            status=status,
            trial_plan=trial_plan,
            created_by=self.user,
        )
        TrialParticipant.objects.create(
            trial=trial,
            sort_record=self.sort_record,
            application=application,
            statistical_group=1,
            participant_number=1,
        )
        return trial

    def test_distribute_application_and_trial_plan_link_oblast_state(self):
        application = self.create_application('001')
        trial_plan = TrialPlan.objects.create(
            year=2026,
            oblast=self.oblast,
            created_by=self.user,
        )

        created_distributions = WorkflowService.distribute_application(
            application,
            [
                {
                    'region': self.region,
                    'trial_type': self.trial_type,
                    'planting_season': 'spring',
                }
            ],
            self.user,
        )
        WorkflowService.distribute_trial_plan(trial_plan, created_distributions)

        application.refresh_from_db()
        oblast_state = ApplicationOblastState.objects.get(
            application=application,
            oblast=self.oblast,
            is_deleted=False,
        )

        self.assertEqual(len(created_distributions), 1)
        self.assertEqual(created_distributions[0].status, 'planned')
        self.assertEqual(oblast_state.status, 'planned')
        self.assertEqual(oblast_state.trial_plan_id, trial_plan.id)
        self.assertEqual(application.status, 'distributed')

    def test_sync_trial_progress_tracks_creation_and_completion(self):
        application = self.create_application('002')
        planned_distribution = PlannedDistribution.objects.create(
            application=application,
            region=self.region,
            trial_type=self.trial_type,
            created_by=self.user,
        )
        trial = self.create_trial(application, year=2026, status='active')

        WorkflowService.sync_trial_progress(trial)

        application.refresh_from_db()
        planned_distribution.refresh_from_db()
        oblast_state = ApplicationOblastState.objects.get(
            application=application,
            oblast=self.oblast,
            is_deleted=False,
        )

        self.assertEqual(oblast_state.status, 'in_trial')
        self.assertEqual(oblast_state.trial_id, trial.id)
        self.assertEqual(application.status, 'in_progress')
        self.assertEqual(planned_distribution.status, 'in_progress')
        self.assertEqual(planned_distribution.year_started, 2026)
        self.assertIsNone(planned_distribution.year_completed)

        trial.status = 'lab_completed'
        trial.save(update_fields=['status', 'updated_at'])
        WorkflowService.sync_trial_progress(trial)

        oblast_state.refresh_from_db()
        self.assertEqual(oblast_state.status, 'in_trial')

    def test_record_trial_decision_approved_registers_application(self):
        application = self.create_application('003')
        planned_distribution = PlannedDistribution.objects.create(
            application=application,
            region=self.region,
            trial_type=self.trial_type,
            created_by=self.user,
        )
        trial = self.create_trial(application, year=2026, status='completed')

        WorkflowService.record_trial_decision(
            trial,
            decision='approved',
            justification='Meets registry criteria',
            recommendations='Include in registry',
            decision_date=date(2026, 10, 1),
            decided_by=self.user,
        )

        trial.refresh_from_db()
        application.refresh_from_db()
        planned_distribution.refresh_from_db()
        oblast_state = ApplicationOblastState.objects.get(
            application=application,
            oblast=self.oblast,
            is_deleted=False,
        )
        history = ApplicationDecisionHistory.objects.get(
            application=application,
            oblast=self.oblast,
            year=2026,
        )

        self.assertEqual(trial.status, 'approved')
        self.assertEqual(trial.decision, 'approved')
        self.assertEqual(oblast_state.status, 'approved')
        self.assertEqual(application.status, 'registered')
        self.assertEqual(planned_distribution.status, 'approved')
        self.assertEqual(planned_distribution.year_started, 2026)
        self.assertEqual(planned_distribution.year_completed, 2026)
        self.assertEqual(history.decision, 'approved')
        self.assertEqual(history.years_tested_total, 1)

    def test_record_trial_decision_continue_keeps_application_in_progress(self):
        application = self.create_application('004')
        planned_distribution = PlannedDistribution.objects.create(
            application=application,
            region=self.region,
            trial_type=self.trial_type,
            created_by=self.user,
        )
        ApplicationDecisionHistory.objects.create(
            application=application,
            oblast=self.oblast,
            year=2025,
            decision='continue',
            decision_date=date(2025, 10, 1),
            decision_justification='First year completed',
            decided_by=self.user,
            years_tested_total=1,
        )
        trial = self.create_trial(application, year=2026, status='completed')

        WorkflowService.record_trial_decision(
            trial,
            decision='continue',
            justification='Second year required',
            decision_date=date(2026, 10, 5),
            decided_by=self.user,
        )

        application.refresh_from_db()
        planned_distribution.refresh_from_db()
        oblast_state = ApplicationOblastState.objects.get(
            application=application,
            oblast=self.oblast,
            is_deleted=False,
        )
        history = ApplicationDecisionHistory.objects.get(
            application=application,
            oblast=self.oblast,
            year=2026,
        )

        self.assertEqual(oblast_state.status, 'in_trial')
        self.assertEqual(application.status, 'in_progress')
        self.assertEqual(planned_distribution.status, 'in_progress')
        self.assertEqual(planned_distribution.year_started, 2026)
        self.assertIsNone(planned_distribution.year_completed)
        self.assertEqual(history.years_tested_total, 2)

    def test_record_trial_decision_rejected_completes_application(self):
        application = self.create_application('005')
        planned_distribution = PlannedDistribution.objects.create(
            application=application,
            region=self.region,
            trial_type=self.trial_type,
            created_by=self.user,
        )
        trial = self.create_trial(application, year=2026, status='completed')

        WorkflowService.record_trial_decision(
            trial,
            decision='rejected',
            justification='Does not meet criteria',
            decision_date=date(2026, 10, 7),
            decided_by=self.user,
        )

        application.refresh_from_db()
        planned_distribution.refresh_from_db()
        oblast_state = ApplicationOblastState.objects.get(
            application=application,
            oblast=self.oblast,
            is_deleted=False,
        )

        self.assertEqual(oblast_state.status, 'removed')
        self.assertEqual(application.status, 'completed')
        self.assertEqual(planned_distribution.status, 'rejected')
        self.assertEqual(planned_distribution.year_completed, 2026)
