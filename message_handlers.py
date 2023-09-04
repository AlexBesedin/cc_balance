import time
from config import (
    bot,
    client, 
    priv_key,
    TRX_WALLET, 
    API_KEY_BNB, 
    BNB_WALLET)
from utils import (
    is_valid_wallet_address, 
    is_valid_amount, 
    get_balance_bnb)


def get_balance_trx(message):
        """Метод получение баланса TRX кошелька"""
        balance = client.get_account_balance(TRX_WALLET)
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Текущий баланс: {balance} TRX')
    

def send_trx(message):
    """Метод отправки транзакции TRX"""
    user_message = message.text.split()
    if len(user_message) != 3:
        bot.send_message(
            chat_id=message.chat.id,
            text="Некорректный ввод параметров. \r\n"
             "Используйте команду /send_trx <адрес получателя> <сумма>")
    else:
        user_wallet_trx = user_message[1]
        value = int(user_message[2]) * 1_000_000
        
        if not is_valid_wallet_address(user_wallet_trx):
            bot.send_message(
                chat_id=message.chat.id,
                text="Некорректный адрес получателя. Пожалуйста, убедитесь, что вы ввели правильный адрес.")
        elif not is_valid_amount(value):
            bot.send_message(
                chat_id=message.chat.id,
                text="Некорректная сумма. Пожалуйста, убедитесь, что вы ввели правильную сумму.")
        else:
            txn = (
                client.trx.transfer(
                    TRX_WALLET, 
                    user_wallet_trx, 
                    value)
                .build()
                .sign(priv_key))
            print(f'txID:{txn.txid}')
            print(txn.broadcast().wait())
            time.sleep(2)
            bot.send_message(
                chat_id=message.chat.id,
                text=f"txID: {txn.txid}")
            time.sleep(3)
            balance = client.get_account_balance(TRX_WALLET)
            bot.send_message(
                chat_id=message.chat.id,
                text=f"Средства успешно отправлены.\n "
                f"Новый баланс кошелька: {balance} TRX")
            
            
def get_bnb_balance(message):
    """Метод проверки баланса BNB кошелька"""
    balance = get_balance_bnb(API_KEY_BNB, BNB_WALLET)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Текущий баланс: {balance:.4f} BNB')
    