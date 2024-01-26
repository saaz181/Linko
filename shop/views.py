import enum

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .UploadTextPhotoPermission import UploadAccess
from .models import *
from .serializers import *
from .utils import validate_type
from django.db.models import Q
from django.utils import timezone
from rest_framework.generics import ListAPIView
from accounts.models import Address


class CartUpdateQuantity(enum.Enum):
    ADD = 'ADD'
    REMOVE = 'REMOVE'


class CreateProductOptionInCart(APIView):
    permission_classes = [IsAuthenticated, UploadAccess]
    serializer_class = CreateProductSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            parent_product_id = serializer.validated_data.get('parent_product_id')
            cart_id = serializer.validated_data.get('cart_id')

            op_description = serializer.validated_data.get('op_description')
            op_image = serializer.validated_data.get('op_image')
            op_color = serializer.validated_data.get('op_color')
            op_design = serializer.validated_data.get('op_design')

            user_cart = Cart.objects.filter(id=cart_id, product__id=parent_product_id)

            if user_cart.exists():
                prod = Product.objects.filter(id=parent_product_id)

                if prod.exists():
                    prod = prod.first()
                    if prod.typeof == ProductType.edit.value or prod.typeof == ProductType.full_edit.value:
                        prod_opt = ProductOptions.objects.create(user=user,
                                                                 op_description=op_description,
                                                                 op_image=op_image,
                                                                 op_color=op_color,
                                                                 op_design=op_design,
                                                                 typeof=prod.typeof)

                        # this the only one that exists
                        user_cart = user_cart.first()
                        user_cart.selected_product = prod_opt
                        user_cart.save()
                        return Response({'message': 'File SuccessFully Uploaded'}, status=status.HTTP_200_OK)

                    return Response({'message': 'You can\'t change the product opt'}, status=status.HTTP_204_NO_CONTENT)

                return Response({'message': 'Product Parent Node Does not exists'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'Cart not found!'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShopCategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = GetCategorySerializer
    permission_classes = [AllowAny, ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProducts(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = GetProductSerializer
    model = Product

    def get(self, request, pk=None):
        if not pk:
            prod_obj = self.model.objects.all()
            return Response(self.serializer_class(prod_obj, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        elif pk is not None:
            prod_obj = self.model.objects.filter(id=pk)
            if prod_obj.exists():
                prod_obj = prod_obj.first()
                return Response(self.serializer_class(prod_obj, context={'request': request}).data,
                                status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GetCartSerializer

    def get(self, request, pk=None):
        user = request.user

        if pk is not None:
            cart_item = Cart.objects.filter(id=pk, user=user, ordered=False)

            if cart_item.exists():
                return Response(self.serializer_class(cart_item, context={'request': request}).data,
                                status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart_items = Cart.objects.filter(user=user, ordered=False)

        if cart_items.exists():
            return Response(self.serializer_class(cart_items, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CreateCartObjSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            product_id = serializer.validated_data.get('product')
            selected_product = serializer.validated_data.get('selected_product')
            scan_option = serializer.validated_data.get('scan_option')
            page_name = serializer.validated_data.get('page_name')
            quantity = serializer.validated_data.get('quantity')

            product_obj = Product.objects.filter(id=product_id)
            if product_obj.exists():
                product_obj = product_obj.first()
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

            cart_obj = Cart.objects.filter(user=user, ordered=False) \
                .filter(Q(product__id=product_id) & Q(selected_product__id=selected_product))

            if not cart_obj.exists():
                if 1 <= quantity <= product_obj.quantity:
                    selected_product = ProductOptions.objects.get(id=selected_product)

                    new_item_in_cart = Cart.objects.create(user=user,
                                                           product=product_obj,
                                                           selected_product=selected_product,
                                                           quantity=quantity,
                                                           scan_option=scan_option)

                    return Response(self.serializer_class(new_item_in_cart).data, status=status.HTTP_201_CREATED)

                return Response({'message': 'Quantity is High!'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Product Already Exists'}, status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        serializer = UpdateCartObjSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            quantity = serializer.validated_data.get('patch_req_for_quantity')
            page_name = serializer.validated_data.get('page_name_update')
            card_photo = serializer.validated_data.get('card_photo')
            card_text = serializer.validated_data.get('card_text')

            if pk is not None:
                cart_obj = Cart.objects.filter(user=user, ordered=False, id=pk)

                if cart_obj.exists():
                    cart_obj = cart_obj.first()

                    if quantity == CartUpdateQuantity.ADD.value:
                        cart_obj.quantity += 1
                        cart_obj.page_name = page_name
                        cart_obj.card_design = card_photo
                        cart_obj.card_text = card_text

                    elif quantity == CartUpdateQuantity.REMOVE.value:
                        if cart_obj.quantity - 1 > 0:
                            cart_obj.quantity -= 1
                            cart_obj.page_name = page_name
                            cart_obj.card_design = card_photo
                            cart_obj.card_text = card_text

                        else:
                            return Response(status=status.HTTP_400_BAD_REQUEST)

                    cart_obj.save()
                    return Response(self.serializer_class(cart_obj).data, status=status.HTTP_200_OK)

                else:
                    return Response({'message': 'Cart Item not found!'}, status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Cart id is not satisfied!'}, status.HTTP_404_NOT_FOUND)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            user = request.user
            cart_obj = Cart.objects.filter(user=user, id=pk, ordered=False)

            if cart_obj.exists():
                cart_obj.delete()
                return Response({'message': 'Cart Item Deleted'}, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderItemsView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = GetOrderItemsSerializer

    @staticmethod
    def validate_user_cart(user_cart):
        for item in user_cart:
            if item.page_name == "" or item.page_name is None or not item.page_name:
                return False
        return True

    def get(self, request, pk=None):
        user = request.user
        if pk is not None:
            order_item = OrderItems.objects.filter(id=pk, user=user, ordered=True)

            if order_item.exists():
                order_item = order_item.first()
                return Response(self.serializer_class(order_item).data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)

        order_items = OrderItems.objects.filter(user=user, ordered=True)

        if order_items.exists():
            order_items = order_items.order_by('-date_ordered')
            return Response(self.serializer_class(order_items, many=True).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CreateOrderItemSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            address_id = serializer.validated_data.get('address')
            coupon_code = serializer.validated_data.get('coupon_code')

            user_cart = Cart.objects.filter(user=user, ordered=False)

            coupon_obj = None
            if coupon_code:
                coupon_obj = Coupon.objects.filter(user=user,
                                                   active=True,
                                                   usage_times__gte=1,
                                                   usage_times__lte=MAX_USAGE_TIMES,
                                                   coupon_code=coupon_code,
                                                   date_coupon_ends__gte=timezone.now())

                if coupon_obj.exists():
                    coupon_obj = coupon_obj.first()

            address = Address.objects.filter(user_addr=user, id=address_id)
            is_user_cart_valid = self.validate_user_cart(user_cart)
            if address.exists():

                if is_user_cart_valid:
                    address = address.first()
                    order_item = OrderItems.objects.create(user=user, address=address, coupon=coupon_obj)

                    return Response(self.serializer_class(order_item).data, status=status.HTTP_201_CREATED)

                else:
                    return Response({'message': 'Your cart items should have specific "page-name"'},
                                    status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'No Address Found'}, status=status.HTTP_404_NOT_FOUND)

        # print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CouponView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CouponSerializer

    def get(self, request):
        user = request.user
        coupon_obj = Coupon.objects.filter(user=user,
                                           active=True,
                                           usage_times__lte=MAX_USAGE_TIMES,
                                           usage_times__gte=1,
                                           date_coupon_ends__gte=timezone.now()
                                           )

        if coupon_obj.exists():
            return Response(GetCouponSerializer(coupon_obj, many=True).data, status=status.HTTP_200_OK)

        return Response({'message': 'No Coupon Found!'}, status=status.HTTP_404_NOT_FOUND)

    # this :post can be deleted
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            coupon_code = serializer.validated_data.get('coupon_code')
            order_item_id = serializer.validated_data.get('order_item_id')

            coupon_obj = Coupon.objects.filter(user=user,
                                               active=True,
                                               usage_times__gte=1,
                                               usage_times__lte=MAX_USAGE_TIMES,
                                               coupon_code=coupon_code,
                                               date_coupon_ends__gte=timezone.now()
                                               )

            if coupon_obj.exists():
                order_item = OrderItems.objects.filter(id=order_item_id, user=user)

                if order_item.exists():
                    order_item = order_item.first()
                    order_item.coupon = coupon_obj.first().coupon_code
                    order_item.save()

                    order_item.use_coupon()
                    return Response({'message': 'Coupon Applied Successfully'}, status=status.HTTP_200_OK)

                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_404_NOT_FOUND)
