# Generated by Django 5.0.3 on 2024-03-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_alter_declareresult_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declareresult',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
