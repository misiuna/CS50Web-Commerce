# Generated by Django 5.0.1 on 2024-02-19 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_remove_bid_bid_remove_user_bid_remove_user_watchlist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
