"""
Management command для обновления адресов ГСУ

Использование:
    python manage.py update_region_addresses
    python manage.py update_region_addresses --set-empty  # Установить пустые адреса
    python manage.py update_region_addresses --show-only  # Только показать текущие адреса
"""

from django.core.management.base import BaseCommand
from trials_app.models import Region


class Command(BaseCommand):
    help = 'Обновить адреса ГСУ (сортоучастков)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--set-empty',
            action='store_true',
            help='Установить пустые адреса для всех регионов',
        )
        parser.add_argument(
            '--show-only',
            action='store_true',
            help='Только показать текущие адреса, не изменять',
        )

    def handle(self, *args, **options):
        if options['show_only']:
            self.show_addresses()
        elif options['set_empty']:
            self.set_empty_addresses()
        else:
            self.show_addresses()
            self.stdout.write('\nДля установки пустых адресов используйте: --set-empty')

    def show_addresses(self):
        """Показать текущие адреса"""
        self.stdout.write('📋 ТЕКУЩИЕ АДРЕСА ГСУ\n')
        
        regions = Region.objects.filter(is_deleted=False).order_by('oblast__name', 'name')
        
        current_oblast = None
        for region in regions:
            if region.oblast.name != current_oblast:
                current_oblast = region.oblast.name
                self.stdout.write(f'\n📍 {current_oblast}:')
            
            address = region.address if region.address else '(адрес не указан)'
            self.stdout.write(f'   {region.name}: {address}')
        
        # Статистика
        total_regions = regions.count()
        regions_with_address = regions.exclude(address__isnull=True).exclude(address='').count()
        regions_without_address = total_regions - regions_with_address
        
        self.stdout.write(f'\n📊 СТАТИСТИКА:')
        self.stdout.write(f'   Всего ГСУ: {total_regions}')
        self.stdout.write(f'   С адресом: {regions_with_address}')
        self.stdout.write(f'   Без адреса: {regions_without_address}')

    def set_empty_addresses(self):
        """Установить пустые адреса для всех регионов"""
        self.stdout.write('🧹 Установка пустых адресов для всех ГСУ...\n')
        
        regions = Region.objects.filter(is_deleted=False)
        updated_count = 0
        
        for region in regions:
            if region.address:  # Обновляем только те, у которых есть адрес
                region.address = ''
                region.save()
                updated_count += 1
                self.stdout.write(f'   ✅ Очищен адрес: {region.name}')
        
        self.stdout.write(f'\n✅ Обновлено {updated_count} регионов')
        
        if updated_count == 0:
            self.stdout.write('   ℹ️  Все адреса уже были пустыми')

