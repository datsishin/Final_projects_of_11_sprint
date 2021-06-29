# Generated by Django 3.2.4 on 2021-06-11 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='titles',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(related_name='genres', to='titles.Genre'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='titles.category'),
            preserve_default=False,
        ),
    ]
