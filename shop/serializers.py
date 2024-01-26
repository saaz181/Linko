from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework import serializers
from .models import *
from accounts.serializers import AddressSerializer


class CreateProductSerializer(ModelSerializer):
    parent_product_id = serializers.IntegerField(required=True)
    cart_id = serializers.IntegerField(required=True)

    class Meta:
        model = ProductOptions
        fields = ['op_description',
                  'op_image',
                  'op_color',
                  'op_design',
                  'parent_product_id',
                  'cart_id',
                  ]


class GetProductOptionSerializer(ModelSerializer):
    class Meta:
        model = ProductOptions
        exclude = ['user', ]


class GetCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'image', ]
        extra_kwargs = {
            'image_url': {'view_name': 'shop-categories', 'lookup_field': 'image'},
        }


class GetProductSerializer(ModelSerializer):
    other_branches = GetProductOptionSerializer(read_only=True, many=True)
    category = GetCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class GetCartSerializer(ModelSerializer):
    product = GetProductSerializer(read_only=True)
    selected_product = GetProductOptionSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ['user', ]

    def get_total_price(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return Cart.calculate_total_price_items(user)


class UpdateCartObjSerializer(serializers.Serializer):
    patch_req_for_quantity = serializers.CharField(max_length=6, required=False)
    page_name_update = serializers.CharField(max_length=50, required=False)
    card_photo = serializers.ImageField(validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'])], required=False)
    card_text = serializers.CharField(max_length=2000, required=False)


class CreateCartObjSerializer(serializers.Serializer):
    product = serializers.IntegerField(required=True, validators=[MinValueValidator(0), ])
    selected_product = serializers.IntegerField(required=True, validators=[MinValueValidator(0), ])
    quantity = serializers.IntegerField(required=True, validators=[MinValueValidator(1), ])
    scan_option = serializers.CharField(max_length=11, default='nfc')


class GetOrderItemsSerializer(ModelSerializer):
    address = AddressSerializer(read_only=True)
    orders = GetCartSerializer(read_only=True, many=True)
    coupon_code = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = OrderItems
        exclude = ['user', ]


class CreateOrderItemSerializer(serializers.Serializer):
    address = serializers.IntegerField(required=True)
    coupon_code = serializers.CharField(max_length=20, required=False)



class CouponSerializer(ModelSerializer):
    coupon_code = serializers.CharField(max_length=15)
    order_item_id = serializers.IntegerField(required=True)


class GetCouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        exclude = ['user', ]
