# Generated by Django 4.1.13 on 2023-12-26 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.TextField(),
        ),
    ]
