# Generated by Django 5.0.1 on 2024-02-13 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_user_alter_bid_user_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='', upload_to='auctions/static/auctions/images'),
        ),
    ]