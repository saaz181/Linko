# Generated by Django 4.1.1 on 2022-11-10 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_remove_productoptions_scan_option_cart_scan_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='page_name',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
