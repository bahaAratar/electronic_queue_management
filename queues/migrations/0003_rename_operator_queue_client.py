# Generated by Django 4.1.6 on 2023-06-19 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0002_window_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queue',
            old_name='operator',
            new_name='client',
        ),
    ]
