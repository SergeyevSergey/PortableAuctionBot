# Generated by Django 4.2.8 on 2023-12-13 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lot', '0002_customuser_userbid_lot_bidders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='bidders',
            field=models.ManyToManyField(related_name='bids', through='lot.UserBid', to='lot.customuser'),
        ),
    ]