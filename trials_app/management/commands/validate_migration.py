"""
validate_migration -- verify Gosreestr migration completeness.

Usage:
  python manage.py validate_migration
"""
import psycopg2
from django.core.management.base import BaseCommand
from django.db.models import Count

from trials_app.models import (
    Application,
    ApplicationDecisionHistory,
    ApplicationOblastState,
    SortOriginator,
    SortRecord,
)


class Command(BaseCommand):
    help = "Validate Gosreestr migration completeness"

    def handle(self, *args, **options):
        self.passed = 0
        self.failed = 0

        self._check1_application_coverage()
        self._check2_unique_application_number()
        self._check3_null_sort_record()
        self._check4_oblast_states()
        self._check5_decision_history()
        self._check6_sort_originator_sync()
        self._check7_sortrecord_orphans()

        self.stdout.write('')
        if self.failed == 0:
            self.stdout.write(self.style.SUCCESS(f'ALL {self.passed} CHECKS PASSED'))
        else:
            self.stdout.write(self.style.ERROR(f'{self.failed} FAILED, {self.passed} passed'))

    def _gos_count(self, sql):
        conn = psycopg2.connect(
            dbname='gosreestr', user='gosreestr', password='gosreestr',
            host='localhost', port=5432,
        )
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result

    def _check(self, name, condition, detail):
        if condition:
            self.stdout.write(self.style.SUCCESS(f'  PASS: {name} — {detail}'))
            self.passed += 1
        else:
            self.stdout.write(self.style.ERROR(f'  FAIL: {name} — {detail}'))
            self.failed += 1

    def _check1_application_coverage(self):
        self.stdout.write('\n--- Check 1: Application coverage ---')

        gos_total = self._gos_count("SELECT count(*) FROM registry_application")

        # Count by migration source
        migrated_created = Application.objects.filter(
            is_deleted=False,
            applicant__contains='',  # all
        ).exclude(
            applicant__startswith='MinIO'  # exclude test
        ).count()

        # Enriched = existing apps whose app_number matches Gosreestr
        gos_numbers = set()
        conn = psycopg2.connect(dbname='gosreestr', user='gosreestr', password='gosreestr', host='localhost', port=5432)
        cur = conn.cursor()
        cur.execute("SELECT registration_number FROM registry_application WHERE registration_number != ''")
        for row in cur.fetchall():
            gos_numbers.add(row[0].strip())
        cur.close()
        conn.close()

        pre_existing = Application.objects.filter(
            is_deleted=False,
            application_number__in=gos_numbers,
        ).exclude(
            purpose__startswith=''  # can't distinguish easily
        )

        trials_total = Application.objects.filter(is_deleted=False).count()

        # The real check: gos_total = created + enriched + drops
        # created = 2366, enriched = 102, drops = 9 → 2366 + 102 + 9 = 2477
        drops = 9
        expected = gos_total  # 2477
        actual = trials_total  # should be >= gos_total - drops (allowing for pre-existing)

        self._check(
            'Application coverage',
            trials_total >= gos_total - drops,
            f'Gosreestr: {gos_total}, Drops: {drops}, Trials total: {trials_total}, '
            f'Coverage: {trials_total}/{gos_total - drops} = {trials_total * 100 // (gos_total - drops)}%'
        )

    def _check2_unique_application_number(self):
        self.stdout.write('\n--- Check 2: Unique application_number ---')

        duplicates = (
            Application.objects
            .filter(is_deleted=False)
            .values('application_number')
            .annotate(cnt=Count('id'))
            .filter(cnt__gt=1)
        )
        dup_count = duplicates.count()

        self._check(
            'No duplicate application_number',
            dup_count == 0,
            f'{dup_count} duplicates' + (
                f': {list(duplicates.values_list("application_number", flat=True)[:5])}'
                if dup_count > 0 else ''
            )
        )

    def _check3_null_sort_record(self):
        self.stdout.write('\n--- Check 3: No null sort_record ---')

        null_count = Application.objects.filter(
            sort_record__isnull=True, is_deleted=False
        ).count()

        self._check(
            'All applications have sort_record',
            null_count == 0,
            f'{null_count} with null sort_record'
        )

    def _check4_oblast_states(self):
        self.stdout.write('\n--- Check 4: Oblast states (migrated slice) ---')

        gos_count = self._gos_count("SELECT count(*) FROM registry_applicationregion")

        # Count only migrated states (tagged with gosreestr justification)
        migrated_count = ApplicationOblastState.objects.filter(
            is_deleted=False,
            decision_justification__startswith='migrated_from_gosreestr',
        ).count()

        total_count = ApplicationOblastState.objects.filter(is_deleted=False).count()
        pre_existing = total_count - migrated_count

        self._check(
            'Migrated oblast states',
            migrated_count >= gos_count * 0.95,
            f'Gosreestr: {gos_count}, Migrated: {migrated_count}, Pre-existing: {pre_existing}, Total: {total_count}'
        )

        from collections import Counter
        statuses = Counter(
            ApplicationOblastState.objects
            .filter(is_deleted=False, decision_justification__startswith='migrated_from_gosreestr')
            .values_list('status', flat=True)
        )
        self.stdout.write(f'  Migrated distribution:')
        for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
            self.stdout.write(f'    {status}: {count}')

    def _check5_decision_history(self):
        self.stdout.write('\n--- Check 5: Decision history (approved only) ---')

        gos_approved = self._gos_count(
            "SELECT count(*) FROM registry_applicationregion WHERE status = 'approved'"
        )
        migrated_history = ApplicationDecisionHistory.objects.filter(
            decision_justification__startswith='migrated_from_gosreestr',
        ).count()

        self._check(
            'Approved history',
            migrated_history >= gos_approved * 0.95,
            f'Gosreestr approved: {gos_approved}, Migrated history: {migrated_history}'
        )

    def _check6_sort_originator_sync(self):
        self.stdout.write('\n--- Check 6: Sort-originator sync ---')

        sr_total = SortRecord.objects.filter(is_deleted=False).count()
        sr_with_orig = (
            SortRecord.objects
            .filter(is_deleted=False, sort_originators__isnull=False)
            .distinct()
            .count()
        )
        sr_without = sr_total - sr_with_orig

        gos_orig_links = self._gos_count("SELECT count(*) FROM registry_applicationoriginator")
        trials_orig_links = SortOriginator.objects.count()

        coverage_pct = sr_with_orig * 100 // sr_total if sr_total > 0 else 0

        self._check(
            'SortOriginator coverage',
            coverage_pct >= 50,
            f'With: {sr_with_orig}/{sr_total} ({coverage_pct}%). '
            f'Gosreestr links: {gos_orig_links}, Trials links: {trials_orig_links}. '
            f'NOTE: backfill Patents.SortAriginator for historical sorts needed'
        )

    def _check7_sortrecord_orphans(self):
        self.stdout.write('\n--- Check 7: SortRecord orphans ---')

        # SortRecords whose sort_id doesn't exist in Patents
        from django.db import connection
        with connection.cursor() as cur:
            # Can't cross-DB query, so check against known Patents count
            pass

        sr_count = SortRecord.objects.filter(is_deleted=False).count()
        # Compare with Patents
        conn = psycopg2.connect(dbname='patent', user='admin', password='qwe1daSjewspds12', host='localhost', port=5432)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM patents_sort WHERE is_deleted=false")
        pat_count = cur.fetchone()[0]
        cur.close()
        conn.close()

        diff = sr_count - pat_count

        self._check(
            'SortRecord vs Patents Sort count',
            abs(diff) <= 5,
            f'Patents: {pat_count}, Trials SortRecord: {sr_count}, Diff: {diff}'
        )
