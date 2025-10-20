# Generated migration to remove laboratory_code field completely

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trials_app', '0014_add_subgroup_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triallaboratoryresult',
            name='laboratory_code',
        ),
    ]
