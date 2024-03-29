# Generated by Django 4.1.1 on 2022-11-07 12:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_userinfo_page_banner_userinfo_page_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccounts',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='bannerandimage',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='counter',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='cryptowalletaddress',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='faq',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='freetext',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='links',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='navigations',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
        migrations.AlterField(
            model_name='video',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])]),
        ),
    ]
