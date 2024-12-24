# Generated by Django 5.1.4 on 2024-12-24 08:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_rename_images_images_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
        migrations.RenameIndex(
            model_name='image',
            new_name='images_imag_created_d57897_idx',
            old_name='images_imag_created_b41a97_idx',
        ),
    ]
