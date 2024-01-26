from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


def generate_order_id():
    found_order_id = False
    order_id = ""
    while not found_order_id:
        order_id = str(uuid.uuid1())
        if PaymentId.objects.filter(order_id=order_id).count() == 0:
            found_order_id = True
    return order_id


class PaymentId(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    trans_id = models.CharField(max_length=255, unique=True)
    amount = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return self.order_id
