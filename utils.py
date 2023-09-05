import re
import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware


def is_valid_wallet_address(address):
    """Проверка валидности TRX адреса"""
    return bool(re.match(r'^T[0-9a-zA-Z]{33}$', address))


def is_valid_bnb_address(address):
    """Проверка валидности адреса BNB"""
    return bool(re.match(r'^0x[0-9a-fA-F]{40}$', address))


def is_valid_amount(amount):
    """Проверка что введёная сумма больше 0 и не отрицательная"""
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
    

def transaction_bnb(private_key, to_address, value):
    """Логика отправки BNB транзакции"""
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # Получение Nonce
    from_address = w3.eth.account.from_key(private_key).address
    nonce = w3.eth.get_transaction_count(from_address) 
    # Подготовка данных для отправки транзакции
    amount = Web3.to_wei(value, 'ether')

    tx_data = {
        'to': to_address,
        'value': amount,
        'gas': 200000,
        'gasPrice': w3.to_wei('5', 'gwei'),
        'nonce': nonce
    }
    signed_txn = w3.eth.account.sign_transaction(tx_data, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash.hex()        