"""
Simplify ApplicationOblastState statuses from 12 to 5.

Mapping:
  planned             → planned       (unchanged)
  trial_plan_created  → planned       (merged)
  trial_created       → in_trial      (merged)
  trial_in_progress   → in_trial      (merged)
  trial_completed     → in_trial      (merged)
  decision_pending    → in_trial      (merged)
  decision_made       → in_trial      (merged)
  continue            → in_trial      (merged)
  approved            → approved      (unchanged)
  rejected            → removed       (merged)
  removed             → removed       (unchanged)
  withdrawn           → withdrawn     (unchanged)
"""
from django.db import migrations, models


def forward_migrate_statuses(apps, schema_editor):
    ApplicationOblastState = apps.get_model('trials_app', 'ApplicationOblastState')

    mapping = {
        'trial_plan_created': 'planned',
        'trial_created': 'in_trial',
        'trial_in_progress': 'in_trial',
        'trial_completed': 'in_trial',
        'decision_pending': 'in_trial',
        'decision_made': 'in_trial',
        'continue': 'in_trial',
        'rejected': 'removed',
    }

    for old_status, new_status in mapping.items():
        ApplicationOblastState.objects.filter(status=old_status).update(status=new_status)


def reverse_migrate_statuses(apps, schema_editor):
    ApplicationOblastState = apps.get_model('trials_app', 'ApplicationOblastState')
    # Best-effort reverse: in_trial → trial_created (most neutral)
    ApplicationOblastState.objects.filter(status='in_trial').update(status='trial_created')


class Migration(migrations.Migration):

    dependencies = [
        ('trials_app', '0035_add_removed_withdrawn_decision_choices'),
    ]

    operations = [
        migrations.RunPython(forward_migrate_statuses, reverse_migrate_statuses),
        migrations.AlterField(
            model_name='applicationoblaststate',
            name='status',
            field=models.CharField(
                choices=[
                    ('planned', 'Запланировано'),
                    ('in_trial', 'В испытании'),
                    ('approved', 'Допуск'),
                    ('removed', 'Снят'),
                    ('withdrawn', 'Отозван'),
                ],
                default='planned',
                help_text='Статус заявки для конкретной области',
                max_length=20,
            ),
        ),
    ]
