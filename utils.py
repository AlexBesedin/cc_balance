import re
import requests

def is_valid_wallet_address(address):
    """Проверка валидности адреса"""
    return bool(re.match(r'^T[0-9a-zA-Z]{33}$', address))


def is_valid_amount(amount):
    """Проверка что введёная сумма больше 0"""
    try:
        amount = float(amount)
        if amount >= 0:
            return True
    except ValueError:
        pass
    return False


def get_balance_bnb(api_key, address):
    """Метод запроса баланса BNB адреса"""
    url = f'https://api.bscscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        balance = float(response.json()['result']) / 10**18
        return balance
    else:
        raise ValueError('Не удалось получить баланс')