# Generated by Django 5.0.1 on 2024-02-19 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0041_remove_bid_bid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bid',
            new_name='Bids',
        ),
    ]