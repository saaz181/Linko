from requests import post, get
from .credentials import *
from .models import *


def create_token(**kwargs):
    order_id = generate_order_id()
    user = kwargs.get('user')
    kwargs.pop('user')

    data = {
        'api_key': API_KEY,
        'order_id': order_id,
        'callback_uri': CALLBACK_URI,
        **kwargs
    }
    print(data)

    headers = {
        'Content-Type': 'application/json'
    }

    response = post(create_token_url, data=data, headers=headers)

    """
    response ->
     {
        code: '',
        trans_id: ''
     }
    """
    print(response.status_code)
    res_json = response.json()
    print(res_json)
    if res_json.get('code') == -1:
        trans_id = res_json.get('trans_id')
        PaymentId.objects.create(user=user,
                                 order_id=order_id,
                                 trans_id=trans_id,
                                 amount=kwargs.get('amount')
                                 )
        return trans_id

    return False


def verify_payment(**kwargs):

    data = {
        'api_key': API_KEY,
        **kwargs
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = post(verify_payment_url, data=data, headers=headers)

    res_json = response.json()

    if res_json.get('code') == 0:
        return res_json
    return False
