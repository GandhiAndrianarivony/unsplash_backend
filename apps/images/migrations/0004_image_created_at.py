# Generated by Django 5.0 on 2024-02-28 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_remove_image_folder_name_image_base_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
