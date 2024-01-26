# Generated by Django 4.1.1 on 2022-10-13 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_coupon_orderitems_coupon'),
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='selected_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='selected_product_opt',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.productoptions'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='page_name',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]