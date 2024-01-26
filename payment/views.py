from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .utils import *
from shop.models import Cart, OrderItems, Coupon
from .credentials import redirect_user_to_bank
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

CURRENCY = 'IRT'  # تومان
HOST = ""

USERINFO_CREATE_PERM = 'can_create_link_on_user_info'


# carve out name from user object
def get_name(user_obj):
    name = ''
    if user_obj.name:
        return user_obj.name
    return name


class PaymentId(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user

        amount = Cart.calculate_total_price_items(user, currency_type=CURRENCY)
        payer_name = get_name(user)
        customer_phone = user.phone_number
        currency = CURRENCY

        order_item = OrderItems.objects.filter(user=user).last()

        if hasattr(order_item.coupon, 'coupon_code'):
            coupon_code = order_item.coupon.coupon_code

            amount = Coupon.calculate_total_price_with_coupon(user, amount, coupon_code)

        data = {
            'amount': amount,
            'payer_name': payer_name,
            'customer_phone': customer_phone,
            'currency': currency,
            'user': user
        }

        result = create_token(**data)

        if result:
            redirect_url = redirect_user_to_bank + str(result)

            return Response({'message': redirect_url}, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def nextpay_callback(request):
    trans_id = request.GET.get('trans_id')
    order_id = request.GET.get('order_id')
    amount = request.GET.get('amount')

    data = {
        'trans_id': trans_id,
        'order_id': order_id,
        'amount': amount,
        'currency': CURRENCY
    }

    verified_payment = verify_payment(**data)

    payment_id = PaymentId.objects.filter(order_id=order_id, trans_id=trans_id).first()
    user = payment_id.user

    order_item = OrderItems.objects.filter(user=user).last()

    if verified_payment:

        cart_obj = Cart.objects.filter(user=user, ordered=False)

        for item in cart_obj:
            item.ordered = True
            item.save()
            order_item.orders.add(item)

        order_item.amount = amount
        order_item.ordered = True
        order_item.save()

        # adding user to groups
        access_links_group = Group.objects.get(name='access_links')
        customization_group = Group.objects.get(name='customization')

        access_links_group.user_set.add(user)
        customization_group.user_set.add(user)

        permission = Permission.objects.get_or_create(name=USERINFO_CREATE_PERM)
        user.user_permissions.add(permission)

        return redirect(f'{HOST}/orders')

    order_item.delete()
    return redirect(f'{HOST}/cart')
