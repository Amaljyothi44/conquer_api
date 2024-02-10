# Generated by Django 4.1.13 on 2024-01-26 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_reminder_date_alter_reminder_nextrepetition'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subquiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('options', models.JSONField()),
                ('nextRepetition', models.IntegerField()),
                ('questionNumber', models.IntegerField()),
                ('subject', models.TextField()),
                ('link', models.URLField(blank=True, null=True)),
                ('correctOption', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]