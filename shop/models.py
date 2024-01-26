import enum

from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels
from accounts.models import Address
from django.utils import timezone
import string
import random

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='shop_category/image', blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


TYPE_PRODUCT = (
    ('normal', 'NORMAL'),
    ('edit', 'EDIT'),
    ('full_edit', 'FULL_EDIT'),
)

class ProductType(enum.Enum):
    normal = 'normal'
    edit = 'edit'
    full_edit = 'full_edit'


class ProductOptions(models.Model):
    op_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='نام/تیتر')
    op_description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    op_color = models.CharField(max_length=12, blank=True, null=True, verbose_name='رنگ')
    op_design = models.CharField(max_length=50, blank=True, null=True, verbose_name='نام طرح')
    op_image = models.ImageField(upload_to='product/', validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='عکس طرح')

    typeof = models.CharField(max_length=10, choices=TYPE_PRODUCT, blank=True, null=True)

    # user is for private configuration ( upload photo and/or text )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}-{self.op_name}"
        return self.op_name

    class Meta:
        verbose_name_plural = 'Product Options'


class Product(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0), ])
    color = models.CharField(max_length=12, blank=True, null=True)
    design = models.CharField(max_length=50, blank=True, null=True, verbose_name='Design Of Card')
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), ])
    off = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), ])
    # create validator for images to detect chain file ext -> card.webp.jpg.png.webp.png (not allowed)
    image = models.ImageField(upload_to='product/', validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'])])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    other_branches = models.ManyToManyField(ProductOptions, blank=True, related_name='product_other_branch')
    typeof = models.CharField(max_length=10, choices=TYPE_PRODUCT, blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ('can_upload_photo', 'Can Upload Photo'),
            ('can_upload_text', 'Can Upload Text')
        ]


SCAN_OPTIONS = (
    ('nfc', 'NFC'),
    ('nfc+qrcode', 'NFC & QRcode')
)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)
    selected_product = models.ForeignKey(ProductOptions, related_name='product_selected_product',
                                         on_delete=models.SET_NULL, blank=True, null=True)
    scan_option = models.CharField(max_length=11, choices=SCAN_OPTIONS, default='nfc')
    page_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0), ])
    # photo & text
    card_design = models.ImageField(upload_to='card_photo_desing/', validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='عکس طرح', blank=True, null=True)
    card_text = models.TextField(blank=True, null=True)

    ordered = models.BooleanField(default=False)

    def total_product_price(self) -> float:
        return self.quantity * self.product.price

    def total_product_off_price(self) -> float:
        return self.quantity * self.product.off

    def profit(self) -> float:
        if self.product.off:
            return self.total_product_price() - self.total_product_off_price()

    def final_payment(self) -> float:
        if self.product.off:
            return self.total_product_off_price()
        return self.total_product_price()

    @staticmethod
    def calculate_total_price_items(user, currency_type="IRT") -> int:
        total_amount_to_pay = 0
        user_cart = Cart.objects.filter(user=user, ordered=False)
        for item in user_cart:
            total_amount_to_pay += item.final_payment()

        if currency_type == 'IRT':
            return total_amount_to_pay
        return total_amount_to_pay * 10

    @staticmethod
    def calculate_price_with_tax(user, currency_type='IRT'):
        # tax value can be change
        tax = 0.09 * Cart.calculate_total_price_items(user)
        total_price_with_tax = Cart.calculate_total_price_items(user) + tax

        if currency_type == 'IRT':
            return total_price_with_tax
        return total_price_with_tax * 10

    @staticmethod
    def validate_product_edit(product, selected_product):
        if product.typeof == ProductType.edit.value or product.typeof == ProductType.full_edit.value:
            if selected_product.typeof == ProductType.edit.value or \
                    selected_product.typeof == ProductType.full_edit.value:
                return True
        return False

    def __str__(self):
        return f"{self.user.username}-{self.selected_product.op_design}"


