from django.urls import path
from .views import *

urlpatterns = [
    path('customized-product', CreateProductOptionInCart.as_view()),

    path('shop-categories', ShopCategoryView.as_view(), name='shop-categories'),

    path('products', GetProducts.as_view(), name='products'),
    path('products/<int:pk>', GetProducts.as_view(), name='products'),

    path('cart', CartView.as_view(), name='cart'),
    path('cart/<int:pk>', CartView.as_view(), name='cart'),

    path('order-items', OrderItemsView.as_view(), name='order-items'),
    path('order-items/<int:pk>', OrderItemsView.as_view(), name='order-items'),

    path('coupon', CouponView.as_view(), name='coupon'),
]
