# Generated by Django 4.1.13 on 2023-12-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countdb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('remcount', models.IntegerField(default=0)),
                ('newscount', models.IntegerField(default=0)),
                ('totalnews', models.IntegerField(default=0)),
                ('dateAnswer', models.DateField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('body', models.JSONField()),
                ('date', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
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
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('answer', models.TextField()),
                ('nextRepetition', models.IntegerField()),
                ('questionNumber', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('subject', models.TextField()),
            ],
        ),
    ]
