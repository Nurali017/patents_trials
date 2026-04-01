"""
migrate_gosreestr -- migrate application/status data from Gosreestr DB into Trials.

Steps:
  1. Sync SortRecord + Originators from Patents (using sync_from_patents)
  2. Create Application records (with fallback for empty/duplicate reg numbers)
  3. Create ApplicationOblastState (status mapping)
  4. Create ApplicationDecisionHistory (approved only — removed is NOT rejected)

Usage:
  python manage.py migrate_gosreestr --oblast-csv mapping_oblast.csv --sort-csv review_sort.csv --originator-csv review_originator.csv
  python manage.py migrate_gosreestr --dry-run --step 1 ...
"""
import csv
from collections import defaultdict
from datetime import date

import psycopg2
from django.core.management.base import BaseCommand
from django.utils import timezone

from trials_app.models import (
    Application,
    ApplicationDecisionHistory,
    ApplicationOblastState,
    Culture,
    Oblast,
    SortRecord,
)


GOSREESTR_STATUS_MAP = {
    'approved': 'approved',
    'removed': 'removed',
    'withdrawn': 'withdrawn',
}


def map_gosreestr_status(gos_status, receipt_date):
    """Cutover rule for 2026 Trials rollout.

    Gosreestr 'testing' means trials are ongoing:
    - receipt_date >= 2026 → 'planned' (new apps, will be managed in Trials)
    - receipt_date < 2026  → 'continue' (legacy ongoing trials)
    """
    if gos_status == 'testing':
        if receipt_date and receipt_date.year >= 2026:
            return 'planned'
        return 'continue'
    return GOSREESTR_STATUS_MAP.get(gos_status, 'planned')


