# Generated by Django 5.0.1 on 2024-02-19 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_alter_bid_bid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bid',
        ),
    ]
