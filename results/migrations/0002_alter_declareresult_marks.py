# Generated by Django 5.0.3 on 2024-03-08 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declareresult',
            name='marks',
            field=models.JSONField(blank=True),
        ),
    ]
