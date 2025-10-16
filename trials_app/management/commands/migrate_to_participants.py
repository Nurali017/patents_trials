"""
Команда для миграции старых данных TrialResult на новую структуру с TrialParticipant

Использование:
    python manage.py migrate_to_participants

Что делает:
1. Для каждого Trial создает TrialParticipant из sort_records
2. Переносит существующие TrialResult на новую структуру
3. Первый сорт помечается как стандарт
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from trials_app.models import Trial, TrialParticipant, TrialResult


class Command(BaseCommand):
    help = 'Migrate old TrialResult data to new TrialParticipant structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет сделано без применения изменений',
        )
        parser.add_argument(
            '--trial-id',
            type=int,
            help='Мигрировать только конкретный Trial',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        trial_id = options.get('trial_id')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - изменения не будут применены'))
        
        # Получить испытания для миграции
        if trial_id:
            trials = Trial.objects.filter(id=trial_id, is_deleted=False)
        else:
            trials = Trial.objects.filter(is_deleted=False)
        
        total_trials = trials.count()
        self.stdout.write(f'Найдено испытаний для миграции: {total_trials}')
        
        migrated_trials = 0
        created_participants = 0
        migrated_results = 0
        skipped_trials = 0
        
        for trial in trials:
            self.stdout.write(f'\n--- Trial #{trial.id}: {trial} ---')
            
            # Проверить, есть ли уже участники
            if trial.participants.exists():
                self.stdout.write(self.style.WARNING(f'  У Trial #{trial.id} уже есть участники, пропускаем'))
                skipped_trials += 1
                continue
            
            # Получить сорта из M2M relationship
            sort_records = trial.sort_records.all()
            
            if not sort_records.exists():
                self.stdout.write(self.style.WARNING(f'  У Trial #{trial.id} нет сортов, пропускаем'))
                skipped_trials += 1
                continue
            
            self.stdout.write(f'  Найдено сортов: {sort_records.count()}')
            
            if not dry_run:
                with transaction.atomic():
                    # Создать участников
                    for idx, sort_record in enumerate(sort_records, start=1):
                        participant = TrialParticipant.objects.create(
                            trial=trial,
                            sort_record=sort_record,
                            statistical_group=0 if idx == 1 else 1,  # Первый = стандарт
                            participant_number=idx,
                        )
                        created_participants += 1
                        self.stdout.write(
                            f'    Создан участник #{idx}: {sort_record.name} '
                            f'{"(Стандарт)" if idx == 1 else ""}'
                        )
                        
                        # Мигрировать результаты для этого сорта
                        old_results = TrialResult.objects.filter(
                            trial=trial,
                            sort_record=sort_record,
                            participant__isnull=True
                        )
                        
                        for result in old_results:
                            result.participant = participant
                            result.save()
                            migrated_results += 1
                        
                        if old_results.count() > 0:
                            self.stdout.write(
                                f'      Перенесено результатов: {old_results.count()}'
                            )
                    
                    migrated_trials += 1
            else:
                self.stdout.write(f'  [DRY RUN] Будет создано участников: {sort_records.count()}')
                self.stdout.write(f'  [DRY RUN] Первый сорт будет помечен как стандарт')
        
        # Итоговая статистика
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('МИГРАЦИЯ ЗАВЕРШЕНА'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'Всего испытаний обработано: {total_trials}')
        self.stdout.write(f'Испытаний мигрировано: {migrated_trials}')
        self.stdout.write(f'Испытаний пропущено: {skipped_trials}')
        self.stdout.write(f'Участников создано: {created_participants}')
        self.stdout.write(f'Результатов перенесено: {migrated_results}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING(
                '\nЭто был DRY RUN. Для применения изменений запустите без --dry-run'
            ))




