# Generated by Django 4.1.1 on 2022-10-06 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_orderitems_amount_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='ordered',
            field=models.BooleanField(default=False, verbose_name='سفارش داده شده'),
        ),
    ]