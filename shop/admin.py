from django.contrib import admin
from .models import Cart, Product, ProductOptions, OrderItems, Category

admin.site.register(ProductOptions)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderItems)
admin.site.register(Category)