class Command(BaseCommand):
    help = "Migrate Gosreestr data into Trials"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--step', type=int, choices=[1, 2, 3, 4])
        parser.add_argument('--oblast-csv', required=True)
        parser.add_argument('--sort-csv', required=True)
        parser.add_argument('--originator-csv', required=True)
        parser.add_argument('--created-by-id', type=int, default=3, help='User ID for created_by (default: 3=alim)')

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        step = options.get('step')
        self.oblast_csv = options['oblast_csv']
        self.sort_csv = options['sort_csv']
        self.originator_csv = options['originator_csv']
        self.created_by_id = options.get('created_by_id', 3)

        if self.dry_run:
            self.stdout.write(self.style.WARNING('=== DRY RUN ===\n'))

        if step is None or step == 1:
            self._step1_sync_sort_records()
        if step is None or step == 2:
            self._step2_create_applications()
        if step is None or step == 3:
            self._step3_create_oblast_states()
        if step is None or step == 4:
            self._step4_create_decision_history()

        self.stdout.write(self.style.SUCCESS('\nDone.'))

    def _read_csv(self, path):
        with open(path, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def _gos_query(self, sql, params=None):
        conn = psycopg2.connect(
            dbname='gosreestr', user='gosreestr', password='gosreestr',
            host='localhost', port=5432,
        )
        cur = conn.cursor()
        cur.execute(sql, params or [])
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def _build_oblast_lookup(self):
        """gos_region_id -> Trials Oblast"""
        lookup = {}
        for row in self._read_csv(self.oblast_csv):
            gos_id = row.get('gos_region_id', '').strip()
            trials_id = row.get('trials_oblast_id', '').strip()
            if gos_id and trials_id:
                oblast = Oblast.objects.filter(id=trials_id, is_deleted=False).first()
                if oblast:
                    lookup[gos_id] = oblast
        return lookup

    def _build_sort_lookup(self):
        """gos_app_id -> patents_sort_id (from mapping_sort + review_sort)"""
        raw = {}

        # First: load mapping_sort.csv (all 2,477 — includes already matched)
        mapping_path = self.sort_csv.replace('review_sort', 'mapping_sort')
        try:
            for row in self._read_csv(mapping_path):
                gos_id = row.get('gos_app_id', '').strip()
                patents_id = row.get('patents_sort_id', '').strip()
                match_type = row.get('match_type', '')
                if gos_id and patents_id and match_type != 'NO_MATCH':
                    raw[gos_id] = {
                        'decision': 'match',
                        'patents_sort_id': patents_id,
                        'dedup_to': '',
                    }
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('  mapping_sort.csv not found'))

        # Then: override with review_sort.csv (expert decisions for 1,334)
        for row in self._read_csv(self.sort_csv):
            gos_id = row.get('gos_app_id', '').strip()
            decision = row.get('expert_decision', '')
            patents_id = row.get('expert_patents_sort_id', '').strip()
            dedup_to = row.get('dedup_to_gos_app_id', '').strip()

            if decision == 'match' and patents_id:
                raw[gos_id] = {'decision': 'match', 'patents_sort_id': patents_id, 'dedup_to': ''}
            elif decision == 'create':
                # For create: sort was created in Patents by import_gosreestr_data
                # Find its patents_sort_id by name + culture
                raw[gos_id] = {'decision': 'create', 'patents_sort_id': '', 'dedup_to': '',
                               'variety': row.get('gos_variety', ''),
                               'culture': row.get('gos_culture', '')}
            elif decision == 'dedup':
                raw[gos_id] = {'decision': 'dedup', 'patents_sort_id': '', 'dedup_to': dedup_to}
            elif decision == 'skip':
                raw[gos_id] = {'decision': 'skip', 'patents_sort_id': '', 'dedup_to': ''}

        return raw

    def _resolve_sort_record(self, gos_app_id, sort_lookup):
        """Resolve gos_app_id to Trials SortRecord, following dedup chain."""
        info = sort_lookup.get(str(gos_app_id), {})
        if info.get('decision') == 'dedup' and info.get('dedup_to'):
            info = sort_lookup.get(info['dedup_to'], {})
        if info.get('decision') == 'skip':
            return None

        patents_sort_id = info.get('patents_sort_id')
        if patents_sort_id:
            return SortRecord.objects.filter(sort_id=int(patents_sort_id), is_deleted=False).first()

        # For create: find by variety name + culture in SortRecord
        variety = info.get('variety', '')
        if variety and info.get('decision') == 'create':
            culture_name = info.get('culture', '').strip()
            qs = SortRecord.objects.filter(name=variety, is_deleted=False)
            if culture_name:
                qs_with_culture = qs.filter(culture__name__iexact=culture_name)
                return qs_with_culture.first() or qs.first()
            return qs.first()

        return None

    # ------------------------------------------------------------------
    # Step 1: Sync ALL missing SortRecords from Patents (+ originators)
    # ------------------------------------------------------------------
    def _step1_sync_sort_records(self):
        self.stdout.write('\n--- Step 1: Sync SortRecord from Patents ---')

        from trials_app.patents_integration import PatentsServiceClient
        client = PatentsServiceClient()

        all_patents = client.get_all_sorts() or []
        existing_sort_ids = set(
            SortRecord.objects.filter(is_deleted=False).values_list('sort_id', flat=True)
        )

        missing = [s for s in all_patents if s.get('id') and s['id'] not in existing_sort_ids]
        self.stdout.write(f'  Patents sorts total: {len(all_patents)}')
        self.stdout.write(f'  Already in Trials: {len(existing_sort_ids)}')
        self.stdout.write(f'  Missing (to sync): {len(missing)}')

        created = 0
        errors = 0

        for sort_data in missing:
            try:
                pid = sort_data['id']
                culture = None
                culture_info = sort_data.get('culture')
                if culture_info:
                    culture_id = culture_info.get('id') if isinstance(culture_info, dict) else culture_info
                    culture = Culture.objects.filter(culture_id=culture_id, is_deleted=False).first()

                if not self.dry_run:
                    sr = SortRecord.objects.create(
                        sort_id=pid,
                        name=sort_data.get('name', ''),
                        public_code=sort_data.get('code', '') or '',
                        culture=culture,
                    )
                    # sync_from_patents will also sync originators
                    sr.sync_from_patents(sync_originators=True)
                created += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ERROR sort {sort_data.get("id")}: {e}'))
                errors += 1

        self.stdout.write(f'  Result: {created} synced, {errors} errors')

    # ------------------------------------------------------------------
    # Step 2: Create Applications
    # ------------------------------------------------------------------
    def _step2_create_applications(self):
        self.stdout.write('\n--- Step 2: Create Applications ---')

        sort_lookup = self._build_sort_lookup()

        # Load Gosreestr applications
        gos_apps = self._gos_query("""
            SELECT a.id, a.registration_number, a.receipt_date, a.variety, a.note
            FROM registry_application a
            ORDER BY a.id
        """)
        self.stdout.write(f'  Gosreestr applications: {len(gos_apps)}')

        # Load duplicate drops
        dup_drops = set()
        try:
            dup_path = self.oblast_csv.replace('mapping_oblast', 'review_duplicates')
            for r in self._read_csv(dup_path):
                if r.get('row_decision') == 'drop':
                    dup_drops.add(str(r.get('gos_app_id', '')))
        except FileNotFoundError:
            pass
        self.stdout.write(f'  Duplicate drops: {len(dup_drops)}')

        created = 0
        enriched = 0
        skipped = 0
        errors = 0

        for gos_id, reg_number, receipt_date, variety, note in gos_apps:
            gos_id_str = str(gos_id)

            # Skip dropped duplicates
            if gos_id_str in dup_drops:
                skipped += 1
                continue

            # Resolve sort_record via mapping + review CSV
            sort_record = self._resolve_sort_record(gos_id_str, sort_lookup)

            if not sort_record:
                skipped += 1
                continue

            # Application number with fallback
            app_number = (reg_number or '').strip()
            if not app_number:
                app_number = f'LEGACY-{gos_id}'

            # Check if already exists
            existing = Application.objects.filter(
                application_number=app_number, is_deleted=False
            ).first()
            if existing:
                enriched += 1
                continue

            # Handle remaining duplicates
            if Application.objects.filter(application_number=app_number).exists():
                app_number = f'LEGACY-{gos_id}'

            # Gosreestr has no applicant data — originators are on the sort level
            # via SortRecord → SortOriginator → Originator

            if not self.dry_run:
                try:
                    from django.contrib.auth.models import User
                    Application.objects.create(
                        application_number=app_number,
                        submission_date=receipt_date or date(2020, 1, 1),
                        sort_record=sort_record,
                        applicant='',
                        status='submitted',
                        purpose=note or '',
                        created_by_id=self.created_by_id,
                    )
                    created += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ERROR gos.{gos_id}: {e}'))
                    errors += 1
            else:
                created += 1

        self.stdout.write(f'  Result: {created} created, {enriched} enriched, {skipped} skipped, {errors} errors')

    # ------------------------------------------------------------------
    # Step 3: Create ApplicationOblastState
    # ------------------------------------------------------------------
    def _step3_create_oblast_states(self):
        self.stdout.write('\n--- Step 3: Create ApplicationOblastState ---')

        oblast_lookup = self._build_oblast_lookup()
        self.stdout.write(f'  Oblast mappings: {len(oblast_lookup)}')

        gos_regions = self._gos_query("""
            SELECT ar.application_id, ar.region_id, ar.status, ar.year
            FROM registry_applicationregion ar
            ORDER BY ar.application_id
        """)
        self.stdout.write(f'  Gosreestr oblast states: {len(gos_regions)}')

        # Build gos_app_id -> (app_number, receipt_date) lookup
        gos_app_numbers = {}
        gos_receipt_dates = {}
        for gos_id, reg_num, receipt_date, _, _ in self._gos_query(
            "SELECT id, registration_number, receipt_date, variety, note FROM registry_application"
        ):
            num = (reg_num or '').strip() or f'LEGACY-{gos_id}'
            gos_app_numbers[str(gos_id)] = num
            gos_receipt_dates[str(gos_id)] = receipt_date

        app_lookup = {}
        for app in Application.objects.filter(is_deleted=False):
            app_lookup[app.application_number] = app

        created = 0
        errors = 0

        for gos_app_id, gos_region_id, gos_status, year in gos_regions:
            app_number = gos_app_numbers.get(str(gos_app_id))
            application = app_lookup.get(app_number) if app_number else None
            oblast = oblast_lookup.get(str(gos_region_id))
            receipt_date = gos_receipt_dates.get(str(gos_app_id))
            trials_status = map_gosreestr_status(gos_status, receipt_date)

            if not application or not oblast:
                errors += 1
                continue

            if not self.dry_run:
                try:
                    ApplicationOblastState.objects.get_or_create(
                        application=application,
                        oblast=oblast,
                        defaults={
                            'status': trials_status,
                            'decision_year': year,
                            'decision_justification': f'migrated_from_gosreestr:{gos_app_id}',
                        },
                    )
                    # Also add to target_oblasts M2M (so frontend can see them)
                    application.target_oblasts.add(oblast)
                    created += 1
                except Exception as e:
                    errors += 1
            else:
                created += 1

        self.stdout.write(f'  Result: {created} created, {errors} errors')

    # ------------------------------------------------------------------
    # Step 4: Create ApplicationDecisionHistory
    # ------------------------------------------------------------------
    def _step4_create_decision_history(self):
        self.stdout.write('\n--- Step 4: Create ApplicationDecisionHistory ---')
        self.stdout.write('  Statuses: approved → approved, removed → removed, withdrawn → withdrawn')

        GOSREESTR_DECISION_MAP = {
            'approved': 'approved',
            'removed': 'removed',
            'withdrawn': 'withdrawn',
        }

        oblast_lookup = self._build_oblast_lookup()

        gos_decisions = self._gos_query("""
            SELECT ar.application_id, ar.region_id, ar.status, ar.year
            FROM registry_applicationregion ar
            WHERE ar.status IN ('approved', 'removed', 'withdrawn')
        """)
        self.stdout.write(f'  Gosreestr decisions (approved+removed+withdrawn): {len(gos_decisions)}')

        gos_app_numbers = {}
        for gos_id, reg_num, _, _, _ in self._gos_query(
            "SELECT id, registration_number, receipt_date, variety, note FROM registry_application"
        ):
            num = (reg_num or '').strip() or f'LEGACY-{gos_id}'
            gos_app_numbers[str(gos_id)] = num

        app_lookup = {}
        for app in Application.objects.filter(is_deleted=False):
            app_lookup[app.application_number] = app

        created = 0
        errors = 0

        for gos_app_id, gos_region_id, gos_status, year in gos_decisions:
            app_number = gos_app_numbers.get(str(gos_app_id))
            application = app_lookup.get(app_number) if app_number else None
            oblast = oblast_lookup.get(str(gos_region_id))
            decision = GOSREESTR_DECISION_MAP.get(gos_status)

            if not application or not oblast or not decision:
                errors += 1
                continue

            effective_year = year or 2020

            if not self.dry_run:
                try:
                    ApplicationDecisionHistory.objects.get_or_create(
                        application=application,
                        oblast=oblast,
                        year=effective_year,
                        defaults={
                            'decision': decision,
                            'decision_date': date(effective_year, 1, 1),
                            'decision_justification': f'migrated_from_gosreestr:{gos_app_id}',
                            'years_tested_total': 1,
                        },
                    )
                    created += 1
                except Exception as e:
                    errors += 1
            else:
                created += 1

        self.stdout.write(f'  Result: {created} created, {errors} errors')
