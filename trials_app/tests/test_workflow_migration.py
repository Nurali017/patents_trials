from datetime import date

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class WorkflowCoreMigrationTests(TransactionTestCase):
    migrate_from = ('trials_app', '0030_groupculture_regions')
    migrate_to = ('trials_app', '0031_workflow_core_refactor')

    def setUp(self):
        super().setUp()
        self.executor = MigrationExecutor(connection)
        self.executor.migrate([self.migrate_from])
        self.apps = self.executor.loader.project_state([self.migrate_from]).apps
        self.set_up_pre_migration_state()

        self.executor = MigrationExecutor(connection)
        self.executor.migrate([self.migrate_to])
        self.apps = self.executor.loader.project_state([self.migrate_to]).apps

    def set_up_pre_migration_state(self):
        user_model = self.apps.get_model('auth', 'User')
        oblast_model = self.apps.get_model('trials_app', 'Oblast')
        climate_zone_model = self.apps.get_model('trials_app', 'ClimateZone')
        region_model = self.apps.get_model('trials_app', 'Region')
        culture_model = self.apps.get_model('trials_app', 'Culture')
        sort_record_model = self.apps.get_model('trials_app', 'SortRecord')
        application_model = self.apps.get_model('trials_app', 'Application')
        trial_plan_model = self.apps.get_model('trials_app', 'TrialPlan')
        trial_model = self.apps.get_model('trials_app', 'Trial')

        self.user = user_model.objects.create_user(
            username='migration-user',
            password='migration-pass',
        )
        self.oblast = oblast_model.objects.create(name='Karaganda', code='KRG')
        climate_zone = climate_zone_model.objects.create(name='Dry steppe', code='dry-steppe')
        region = region_model.objects.create(
            name='Osakarovka GSU',
            oblast=self.oblast,
            climate_zone=climate_zone,
        )
        culture = culture_model.objects.create(
            culture_id=2001,
            name='Barley',
            code='BARLEY',
        )
        sort_record = sort_record_model.objects.create(
            sort_id=6001,
            name='Saryarka',
            culture=culture,
        )
        application = application_model.objects.create(
            application_number='APP-MIG-001',
            submission_date=date(2026, 1, 20),
            sort_record=sort_record,
            applicant='Migration Applicant',
            created_by=self.user,
        )
        application.target_oblasts.add(self.oblast)

        trial_plan = trial_plan_model.objects.create(
            year=2026,
            oblast=self.oblast,
            created_by=self.user,
        )
        trial = trial_model.objects.create(
            region=region,
            culture=culture,
            start_date=date(2026, 5, 15),
            created_by=self.user,
        )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE trials_app_application_target_oblasts
                SET status = %s,
                    trial_plan_id = %s,
                    trial_id = %s,
                    decision_date = %s,
                    decision_justification = %s,
                    decided_by_id = %s,
                    decision_year = %s
                WHERE application_id = %s AND oblast_id = %s
                """,
                [
                    'approved',
                    trial_plan.id,
                    trial.id,
                    date(2026, 10, 9),
                    'Migrated decision',
                    self.user.id,
                    2026,
                    application.id,
                    self.oblast.id,
                ],
            )

        self.application_id = application.id
        self.trial_plan_id = trial_plan.id
        self.trial_id = trial.id

    def test_backfills_application_oblast_state_from_legacy_join_table(self):
        application_oblast_state_model = self.apps.get_model('trials_app', 'ApplicationOblastState')

        state = application_oblast_state_model.objects.get(
            application_id=self.application_id,
            oblast_id=self.oblast.id,
            is_deleted=False,
        )

        self.assertEqual(state.status, 'approved')
        self.assertEqual(state.trial_plan_id, self.trial_plan_id)
        self.assertEqual(state.trial_id, self.trial_id)
        self.assertEqual(state.decision_date, date(2026, 10, 9))
        self.assertEqual(state.decision_justification, 'Migrated decision')
        self.assertEqual(state.decided_by_id, self.user.id)
        self.assertEqual(state.decision_year, 2026)
