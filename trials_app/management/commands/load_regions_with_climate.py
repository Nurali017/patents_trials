"""
Management command для загрузки сортоучастков с природно-климатическими зонами

Использование:
    python manage.py load_regions_with_climate
"""

from django.core.management.base import BaseCommand
from trials_app.models import Oblast, ClimateZone, Region


class Command(BaseCommand):
    help = 'Загрузить сортоучастки с природно-климатическими зонами'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка природно-климатических зон и сортоучастков...\n')
        
        # Данные из таблицы
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
                'regions': ['Железинская ГСС', 'Плодоовощной ГСУ', 'Телер']
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
                'regions': ['Шиелийский ГСУ', 'Жанакорганский ГСУ', 'Казалинский ГСУ', 'Жалагашский ГСУ', 'Хали']
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
        
        climate_zones_created = 0
        regions_created = 0
        regions_updated = 0
        
        for item in data:
            # Получить область
            try:
                oblast = Oblast.objects.get(name=item['oblast'])
            except Oblast.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Область "{item["oblast"]}" не найдена, пропуск...')
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
            
            # Создать или обновить регионы
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
                else:
                    # Обновить климатическую зону если она изменилась
                    if region.climate_zone != climate_zone:
                        region.climate_zone = climate_zone
                        region.save()
                        regions_updated += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'   🔄 Обновлён регион: {region_name} - {climate_zone.name}')
                        )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Загрузка завершена!'))
        self.stdout.write(f'   Климатических зон создано: {climate_zones_created}')
        self.stdout.write(f'   Регионов создано: {regions_created}')
        self.stdout.write(f'   Регионов обновлено: {regions_updated}')
        self.stdout.write('='*60 + '\n')


