# Generated by Django 2.2.1 on 2019-06-27 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_migrate_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
    ]
