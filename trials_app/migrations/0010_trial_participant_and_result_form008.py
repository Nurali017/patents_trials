# Generated manually for Form 008 support - participants and results

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trials_app', '0009_trial_form008_fields'),
    ]

    operations = [
        # TrialParticipant: добавить код группы спелости
        migrations.AddField(
            model_name='trialparticipant',
            name='maturity_group_code',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                verbose_name='Код группы',
                help_text='Код группы спелости участника (наследуется из Trial или Application)'
            ),
        ),
        
        # TrialParticipant: УБРАТЬ choices из statistical_result
        migrations.AlterField(
            model_name='trialparticipant',
            name='statistical_result',
            field=models.IntegerField(
                blank=True,
                null=True,
                db_index=True,
                verbose_name='Группа по стат. обработке',
                help_text='''АВТОРАСЧЕТ: Код группы = int((У_сорта - У_стандарта) / НСР₀.₉₅)

Примеры:
- Стандарт: 0
- Отклонение +16.2 ц/га, НСР=5.2 → код +3
- Отклонение +7.0 ц/га, НСР=5.2 → код +1  
- Отклонение +2.0 ц/га, НСР=5.2 → код 0 (несущественно)
- Отклонение -13.2 ц/га, НСР=5.2 → код -2

Интерпретация:
- Положительный код (≥1): превышение над стандартом на N НСР
- Код 0: отклонение < НСР (статистически равен стандарту)
- Отрицательный код (≤-1): отставание от стандарта на N НСР'''
            ),
        ),
        
        # TrialResult: добавить поля для делянок (только для урожайности)
        migrations.AddField(
            model_name='trialresult',
            name='plot_1',
            field=models.FloatField(
                blank=True,
                null=True,
                help_text='Значение с делянки 1 (повторность 1)'
            ),
        ),
        migrations.AddField(
            model_name='trialresult',
            name='plot_2',
            field=models.FloatField(
                blank=True,
                null=True,
                help_text='Значение с делянки 2 (повторность 2)'
            ),
        ),
        migrations.AddField(
            model_name='trialresult',
            name='plot_3',
            field=models.FloatField(
                blank=True,
                null=True,
                help_text='Значение с делянки 3 (повторность 3)'
            ),
        ),
        migrations.AddField(
            model_name='trialresult',
            name='plot_4',
            field=models.FloatField(
                blank=True,
                null=True,
                help_text='Значение с делянки 4 (повторность 4)'
            ),
        ),
        
        # TrialResult: флаги контроля качества
        migrations.AddField(
            model_name='trialresult',
            name='is_rejected',
            field=models.BooleanField(
                default=False,
                help_text='Сорт забракован (сортовая чистота <90%)'
            ),
        ),
        migrations.AddField(
            model_name='trialresult',
            name='rejection_reason',
            field=models.TextField(
                blank=True,
                null=True,
                help_text='Причина брака (например: сортовая чистота 85%)'
            ),
        ),
        migrations.AddField(
            model_name='trialresult',
            name='is_restored',
            field=models.BooleanField(
                default=False,
                help_text='Данные восстановлены статистическим методом (при гибели делянки)'
            ),
        ),
    ]

