"""
Management command для загрузки типов испытаний

Использование:
    python manage.py load_trial_types
"""

from django.core.management.base import BaseCommand
from trials_app.models import TrialType


class Command(BaseCommand):
    help = 'Загрузить типы испытаний (КСИ, ООС, ДЮС-ТЕСТ и др.)'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка типов испытаний...\n')
        
        # Данные типов испытаний
        trial_types = [
            {
                'code': 'competitive',
                'name': 'КСИ',
                'name_full': 'Конкурсное сортоиспытание (КСИ)',
                'category': 'mandatory',
                'description': 'Основное испытание для оценки хозяйственной ценности сорта',
                'requires_area': True,
                'requires_standard': True,
                'default_area_ha': 0.025,
                'sort_order': 1
            },
            {
                'code': 'oos',
                'name': 'ООС',
                'name_full': 'Опыты на хозяйственную полезность (ООС)',
                'category': 'mandatory',
                'description': 'Испытание для подтверждения хозяйственной полезности',
                'requires_area': True,
                'requires_standard': True,
                'default_area_ha': 0.028,
                'sort_order': 2
            },
            {
                'code': 'dus',
                'name': 'ДЮС-ТЕСТ',
                'name_full': 'Испытание на отличимость, однородность и стабильность (ДЮС-ТЕСТ)',
                'category': 'mandatory',
                'description': 'Оценка отличимости от других сортов, однородности и стабильности признаков',
                'requires_area': True,
                'requires_standard': False,
                'default_area_ha': 0.028,
                'sort_order': 3
            },
            {
                'code': 'production',
                'name': 'Производственное',
                'name_full': 'Производственное испытание',
                'category': 'additional',
                'description': 'Испытание в производственных условиях',
                'requires_area': True,
                'requires_standard': True,
                'default_area_ha': 1.0,
                'sort_order': 4
            },
            {
                'code': 'variety_technology',
                'name': 'Сортовая технология',
                'name_full': 'Опыты по изучению сортовой технологии',
                'category': 'additional',
                'description': 'Изучение оптимальных приемов возделывания сорта',
                'requires_area': True,
                'requires_standard': False,
                'default_area_ha': 0.6,
                'sort_order': 5
            },
            {
                'code': 'efu',
                'name': 'ЭФУ',
                'name_full': 'Опыты ЭФУ и демонстрационных посевов',
                'category': 'demonstration',
                'description': 'Экологическое испытание и демонстрация сортов',
                'requires_area': True,
                'requires_standard': False,
                'default_area_ha': 0.01,
                'sort_order': 6
            },
            {
                'code': 'methodological',
                'name': 'Методические опыты',
                'name_full': 'Методические опыты, опыты по договору, коллекция',
                'category': 'special',
                'description': 'Специальные исследовательские опыты',
                'requires_area': True,
                'requires_standard': False,
                'default_area_ha': 0.15,
                'sort_order': 7
            },
            {
                'code': 'ground_control',
                'name': 'Грунтконтроль',
                'name_full': 'Опыты по грунтконтролю',
                'category': 'special',
                'description': 'Контроль качества семян и почвы',
                'requires_area': False,
                'requires_standard': False,
                'sort_order': 8
            },
            {
                'code': 'ksi_applicant',
                'name': 'КСИ на территории заявителя',
                'name_full': 'Опыты КСИ на территории заявителя',
                'category': 'additional',
                'description': 'Конкурсное испытание на территории заявителя',
                'requires_area': True,
                'requires_standard': True,
                'default_area_ha': 0.025,
                'sort_order': 9
            },
            {
                'code': 'seed_reproduction',
                'name': 'Размножение семян',
                'name_full': 'План размножения семян для целей сортоиспытания',
                'category': 'reproduction',
                'description': 'Размножение семян для дальнейших испытаний',
                'requires_area': True,
                'requires_standard': False,
                'sort_order': 10
            },
            {
                'code': 'planting_material',
                'name': 'Выращивание посадочного материала',
                'name_full': 'План выращивания посадочного материала плодовоягодных культур и винограда',
                'category': 'reproduction',
                'description': 'Выращивание саженцев для испытаний',
                'requires_area': True,
                'requires_standard': False,
                'sort_order': 11
            },
            {
                'code': 'technology_economic',
                'name': 'Технолого-экономические',
                'name_full': 'Технолого-экономические опыты',
                'category': 'special',
                'description': 'Оценка экономической эффективности сорта',
                'requires_area': True,
                'requires_standard': False,
                'sort_order': 12
            },
            {
                'code': 'seed_reproduction_production',
                'name': 'Размножение для производства',
                'name_full': 'План размножения семян для внедрения в производство',
                'category': 'reproduction',
                'description': 'Размножение семян для внедрения',
                'requires_area': True,
                'requires_standard': False,
                'sort_order': 13
            },
        ]
        
        created = 0
        updated = 0
        
        for trial_type_data in trial_types:
            trial_type, created_flag = TrialType.objects.update_or_create(
                code=trial_type_data['code'],
                defaults={
                    'name': trial_type_data['name'],
                    'name_full': trial_type_data['name_full'],
                    'category': trial_type_data['category'],
                    'description': trial_type_data['description'],
                    'requires_area': trial_type_data['requires_area'],
                    'requires_standard': trial_type_data['requires_standard'],
                    'default_area_ha': trial_type_data.get('default_area_ha'),
                    'sort_order': trial_type_data['sort_order'],
                }
            )
            
            if created_flag:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Создан: {trial_type.name_full}')
                )
            else:
                updated += 1
                self.stdout.write(
                    self.style.SUCCESS(f'🔄 Обновлен: {trial_type.name_full}')
                )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Загрузка завершена!'))
        self.stdout.write(f'   Типов создано: {created}')
        self.stdout.write(f'   Типов обновлено: {updated}')
        self.stdout.write('='*60 + '\n')

