"""
Management команда для создания тестового пользователя

Использование:
    python manage.py create_test_user
    python manage.py create_test_user --username admin --password admin123
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Создать тестового пользователя для разработки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='testuser',
            help='Имя пользователя (по умолчанию: testuser)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='testpass123',
            help='Пароль (по умолчанию: testpass123)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Email (по умолчанию: test@example.com)'
        )
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Создать суперпользователя'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        is_superuser = options['superuser']

        # Проверяем существует ли пользователь
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Пользователь "{username}" уже существует')
            )
            user = User.objects.get(username=username)
        else:
            # Создаем пользователя
            if is_superuser:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Суперпользователь "{username}" создан!')
                )
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name='Test',
                    last_name='User'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Пользователь "{username}" создан!')
                )

        # Создаем или получаем токен
        token, created = Token.objects.get_or_create(user=user)
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Токен создан: {token.key}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'ℹ️  Токен уже существует: {token.key}')
            )

        # Выводим информацию для использования
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('📋 Данные для входа:'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Email:    {email}')
        self.stdout.write(f'Token:    {token.key}')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🔐 Пример использования API:'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write('# Логин (получение токена):')
        self.stdout.write(f'''curl -X POST http://localhost:8001/api/v1/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{{"username": "{username}", "password": "{password}"}}'
''')
        self.stdout.write('# Использование токена:')
        self.stdout.write(f'''curl http://localhost:8001/api/v1/applications/ \\
  -H "Authorization: Token {token.key}"
''')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))

