# Generated by Django 5.0.1 on 2024-02-20 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0046_bids'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='watchlist',
            new_name='userWatchlist',
        ),
    ]