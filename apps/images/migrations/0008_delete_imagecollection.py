# Generated by Django 5.0 on 2024-03-22 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_alter_imagecollection_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImageCollection',
        ),
    ]
