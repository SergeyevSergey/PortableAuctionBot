# Generated by Django 4.2.8 on 2023-12-16 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lot', '0006_alter_lot_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbid',
            name='bid_cost',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Bid cost'),
        ),
    ]
