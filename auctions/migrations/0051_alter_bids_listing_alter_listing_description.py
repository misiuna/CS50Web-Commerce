# Generated by Django 5.0.1 on 2024-03-04 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0050_rename_bid_bids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='allListingBids', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=320),
        ),
    ]