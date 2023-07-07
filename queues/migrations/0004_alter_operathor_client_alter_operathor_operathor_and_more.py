# Generated by Django 4.1.6 on 2023-07-06 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('queues', '0003_alter_operathor_client_alter_operathor_operathor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operathor',
            name='client',
            field=models.ManyToManyField(blank=True, to='queues.queue'),
        ),
        migrations.AlterField(
            model_name='operathor',
            name='operathor',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operathor',
            name='window',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='queues.window'),
            preserve_default=False,
        ),
    ]
