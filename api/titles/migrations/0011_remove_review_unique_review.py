# Generated by Django 3.2.4 on 2021-06-24 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0010_alter_review_score'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_review',
        ),
    ]
