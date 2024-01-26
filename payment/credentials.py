# nextpay api docs
# https://nextpay.org/nx/docs

API_KEY = "038d1d78-c07f-4119-9ff0-fa267611776d"
CALLBACK_URI = "http://127.0.0.1:8000/payment/callback"


create_token_url = "https://nextpay.org/nx/gateway/token"  # POST
redirect_user_to_bank = "https://nextpay.org/nx/gateway/payment/"  # POST
verify_payment_url = 'https://nextpay.org/nx/gateway/verify'  # POST

create_token_customer_field = {
    'amount': 0,        # required
    'currency': 'IRT',  # IRR | IRT
    'customer_phone': 0,
    'custom_json_fields': {},
    'payer_name': "",
    'payer_desc': "",
}
