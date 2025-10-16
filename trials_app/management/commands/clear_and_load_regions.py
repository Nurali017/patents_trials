"""
Management command для очистки и загрузки новых данных областей и регионов

Использование:
    python manage.py clear_and_load_regions
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from trials_app.models import Oblast, ClimateZone, Region


class Command(BaseCommand):
    help = 'Очистить и загрузить новые данные областей и регионов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Только очистить данные, не загружать новые',
        )
        parser.add_argument(
            '--load-only',
            action='store_true',
            help='Только загрузить новые данные, не очищать существующие',
        )

    def handle(self, *args, **options):
        if not options['load_only']:
            self.clear_data()
        
        if not options['clear_only']:
            self.load_new_data()

    def clear_data(self):
        """Очистить существующие данные"""
        self.stdout.write('🧹 Очистка существующих данных...')
        
        with transaction.atomic():
            # Удаляем все регионы
            regions_count = Region.objects.filter(is_deleted=False).count()
            Region.objects.filter(is_deleted=False).update(is_deleted=True)
            self.stdout.write(f'   🗑️  Удалено регионов: {regions_count}')
            
            # Удаляем все климатические зоны
            climate_zones_count = ClimateZone.objects.filter(is_deleted=False).count()
            ClimateZone.objects.filter(is_deleted=False).update(is_deleted=True)
            self.stdout.write(f'   🗑️  Удалено климатических зон: {climate_zones_count}')
            
            # Удаляем все области
            oblasts_count = Oblast.objects.filter(is_deleted=False).count()
            Oblast.objects.filter(is_deleted=False).update(is_deleted=True)
            self.stdout.write(f'   🗑️  Удалено областей: {oblasts_count}')
        
        self.stdout.write(self.style.SUCCESS('✅ Очистка завершена!\n'))

    def load_new_data(self):
        """Загрузить новые данные согласно таблице"""
        self.stdout.write('📊 Загрузка новых данных областей и регионов...\n')
        
        # Данные из предоставленной таблицы
        data = [
            {
                'oblast': 'Акмолинская',
                'climate_zone': 'Лесостепная зона',
                'climate_code': 'forest-steppe',
                'regions': ['Кокшетауский ГСУ', 'Сандыктауский ГСУ']
            },
            {
                'oblast': 'Акмолинская',
                'climate_zone': 'Степная слабо увлажнённая',
                'climate_code': 'steppe-low-humid',
                'regions': ['Шортандинский ГСУ', 'Целиноградский ГСУ']
            },
            {
                'oblast': 'Акмолинская',
                'climate_zone': 'Степная слабо засушливая',
                'climate_code': 'steppe-low-arid',
                'regions': ['Егиндыкольский ГСУ', 'Жаксынский ГСУ']
            },
            {
                'oblast': 'Северо-Казахстанская',
                'climate_zone': 'Лесостепная зона',
                'climate_code': 'forest-steppe',
                'regions': ['Арыкбалыкский ГСУ', 'Айыртауский ГСУ', 'Есильский ГСУ']
            },
            {
                'oblast': 'Северо-Казахстанская',
                'climate_zone': 'Степная слабо увлажнённая',
                'climate_code': 'steppe-low-humid',
                'regions': ['Рузаевский ГСУ', 'Шалакынский ГСУ', 'Сергеевский ГСУ', 'Кызылжарский ГСУ']
            },
            {
                'oblast': 'Костанайская',
                'climate_zone': 'Степная слабо увлажнённая',
                'climate_code': 'steppe-low-humid',
                'regions': ['Мендыкаринский ГСУ', 'Федоровский ГСУ', 'Казахстанская ГСС', 'Костанайский комплексный ГСУ', 'Костанайский']
            },
            {
                'oblast': 'Костанайская',
                'climate_zone': 'Степная слабозасушливая',
                'climate_code': 'steppe-low-arid',
                'regions': ['Житикаринский']
            },
            {
                'oblast': 'Павлодарская',
                'climate_zone': 'Степная слабо увлажнённая',
                'climate_code': 'steppe-low-humid',
                'regions': ['Железинская ГСС', 'Плодоовощной ГСУ']
            },
            {
                'oblast': 'Павлодарская',
                'climate_zone': 'Степная слабозасушливая',
                'climate_code': 'steppe-low-arid',
                'regions': ['Иртышский комплексный ГСУ', 'Павлодарский зерновой ГСУ', 'Павлодарский овощной ГСУ']
            },
            {
                'oblast': 'Карагандинская',
                'climate_zone': 'Степная слабозасушливая',
                'climate_code': 'steppe-low-arid',
                'regions': ['Карагандинский овощной ГСУ', 'Оскаровский ГСУ']
            },
            {
                'oblast': 'Карагандинская',
                'climate_zone': 'Степная умеренно засушливая',
                'climate_code': 'steppe-moderate-arid',
                'regions': ['Каркаралинский ГСУ']
            },
            {
                'oblast': 'Улытау',
                'climate_zone': 'Пустынно-степная умеренно засушливая',
                'climate_code': 'desert-steppe-moderate-arid',
                'regions': ['Жана-Аркинский ГСУ']
            },
            {
                'oblast': 'Западно-Казахстанская',
                'climate_zone': 'Степная слабо засушливая',
                'climate_code': 'steppe-low-arid',
                'regions': ['Бурлинский ГСУ', 'Зелёновский ГСУ', 'Уральский ГСУ', 'Сырымский ГСУ']
            },
            {
                'oblast': 'Актюбинская',
                'climate_zone': 'Степная слабо засушливая',
                'climate_code': 'steppe-low-arid',
                'regions': ['Алгинский ГСУ', 'Айтекебийский ГСУ']
            },
            {
                'oblast': 'Актюбинская',
                'climate_zone': 'Степная слабоувлажненная',
                'climate_code': 'steppe-low-humid',
                'regions': ['Мартукский ГСУ']
            },
            {
                'oblast': 'Восточно-Казахстанская',
                'climate_zone': 'Степная слабо засушливая',
                'climate_code': 'steppe-low-arid',
                'regions': ['Шемонаихинский ГСУ']
            },
            {
                'oblast': 'Восточно-Казахстанская',
                'climate_zone': 'Степная умеренно-засушливая',
                'climate_code': 'steppe-moderate-arid',
                'regions': ['Курчумский ГСС']
            },
            {
                'oblast': 'Восточно-Казахстанская',
                'climate_zone': 'Степная слабо увлажнённая',
                'climate_code': 'steppe-low-humid',
                'regions': ['ГСУ Алтай']
            },
            {
                'oblast': 'Абай',
                'climate_zone': 'Степная слабо увлажнённая',
                'climate_code': 'steppe-low-humid',
                'regions': ['Кокпектинский ГСУ', 'Новопокровский ГСУ']
            },
            {
                'oblast': 'Абай',
                'climate_zone': 'Степная умеренно засушливая',
                'climate_code': 'steppe-moderate-arid',
                'regions': ['Урджарский ГСУ']
            },
            {
                'oblast': 'Абай',
                'climate_zone': 'Пустынно-степная умеренно засушливая',
                'climate_code': 'desert-steppe-moderate-arid',
                'regions': ['Восточно-Казахстанский']
            },
            {
                'oblast': 'Жетісу',
                'climate_zone': 'Предгорная (Джунгарский Алатау, северо-запад Тянь-Шань)',
                'climate_code': 'foothill-dzungarian-tienshan',
                'regions': ['Плодово-ягодный ГСУ', 'Талдыкорганский п/ягодный ГСУ', 'Карабулакский ГСУ', 'Когалинский ГСУ', 'Саркандский ГСУ', 'Панфиловский ГСУ']
            },
            {
                'oblast': 'Жетісу',
                'climate_zone': 'Предгорная (Северо-Западный Тянь-Шань)',
                'climate_code': 'foothill-northwest-tienshan',
                'regions': ['Кербулакский ГСУ']
            },
            {
                'oblast': 'Алматинская',
                'climate_zone': 'Пустынная очень засушливая',
                'climate_code': 'desert-very-arid',
                'regions': ['Балхашский рисовый']
            },
            {
                'oblast': 'Алматинская',
                'climate_zone': 'Предгорная (Заилийский Алатау)',
                'climate_code': 'foothill-zailiysky-alatau',
                'regions': ['Алматинский п/ягодный ГСУ', 'Каскеленский п/ягодный ГСУ', 'Енбекшиказахский ГСУ', 'Илийский зерновой ГСУ', 'Илийский комплексный ГСУ', 'Райымбекский ГСУ']
            },
            {
                'oblast': 'Кызылординская',
                'climate_zone': 'Пустынная сухая',
                'climate_code': 'desert-dry',
                'regions': ['Шиелийский ГСУ', 'Жанакорганский ГСУ', 'Казалинский ГСУ', 'Жалагашский ГСУ']
            },
            {
                'oblast': 'Жамбылская',
                'climate_zone': 'Предгорная (Северо-Западный Тянь-Шань)',
                'climate_code': 'foothill-northwest-tienshan',
                'regions': ['Т.Рыскуловский ГСУ', 'Жуалинский ГСУ', 'Жамбылский комплексный ГСУ', 'Байзакский ГСУ']
            },
            {
                'oblast': 'Туркестанская',
                'climate_zone': 'Предгорная (Северного и Западного Тянь-Шаня)',
                'climate_code': 'foothill-north-west-tienshan',
                'regions': ['Сарыагашский ГСУ', 'Ленгерский ГСУ', 'Сайрамский комплексный ГСУ', 'Георгиевский ГСУ', 'Сарыагашский п/ягодный ГСУ', 'Сарыагашский хлопковый ГСУ', 'Туркестанский ГСУ']
            },
        ]
        
        with transaction.atomic():
            oblasts_created = 0
            climate_zones_created = 0
            regions_created = 0
            
            # Собираем уникальные области
            unique_oblasts = set()
            for item in data:
                unique_oblasts.add(item['oblast'])
            
            # Создаем области
            for oblast_name in unique_oblasts:
                oblast, created = Oblast.objects.get_or_create(
                    name=oblast_name,
                    defaults={
                        'code': self.generate_oblast_code(oblast_name)
                    }
                )
                if created:
                    oblasts_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Создана область: {oblast_name}')
                    )
            
            # Создаем климатические зоны и регионы
            for item in data:
                # Получить область
                try:
                    oblast = Oblast.objects.get(name=item['oblast'])
                except Oblast.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Область "{item["oblast"]}" не найдена!')
                    )
                    continue
                
                # Создать или получить климатическую зону
                climate_zone, created = ClimateZone.objects.get_or_create(
                    code=item['climate_code'],
                    defaults={
                        'name': item['climate_zone'],
                        'description': f'Природно-климатическая зона: {item["climate_zone"]}'
                    }
                )
                
                if created:
                    climate_zones_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Создана климатическая зона: {climate_zone.name}')
                    )
                
                # Создать регионы
                for region_name in item['regions']:
                    region, created = Region.objects.get_or_create(
                        name=region_name,
                        oblast=oblast,
                        defaults={'climate_zone': climate_zone}
                    )
                    
                    if created:
                        regions_created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'   ✅ Создан регион: {region_name} ({oblast.name}) - {climate_zone.name}')
                        )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Загрузка завершена!'))
        self.stdout.write(f'   Областей создано: {oblasts_created}')
        self.stdout.write(f'   Климатических зон создано: {climate_zones_created}')
        self.stdout.write(f'   Регионов создано: {regions_created}')
        self.stdout.write('='*60 + '\n')

    def generate_oblast_code(self, oblast_name):
        """Генерировать код области"""
        codes = {
            'Акмолинская': 'AKM',
            'Северо-Казахстанская': 'SKZ',
            'Костанайская': 'KST',
            'Павлодарская': 'PAV',
            'Карагандинская': 'KAR',
            'Улытау': 'ULY',
            'Западно-Казахстанская': 'ZKZ',
            'Актюбинская': 'AKT',
            'Восточно-Казахстанская': 'VKZ',
            'Абай': 'ABA',
            'Жетісу': 'ZET',
            'Алматинская': 'ALM',
            'Кызылординская': 'KZY',
            'Жамбылская': 'ZAM',
            'Туркестанская': 'TUR',
        }
        return codes.get(oblast_name, 'UNK')

