# Generated by Django 4.1.1 on 2022-10-03 12:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('shop', '0002_alter_product_other_branches'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productoptions',
            options={'verbose_name_plural': 'Product Options'},
        ),
        migrations.AddField(
            model_name='productoptions',
            name='_type',
            field=models.CharField(blank=True, choices=[('edit', 'EDIT'), ('full_edit', 'FULL_EDIT')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='productoptions',
            name='op_color',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='رنگ'),
        ),
        migrations.AlterField(
            model_name='productoptions',
            name='op_description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='productoptions',
            name='op_design',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='طرح'),
        ),
        migrations.AlterField(
            model_name='productoptions',
            name='op_image',
            field=models.ImageField(upload_to='product/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='عکس'),
        ),
        migrations.AlterField(
            model_name='productoptions',
            name='op_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='نام/تیتر'),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_on_debt', models.BooleanField(default=False, verbose_name='مشتری بدهی دارد')),
                ('amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='مبلغ قابل پرداخت')),
                ('amount_paid', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='مبلغ پرداخت شده')),
                ('is_delivered', models.BooleanField(default=False, verbose_name='ارسال سفارش')),
                ('is_received', models.BooleanField(default=False, verbose_name='سفارش تحویل گرفته شده')),
                ('date_received', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ ارسال سفارش توسط شرکت')),
                ('date_delivered', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ تحویل سفارش توسط مشتری')),
                ('date_ordered', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان سفارش مشتری')),
                ('ordered', models.BooleanField(default=False, verbose_name='سفارش داده شده')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.address')),
                ('order', models.ManyToManyField(blank=True, to='shop.cart', verbose_name='سفارشات')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Order Items',
            },
        ),
    ]