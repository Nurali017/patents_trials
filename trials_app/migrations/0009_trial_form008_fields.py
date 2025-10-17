# Generated manually for Form 008 support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials_app', '0008_indicator_validation_rules'),
    ]

    operations = [
        # Добавить поля для формы 008 в Trial
        migrations.AddField(
            model_name='trial',
            name='maturity_group_code',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                db_index=True,
                verbose_name='Код группы',
                help_text='Код группы спелости для формы 008 (1, 2, 3...). Все сорта в одной группе спелости имеют одинаковый код.'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='maturity_group_name',
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name='Группа спелости',
                help_text='Название группы спелости (Среднеранняя группа, D-03 и т.д.)'
            ),
        ),
        
        # Статистика опыта (РУЧНОЙ ВВОД готовых результатов дисперсионного анализа)
        migrations.AddField(
            model_name='trial',
            name='lsd_095',
            field=models.FloatField(
                blank=True,
                null=True,
                verbose_name='НСР₀.₉₅',
                help_text='Наименьшая существенная разность (ц/га). ОБЯЗАТЕЛЬНО для автоматического расчета кодов групп! Вводится вручную на основе дисперсионного анализа.'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='error_mean',
            field=models.FloatField(
                blank=True,
                null=True,
                verbose_name='E (ошибка средней)',
                help_text='Ошибка средней (ц/га)'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='accuracy_percent',
            field=models.FloatField(
                blank=True,
                null=True,
                verbose_name='P% (точность опыта)',
                help_text='Точность опыта (%). Должно быть ≤4% при 4-кратной повторности'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='replication_count',
            field=models.IntegerField(
                default=4,
                help_text='Количество повторений (делянок)'
            ),
        ),
        
        # Дополнительные поля для формы 008
        migrations.AddField(
            model_name='trial',
            name='trial_code',
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                help_text='Код ГСУ для отчетности'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='culture_code',
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                help_text='Код культуры для отчетности'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='predecessor_code',
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                help_text='Код предшественника для отчетности'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='responsible_person_title',
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                help_text='Должность руководителя ГСУ'
            ),
        ),
        migrations.AddField(
            model_name='trial',
            name='approval_date',
            field=models.DateField(
                blank=True,
                null=True,
                help_text='Дата утверждения формы 008'
            ),
        ),
    ]

