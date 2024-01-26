import string
import random


def validate_type(*variables, data_type=None) -> bool:
    is_valid = True
    try:
        for var in variables:
            if type(data_type(var)) != data_type:
                is_valid = not is_valid
    except ValueError:
        is_valid = False

    return is_valid


def generate_coupon_code():
    length = 15
    characters = string.digits + string.ascii_letters
    choices = ''.join(random.choices(characters, k=length))

    return choices
