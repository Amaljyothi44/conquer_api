# Generated by Django 4.1.13 on 2023-12-30 08:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_reminder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reminder',
            name='nextRepetition',
            field=models.IntegerField(default=0),
        ),
    ]