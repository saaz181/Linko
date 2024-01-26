import random
import string


def generate_random_code(model):
    LENGTH = 10
    characters = string.digits + string.ascii_letters
    symbols = '#@$%&='
    characters += symbols
    code = ''

    found_unique_code = False
    while not found_unique_code:
        code = ''.join(random.choices(characters, k=LENGTH))
        if model.objects.filter(code=code).count() == 0:
            found_unique_code = True

    return code
