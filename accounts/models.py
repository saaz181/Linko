from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from .utils import generate_random_code
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Address(models.Model):
    user_addr = models.ForeignKey('User', on_delete=models.CASCADE , related_name='user_addr')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='نام')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    zip_code = models.PositiveBigIntegerField(unique=True, blank=True, null=True, verbose_name='کدپستی')
    phone = models.PositiveBigIntegerField(verbose_name='شماره تلفن', blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='کشور')
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name='استان')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='شهر')

    def __str__(self):
        return f'{self.name}-{self.zip_code}'

    def save(self, *args, **kwargs):
        if len(str(self.zip_code)) == 10:
            super(Address, self).save(*args, **kwargs)
        else:
            return


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True,
                                        null=True,
                                        validators=[FileExtensionValidator(
                                            allowed_extensions=['jpg', 'jpeg', 'png'])
                                        ],
                                        )
    phone_number = models.PositiveBigIntegerField(unique=True, verbose_name='شماره تلفن')
    info = models.ManyToManyField(Address, blank=True, verbose_name='آدرس(ها)')
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    gift_card = models.CharField(max_length=8, unique=True, blank=True, null=True)

    REQUIRED_FIELDS = ['username', 'phone_number', ]
    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email

    @staticmethod
    def valid_phone_number(phone_number):
        return str(phone_number).startswith('9') and len(str(phone_number)) == 10

    def save(self, *args, **kwargs):
        if self.valid_phone_number(self.phone_number):
            super(User, self).save(*args, **kwargs)
        else:
            return


@receiver(pre_save, sender=User)
def create_code_user(sender, instance, *args, **kwargs):
    code = generate_random_code(User)
    instance.code = code




