# Generated by Django 5.0.1 on 2024-01-24 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='subject',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