class OrderItems(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Cart, blank=True, verbose_name='سفارشات')
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name='مبلغ پرداخت شده')
    is_delivered = models.BooleanField(default=False, verbose_name='ارسال سفارش')
    is_received = models.BooleanField(default=False, verbose_name='سفارش تحویل گرفته شده')
    date_received = jmodels.jDateTimeField(blank=True, null=True, verbose_name='تاریخ ارسال سفارش توسط شرکت')
    date_delivered = jmodels.jDateTimeField(blank=True, null=True, verbose_name='تاریخ تحویل سفارش توسط مشتری')
    date_ordered = models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان سفارش مشتری')

    # The field "ordered" is used for when we create an order object
    # then he/she redirect to payment page if his payment was successful
    # the obj will create with ordered=True in OrderItems else
    # the object will create but with ordered=False
    ordered = models.BooleanField(default=False, verbose_name='سفارش داده شده')

    # This field is for determine which order the cards pages created for them or not
    created_card = models.BooleanField(default=False)

    coupon = models.ForeignKey("Coupon", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.email

    # this :use_coupon can be deleted
    def use_coupon(self):
        if self.coupon:
            coupon_obj = Coupon.objects.filter(user=self.user,
                                               active=True,
                                               usage_times__gte=1,
                                               usage_times__lte=MAX_USAGE_TIMES,
                                               coupon_code=self.coupon.coupon_code,
                                               date_coupon_ends__gte=timezone.now()
                                               )
            if coupon_obj.exists():
                coupon_obj = coupon_obj.first()

                total_amount = Cart.objects.filter(user=self.user, ordered=True)
                if total_amount.exists():

                    # can replace "total_amount" with tax -> Cart.calculate_price_with_tax(self.user)
                    total_amount = Cart.calculate_total_price_items(self.user)
                    discount_amount = total_amount * (coupon_obj.off_percent / 100)

                    total_amount -= discount_amount
                    self.amount = total_amount

                    if self.coupon.usage_times - 1 >= 0:
                        self.coupon.usage_times -= 1
                        self.coupon.save()
                    else:
                        self.coupon.delete()

                    self.save()

    class Meta:
        verbose_name_plural = 'Order Items'


MAX_USAGE_TIMES = 3


def generate_coupon_code():
    length = 15
    characters = string.digits + string.ascii_letters

    found_unique_coupon = False
    coupon = ""
    while not found_unique_coupon:
        coupon = ''.join(random.choices(characters, k=length))
        if Coupon.objects.filter(coupon_code=coupon).count() == 0:
            found_unique_coupon = True

    return coupon


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=15, blank=True, null=True, default=generate_coupon_code, unique=True)
    off_percent = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0), ])
    active = models.BooleanField(default=False)
    date_coupon_created = models.DateTimeField(auto_now_add=True)
    date_coupon_ends = models.DateTimeField(blank=True, null=True)
    usage_times = models.IntegerField(default=0,
                                      validators=[MinValueValidator(0), MaxValueValidator(MAX_USAGE_TIMES), ])

    def __str__(self):
        return f"{self.coupon_code}"

    @staticmethod
    def calculate_total_price_with_coupon(user, amount, coupon_code):
        if coupon_code:
            coupon_obj = Coupon.objects.filter(user=user,
                                               active=True,
                                               usage_times__gte=1,
                                               usage_times__lte=MAX_USAGE_TIMES,
                                               coupon_code=coupon_code,
                                               date_coupon_ends__gte=timezone.now()
                                               )

            if coupon_obj.exists():
                coupon_obj = coupon_obj.first()

                discount_amount = amount * (coupon_obj.off_percent / 100)
                amount -= discount_amount

                if coupon_obj.usage_times - 1 >= 0:
                    coupon_obj.usage_times -= 1
                    coupon_obj.save()
                else:
                    coupon_obj.delete()

                return amount

        return False
