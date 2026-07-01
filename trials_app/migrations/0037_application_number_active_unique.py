from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials_app', '0036_simplify_oblast_statuses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_number',
            field=models.CharField(
                help_text='Уникальный номер заявки (например, APP-2025-001)',
                max_length=100,
            ),
        ),
        migrations.AddConstraint(
            model_name='application',
            constraint=models.UniqueConstraint(
                condition=models.Q(is_deleted=False),
                fields=('application_number',),
                name='uniq_active_application_number',
            ),
        ),
    ]
