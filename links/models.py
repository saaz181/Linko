from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, FileExtensionValidator
from datetime import datetime
from shop.models import Product, ProductOptions

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


"""
we need to store some front-end property
in order to save user change in ui elements & order
then all of our other model inherit from this front data
"""

text_dir = (
    ('r', 'RIGHT'),
    ('l', 'LEFT'),
    ('c', 'CENTER'),
)


class AbstractData(models.Model):
    # front data
    color = models.CharField(max_length=12, blank=True, null=True, default="#000000")
    background_color = models.CharField(max_length=12, blank=True, null=True, default='#ffffff')
    font = models.CharField(max_length=50, blank=True, null=True)
    font_size = models.IntegerField(default=14)
    icon = models.ImageField(upload_to='icons', validators=[
        FileExtensionValidator(allowed_extensions=['ico', 'jpg', 'jpeg', 'png', 'webp'])], blank=True, null=True)
    border_radius = models.CharField(max_length=5, blank=True, null=True)
    border_color = models.CharField(max_length=12, blank=True, null=True, default='#000000')
    animation = models.CharField(max_length=12, blank=True, null=True)
    text_direction = models.CharField(max_length=1, choices=text_dir, blank=True, null=True, default='c')
    placeholder_text = models.CharField(max_length=100, blank=True, null=True)
    seperator_shape = models.CharField(max_length=10, blank=True, null=True, verbose_name='seperator shape')
    seperator_full_size = models.BooleanField(default=False)
    margin_bottom_top = models.IntegerField(default=1)

    # ordering of objects display in front-end app
    ordering = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0), ])

    # other data
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=30, blank=True, null=True, default="")
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class SocialMedia(AbstractData):
    base_link_to_append = models.URLField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Social Media'


TYPES = (
    ('sms', 'SMS',),
    ('email', 'EMAIL',),
    ('phone_number', 'PHONE_NUMBER',),
    ('tel', 'TELEPHONE',),
    ('fax', 'FAX',),
)


class ContactInfo(AbstractData):
    _type = models.CharField(max_length=12, choices=TYPES, blank=True)
    text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Contact Info'


# TODO: optimize images with compression
class BannerAndImage(AbstractData):
    images = models.ImageField(upload_to='banners/image/', blank=True, null=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    url_text = models.CharField(max_length=50, blank=True, null=True)


class Video(AbstractData):
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Links(AbstractData):
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Links'


NAVIGATION_APPS = (
    ('google_map', 'GOOGLE'),
    ('neshan', 'NESHAN'),
    ('balad', 'BALAD'),
    ('waze', 'WAZE'),
    ('others', 'OTHER')
)


class Navigations(AbstractData):
    application = models.CharField(max_length=10, choices=NAVIGATION_APPS, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    detail_address = models.TextField(blank=True, null=True, verbose_name='آدرس دقیق')

    class Meta:
        verbose_name_plural = 'Navigations'


class FAQ(AbstractData):
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'FAQs'


class FreeText(AbstractData):
    body = models.TextField(blank=True, null=True)


# TODO: get and add all bank logos and names
class BankAccounts(AbstractData):
    credit_card = models.CharField(max_length=20, blank=True, null=True)
    sheba_code = models.CharField(max_length=28, blank=True, null=True)
    account_number = models.CharField(max_length=30, blank=True, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Bank Accounts'


class CryptoWalletAddress(AbstractData):
    wallet_address = models.CharField(max_length=50, blank=True, null=True)
    coin_type = models.CharField(max_length=30, blank=True, null=True)
    icon_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.coin_type


class Counter(AbstractData):
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    def update_time(self):
        now_time = datetime.now()
        self.start = now_time
        self.save()

    def calculate_duration(self):
        diff = self.end - self.start
        seconds = diff.seconds

        day = 24 * 60 * 60
        hour = 60 * 60

        days = seconds // day
        hours = (seconds % day) // hour
        minutes = ((seconds % days) % hour) // 60
        _seconds = ((seconds % days) % hour) % 60

        return {
            'day': days,
            'hour': hours,
            'minute': minutes,
            'seconds': _seconds
        }

    def is_valid_counter(self):
        return self.end > self.start and self.end > datetime.now()


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    # name here represent the name of the page
    page_name = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # TODO: should provide default image(s) for this fields
    page_photo = models.ImageField(upload_to='pages/logos', blank=True, null=True,
                                   validators=[FileExtensionValidator(
                                       allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])

    page_banner = models.ImageField(upload_to='pages/banners', blank=True, null=True,
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])

    page_bio = models.TextField(blank=True, null=True)

    services = models.ManyToManyField(SocialMedia, blank=True)
    contact_info = models.ManyToManyField(ContactInfo, blank=True)
    images = models.ManyToManyField(BannerAndImage, blank=True)
    video_links = models.ManyToManyField(Video, blank=True)
    links = models.ManyToManyField(Links, blank=True)
    navigation_info = models.ManyToManyField(Navigations, blank=True)
    faq = models.ManyToManyField(FAQ, blank=True)
    free_texts = models.ManyToManyField(FreeText, blank=True)
    counter = models.ManyToManyField(Counter, blank=True)
    bank_account = models.ManyToManyField(BankAccounts, blank=True)
    crypto_wallet_address = models.ManyToManyField(CryptoWalletAddress, blank=True)

    # determine which product related to which page
    selected_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_product_opt = models.ForeignKey(ProductOptions, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User Info'

    def __str__(self):
        if self.page_name is not None:
            return self.page_name
        return self.user.username



"""
In order to get the raw info of models
get icon, name, etc. we create this class just like UserInfo model
"""


class Blank(models.Model):
    services = models.ManyToManyField(SocialMedia, blank=True)
    contact_info = models.ManyToManyField(ContactInfo, blank=True)
    images = models.ManyToManyField(BannerAndImage, blank=True)
    video_links = models.ManyToManyField(Video, blank=True)
    links = models.ManyToManyField(Links, blank=True)
    navigation_info = models.ManyToManyField(Navigations, blank=True)
    faq = models.ManyToManyField(FAQ, blank=True)
    free_texts = models.ManyToManyField(FreeText, blank=True)
    counter = models.ManyToManyField(Counter, blank=True)
    bank_account = models.ManyToManyField(BankAccounts, blank=True)
    crypto_wallet_address = models.ManyToManyField(CryptoWalletAddress, blank=True)

    def save(self, *args, **kwargs):

        blank_objects = Blank.objects.count()

        if blank_objects == 0:
            super(Blank, self).save(*args, **kwargs)
        else:
            return
