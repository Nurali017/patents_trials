from django.db import migrations, models


def populate_country_from_is_foreign(apps, schema_editor):
    """
    is_foreign=False → country='KZ' (отечественный = Казахстан).
    is_foreign=True → country='' (неизвестная страна, is_foreign сохраняется в БД).
    """
    Originator = apps.get_model('trials_app', 'Originator')

    Originator.objects.filter(is_foreign=False).update(country='KZ')
    # is_foreign=True: оставляем country='' (дефолт), is_foreign НЕ трогаем


def reverse_migration(apps, schema_editor):
    """Обратная миграция: очистить country."""
    Originator = apps.get_model('trials_app', 'Originator')
    Originator.objects.all().update(country='')


class Migration(migrations.Migration):

    dependencies = [
        ('trials_app', '0033_add_is_winter_to_culture'),
    ]

    operations = [
        migrations.AddField(
            model_name='originator',
            name='country',
            field=models.CharField(
                blank=True,
                default='',
                help_text='ISO 3166-1 alpha-2 код страны',
                max_length=2,
            ),
        ),
        migrations.RunPython(populate_country_from_is_foreign, reverse_migration),
    ]
