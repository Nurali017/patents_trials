"""
fix_sync_issues — очистка и исправление данных синхронизации Patents ↔ Trials.

Подзадачи:
  1. Удалить мусорные группы культур (id=2, id=16)
  2. Заполнить group_culture для культур без группы (через Patents API)
  3. Обновить сокращённые имена групп
  4. Исправить битые sort_id в SortRecord

Использование:
  python manage.py fix_sync_issues              # все шаги
  python manage.py fix_sync_issues --dry-run    # только показать
  python manage.py fix_sync_issues --step 2     # только шаг 2
"""
from django.core.management.base import BaseCommand
from django.db.models import Q

from trials_app.models import (
    Application,
    Culture,
    GroupCulture,
    SortRecord,
    Trial,
    TrialParticipant,
)
from trials_app.patents_integration import PatentsServiceClient


GARBAGE_GROUP_IDS = [2, 16]

NAME_FIXES = {
    "Овощные": "Овощные культуры",
    "Ягодные": "Ягодные культуры",
    "Орехоплодные": "Орехоплодные культуры",
    "Цветочно-декоративные": "Цветочно-декоративные культуры",
    "Цитрусовые и субтропические": "Цитрусовые и субтропические культуры",
}


class Command(BaseCommand):
    help = "Очистка и исправление данных синхронизации Patents ↔ Trials"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только показать что будет сделано, не менять данные',
        )
        parser.add_argument(
            '--step',
            type=int,
            choices=[1, 2, 3, 4],
            help='Выполнить только конкретный шаг (1-4)',
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        step = options.get('step')

        if self.dry_run:
            self.stdout.write(self.style.WARNING('=== DRY RUN — данные не изменяются ===\n'))

        if step is None or step == 1:
            self._step1_delete_garbage_groups()
        if step is None or step == 2:
            self._step2_fill_group_culture()
        if step is None or step == 3:
            self._step3_fix_group_names()
        if step is None or step == 4:
            self._step4_fix_broken_sort_ids()

        self.stdout.write(self.style.SUCCESS('\nГотово.'))

    def _step1_delete_garbage_groups(self):
        self.stdout.write('\n--- Шаг 1: Удаление мусорных групп культур ---')

        for group_id in GARBAGE_GROUP_IDS:
            try:
                group = GroupCulture.objects.get(id=group_id)
            except GroupCulture.DoesNotExist:
                self.stdout.write(f'  Группа id={group_id} не найдена — пропуск')
                continue

            linked_count = Culture.objects.filter(group_culture=group).count()
            if linked_count > 0:
                self.stdout.write(self.style.WARNING(
                    f'  SKIP: Группа id={group_id} "{group.name}" — {linked_count} привязанных культур'
                ))
                continue

            self.stdout.write(f'  Удаление группы id={group_id} "{group.name}"')
            if not self.dry_run:
                group.hard_delete()

    def _step2_fill_group_culture(self):
        self.stdout.write('\n--- Шаг 2: Заполнение group_culture для культур без группы ---')

        cultures_without_group = Culture.objects.filter(
            group_culture__isnull=True,
            is_deleted=False,
        )
        count = cultures_without_group.count()
        self.stdout.write(f'  Найдено культур без группы: {count}')

        if count == 0:
            return

        client = PatentsServiceClient()
        fixed = 0
        errors = 0

        for culture in cultures_without_group:
            try:
                patents_culture = client.get_culture(culture.culture_id)
                if not patents_culture:
                    self.stdout.write(self.style.WARNING(
                        f'  SKIP: Культура "{culture.name}" (culture_id={culture.culture_id}) — не найдена в Patents'
                    ))
                    errors += 1
                    continue

                patents_group_id = None
                if 'group' in patents_culture and patents_culture['group']:
                    patents_group_id = patents_culture['group'].get('id') or patents_culture['group']
                elif 'group_id' in patents_culture:
                    patents_group_id = patents_culture['group_id']

                if not patents_group_id:
                    self.stdout.write(self.style.WARNING(
                        f'  SKIP: Культура "{culture.name}" — Patents не содержит group_id'
                    ))
                    errors += 1
                    continue

                local_group = GroupCulture.objects.filter(
                    group_culture_id=patents_group_id,
                    is_deleted=False,
                ).first()

                if not local_group:
                    self.stdout.write(self.style.WARNING(
                        f'  SKIP: Культура "{culture.name}" — локальная группа с group_culture_id={patents_group_id} не найдена'
                    ))
                    errors += 1
                    continue

                self.stdout.write(
                    f'  {culture.name} → группа "{local_group.name}" (group_culture_id={patents_group_id})'
                )
                if not self.dry_run:
                    culture.group_culture = local_group
                    culture.save(update_fields=['group_culture_id', 'updated_at'])
                fixed += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'  ERROR: Культура "{culture.name}" (culture_id={culture.culture_id}) — {e}'
                ))
                errors += 1

        self.stdout.write(f'  Результат: {fixed} исправлено, {errors} ошибок')

    def _step3_fix_group_names(self):
        self.stdout.write('\n--- Шаг 3: Обновление сокращённых имён групп ---')

        for old_name, new_name in NAME_FIXES.items():
            updated = GroupCulture.objects.filter(name=old_name)
            if updated.exists():
                self.stdout.write(f'  "{old_name}" → "{new_name}"')
                if not self.dry_run:
                    updated.update(name=new_name)
            else:
                self.stdout.write(f'  "{old_name}" — не найдена (уже исправлена?)')

    def _step4_fix_broken_sort_ids(self):
        self.stdout.write('\n--- Шаг 4: Исправление битых sort_id ---')

        client = PatentsServiceClient()
        sort_records = SortRecord.objects.filter(is_deleted=False)
        broken = []

        for sr in sort_records:
            try:
                exists = client.sort_exists(sr.sort_id)
                if not exists:
                    broken.append(sr)
            except Exception:
                broken.append(sr)

        self.stdout.write(f'  Найдено битых sort_id: {len(broken)}')

        for sr in broken:
            has_applications = Application.objects.filter(sort_record=sr).exists()
            has_participants = TrialParticipant.objects.filter(sort_record=sr).exists()
            has_references = has_applications or has_participants

            if has_references:
                refs = []
                if has_applications:
                    refs.append('Application')
                if has_participants:
                    refs.append('TrialParticipant')
                self.stdout.write(self.style.WARNING(
                    f'  MANUAL REVIEW: sort_id={sr.sort_id} "{sr.name}" — '
                    f'есть ссылки: {", ".join(refs)}'
                ))
            else:
                self.stdout.write(
                    f'  soft-delete: sort_id={sr.sort_id} "{sr.name}" — нет ссылок'
                )
                if not self.dry_run:
                    sr.delete()
