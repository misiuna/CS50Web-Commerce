# Generated by Django 5.0.1 on 2024-02-13 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='image',
        ),
    ]
