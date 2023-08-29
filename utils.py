import re


def is_valid_wallet_address(address):
    return bool(re.match(r'^T[0-9a-zA-Z]{33}$', address))


def is_valid_amount(amount):
    try:
        amount = float(amount)
        if amount >= 0:
            return True
    except ValueError:
        pass
    return False