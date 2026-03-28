from datetime import date
from io import StringIO
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from trials_app.models import (
    Application,
    ApplicationOblastState,
    Culture,
    Oblast,
    SortRecord,
)
from trials_app.management.commands.migrate_gosreestr import map_gosreestr_status


class MapGosreestrStatusTests(TestCase):
    """Test the cutover helper function."""

    def test_testing_before_2026_returns_continue(self):
        result = map_gosreestr_status('testing', date(2025, 6, 15))
        self.assertEqual(result, 'continue')

    def test_testing_2026_returns_planned(self):
        result = map_gosreestr_status('testing', date(2026, 1, 29))
        self.assertEqual(result, 'planned')

    def test_testing_none_date_returns_continue(self):
        result = map_gosreestr_status('testing', None)
        self.assertEqual(result, 'continue')

    def test_approved_unchanged(self):
        self.assertEqual(map_gosreestr_status('approved', date(2020, 1, 1)), 'approved')

    def test_removed_unchanged(self):
        self.assertEqual(map_gosreestr_status('removed', date(2023, 5, 1)), 'removed')

    def test_withdrawn_unchanged(self):
        self.assertEqual(map_gosreestr_status('withdrawn', date(2024, 1, 1)), 'withdrawn')

    def test_unknown_status_defaults_to_planned(self):
        self.assertEqual(map_gosreestr_status('garbage', date(2020, 1, 1)), 'planned')


class FixTestingCutoverCommandTests(TestCase):
    """Test the fix_testing_cutover management command."""

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username='cutover-test', password='pass',
        )
        cls.oblast_a = Oblast.objects.create(name='Almaty', code='ALM')
        cls.oblast_b = Oblast.objects.create(name='Kostanay', code='KST')
        cls.culture = Culture.objects.create(
            culture_id=9001, name='Test Wheat', code='TW',
        )
        cls.sort_record = SortRecord.objects.create(
            sort_id=9001, name='Test Sort', culture=cls.culture,
        )

    def _create_app(self, number, submission_date):
        app = Application.objects.create(
            application_number=number,
            submission_date=submission_date,
            sort_record=self.sort_record,
            applicant='Test Applicant',
            status='submitted',
            created_by=self.user,
        )
        app.target_oblasts.add(self.oblast_a, self.oblast_b)
        return app

    def _create_oblast_state(self, app, oblast, status, justification=None):
        return ApplicationOblastState.objects.create(
            application=app,
            oblast=oblast,
            status=status,
            decision_justification=justification or '',
        )

    def _mock_gosreestr_years(self, year_map):
        """Create a mock for psycopg2.connect that returns given year_map."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (gos_id, year) for gos_id, year in year_map.items()
        ]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn

    @patch('trials_app.management.commands.fix_testing_cutover.psycopg2.connect')
    def test_pre2026_testing_becomes_continue(self, mock_connect):
        """testing + receipt_date < 2026 → continue."""
        app = self._create_app('CUT-001', date(2024, 3, 1))
        aos = self._create_oblast_state(
            app, self.oblast_a, 'planned', 'migrated_from_gosreestr:100',
        )
        mock_connect.return_value = self._mock_gosreestr_years({100: 2024})

        call_command('fix_testing_cutover', stdout=StringIO())

        aos.refresh_from_db()
        self.assertEqual(aos.status, 'continue')

    @patch('trials_app.management.commands.fix_testing_cutover.psycopg2.connect')
    def test_2026_testing_stays_planned(self, mock_connect):
        """testing + receipt_date >= 2026 → planned (no change)."""
        app = self._create_app('CUT-002', date(2026, 1, 29))
        aos = self._create_oblast_state(
            app, self.oblast_a, 'planned', 'migrated_from_gosreestr:200',
        )
        mock_connect.return_value = self._mock_gosreestr_years({200: 2026})

        call_command('fix_testing_cutover', stdout=StringIO())

        aos.refresh_from_db()
        self.assertEqual(aos.status, 'planned')

    @patch('trials_app.management.commands.fix_testing_cutover.psycopg2.connect')
    def test_non_legacy_planned_untouched(self, mock_connect):
        """planned without migrated_from_gosreestr tag → no change."""
        app = self._create_app('CUT-003', date(2024, 5, 1))
        aos = self._create_oblast_state(
            app, self.oblast_a, 'planned', '',
        )
        mock_connect.return_value = self._mock_gosreestr_years({})

        call_command('fix_testing_cutover', stdout=StringIO())

        aos.refresh_from_db()
        self.assertEqual(aos.status, 'planned')

    @patch('trials_app.management.commands.fix_testing_cutover.psycopg2.connect')
    def test_approved_removed_withdrawn_untouched(self, mock_connect):
        """approved/removed/withdrawn with tag → no change."""
        app = self._create_app('CUT-004', date(2023, 1, 1))
        aos_approved = self._create_oblast_state(
            app, self.oblast_a, 'approved', 'migrated_from_gosreestr:300',
        )
        aos_removed = self._create_oblast_state(
            app, self.oblast_b, 'removed', 'migrated_from_gosreestr:300',
        )
        mock_connect.return_value = self._mock_gosreestr_years({300: 2023})

        call_command('fix_testing_cutover', stdout=StringIO())

        aos_approved.refresh_from_db()
        aos_removed.refresh_from_db()
        self.assertEqual(aos_approved.status, 'approved')
        self.assertEqual(aos_removed.status, 'removed')

    @patch('trials_app.management.commands.fix_testing_cutover.psycopg2.connect')
    def test_application_status_recalc_to_in_progress(self, mock_connect):
        """After cutover, Application.status should become in_progress."""
        app = self._create_app('CUT-005', date(2024, 1, 1))
        self._create_oblast_state(
            app, self.oblast_a, 'planned', 'migrated_from_gosreestr:400',
        )
        self._create_oblast_state(
            app, self.oblast_b, 'planned', 'migrated_from_gosreestr:400',
        )
        self.assertEqual(app.status, 'submitted')

        mock_connect.return_value = self._mock_gosreestr_years({400: 2024})

        call_command('fix_testing_cutover', stdout=StringIO())

        app.refresh_from_db()
        self.assertEqual(app.status, 'in_progress')

    @patch('trials_app.management.commands.fix_testing_cutover.psycopg2.connect')
    def test_dry_run_does_not_change_data(self, mock_connect):
        """--dry-run should not modify any records."""
        app = self._create_app('CUT-006', date(2024, 1, 1))
        aos = self._create_oblast_state(
            app, self.oblast_a, 'planned', 'migrated_from_gosreestr:500',
        )
        mock_connect.return_value = self._mock_gosreestr_years({500: 2024})

        call_command('fix_testing_cutover', '--dry-run', stdout=StringIO())

        aos.refresh_from_db()
        self.assertEqual(aos.status, 'planned')
        app.refresh_from_db()
        self.assertEqual(app.status, 'submitted')

    @patch('trials_app.management.commands.fix_testing_cutover.psycopg2.connect')
    def test_reverse_restores_planned(self, mock_connect):
        """--reverse should revert continue → planned and recalc status."""
        app = self._create_app('CUT-007', date(2024, 1, 1))
        aos = self._create_oblast_state(
            app, self.oblast_a, 'continue', 'migrated_from_gosreestr:600',
        )
        mock_connect.return_value = self._mock_gosreestr_years({600: 2024})

        call_command('fix_testing_cutover', '--reverse', stdout=StringIO())

        aos.refresh_from_db()
        self.assertEqual(aos.status, 'planned')
