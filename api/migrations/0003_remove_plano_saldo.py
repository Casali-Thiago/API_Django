# Generated by Django 5.2 on 2025-05-01 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_plano_ultima_data_resgate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plano',
            name='saldo',
        ),
    ]
