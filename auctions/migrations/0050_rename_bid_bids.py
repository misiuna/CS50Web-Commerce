# Generated by Django 5.0.1 on 2024-02-23 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0049_rename_comment_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bid',
            new_name='Bids',
        ),
    ]