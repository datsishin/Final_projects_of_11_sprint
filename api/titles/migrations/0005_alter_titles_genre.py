# Generated by Django 3.2.4 on 2021-06-16 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_auto_20210616_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genres', to='titles.Genre'),
        ),
    ]
