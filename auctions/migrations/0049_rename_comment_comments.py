# Generated by Django 5.0.1 on 2024-02-22 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0048_alter_user_userwatchlist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Comments',
        ),
    ]
