from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from collections import OrderedDict
from shop.serializers import GetProductOptionSerializer, GetProductSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AbstractDataSerializer(ModelSerializer):
    class Meta:
        model = AbstractData
        fields = '__all__'


class SocialMediaSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SocialMedia
        exclude = ['user', ]

    # https://stackoverflow.com/questions/27015931/remove-null-fields-from-django-rest-framework-response
    def to_representation(self, instance):
        result = super(SocialMediaSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class ContactInfoSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ContactInfo
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(ContactInfoSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class BannerAndImageSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = BannerAndImage
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(BannerAndImageSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class VideoSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Video
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(VideoSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class LinksSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Links
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(LinksSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class NavigationsSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Navigations
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(NavigationsSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class FAQSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = FAQ
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(FAQSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class FreeTextSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = FreeText
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(FreeTextSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class BankAccountsSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = BankAccounts
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(BankAccountsSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class CryptoWalletAddressSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = CryptoWalletAddress
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(CryptoWalletAddressSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class CounterSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Counter
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(CounterSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class UserInfoForPublic(ModelSerializer):
    services = SocialMediaSerializer(read_only=True, many=True)
    contact_info = ContactInfoSerializer(read_only=True, many=True)
    images = BannerAndImageSerializer(read_only=True, many=True)
    video_links = VideoSerializer(read_only=True, many=True)
    links = LinksSerializer(read_only=True, many=True)
    navigation_info = NavigationsSerializer(read_only=True, many=True)
    faq = FAQSerializer(read_only=True, many=True)
    free_texts = FreeTextSerializer(read_only=True, many=True)
    counter = CounterSerializer(read_only=True, many=True)
    bank_account = BankAccountsSerializer(read_only=True, many=True)
    crypto_wallet_address = CryptoWalletAddressSerializer(read_only=True, many=True)

    class Meta:
        model = UserInfo
        exclude = ['user', 'selected_product', 'selected_product_opt']

    def to_representation(self, instance):
        result = super(UserInfoForPublic, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class UserInfoSerializer(ModelSerializer):
    services = SocialMediaSerializer(read_only=True, many=True)
    contact_info = ContactInfoSerializer(read_only=True, many=True)
    images = BannerAndImageSerializer(read_only=True, many=True)
    video_links = VideoSerializer(read_only=True, many=True)
    links = LinksSerializer(read_only=True, many=True)
    navigation_info = NavigationsSerializer(read_only=True, many=True)
    faq = FAQSerializer(read_only=True, many=True)
    free_texts = FreeTextSerializer(read_only=True, many=True)
    counter = CounterSerializer(read_only=True, many=True)
    bank_account = BankAccountsSerializer(read_only=True, many=True)
    crypto_wallet_address = CryptoWalletAddressSerializer(read_only=True, many=True)
    selected_product = GetProductSerializer(read_only=True)
    selected_product_opt = GetProductOptionSerializer(read_only=True)

    class Meta:
        model = UserInfo
        exclude = ['user', ]

    def to_representation(self, instance):
        result = super(UserInfoSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class UserInfoPatchSerializer(serializers.Serializer):
    page_name = serializers.CharField(max_length=50, required=True, write_only=True)
    user_info_id = serializers.IntegerField(required=True, write_only=True)


class BlankSerializer(ModelSerializer):
    services = SocialMediaSerializer(read_only=True, many=True)
    contact_info = ContactInfoSerializer(read_only=True, many=True)
    images = BannerAndImageSerializer(read_only=True, many=True)
    video_links = VideoSerializer(read_only=True, many=True)
    links = LinksSerializer(read_only=True, many=True)
    navigation_info = NavigationsSerializer(read_only=True, many=True)
    faq = FAQSerializer(read_only=True, many=True)
    free_texts = FreeTextSerializer(read_only=True, many=True)
    counter = CounterSerializer(read_only=True, many=True)
    bank_account = BankAccountsSerializer(read_only=True, many=True)
    crypto_wallet_address = CryptoWalletAddressSerializer(read_only=True, many=True)

    class Meta:
        model = Blank
        fields = '__all__'

    def to_representation(self, instance):
        result = super(BlankSerializer, self).to_representation(instance)

        return OrderedDict([(key, result[key]) for key in result if result[key] != []])




