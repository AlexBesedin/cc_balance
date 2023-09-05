import time
from config import (
    bot,
    client, 
    priv_key,
    TRX_WALLET, 
    API_KEY_BNB, 
    BNB_WALLET,
    BNB_PRIVATE_KEY,
    )
from utils import (
    is_valid_wallet_address, 
    is_valid_amount, 
    get_balance_bnb,
    transaction_bnb,
    is_valid_bnb_address)


def get_info(message):
    """Обработчик команды /info"""
    bot.send_message(
        chat_id=message.chat.id,
        text="/bnb_balance - Текущий баланс BNB кошелька\r\n"
             "/trx_balance - Текущий баланс TRX кошелька\r\n"
             "/send_bnb - Пополнить счёт своего BNB кошелька\r\n"
             "/send_trx - Пополнить счёт своего TRX кошелька\r\n"
    )


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
        balance = client.get_account_balance(TRX_WALLET)
        value_view = int(user_message[2])
        if not is_valid_wallet_address(user_wallet_trx):
            bot.send_message(
                chat_id=message.chat.id,
                text="Некорректный адрес получателя. Пожалуйста, убедитесь, что вы ввели правильный адрес.")
        elif not is_valid_amount(value):
            bot.send_message(
                chat_id=message.chat.id,
                text="Некорректная сумма. Пожалуйста, убедитесь, что вы ввели правильную сумму.")
        elif value > balance:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Введенная сумма {value_view} TRX превышает доступный баланс {balance} TRX'
            )
        else:
            txn = (
                client.trx.transfer(
                    TRX_WALLET, 
                    user_wallet_trx, 
                    value)
                .build()
                .sign(priv_key))
            print(f'txID: {txn.txid}')
            print(txn.broadcast().wait())
            time.sleep(2)
            bot.send_message(
                chat_id=message.chat.id,
                text=f"txID: {txn.txid}")
            time.sleep(3)
            new_balance = client.get_account_balance(TRX_WALLET)
            bot.send_message(
                chat_id=message.chat.id,
                text=f"Средства успешно отправлены.\n "
                f"Новый баланс кошелька: {new_balance} TRX")

                  
def get_bnb_balance(message):
    """Метод проверки баланса BNB кошелька"""
    balance = get_balance_bnb(API_KEY_BNB, BNB_WALLET)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Текущий баланс: {balance:.4f} BNB')
    

def send_bnb(message):
    """Отправка тразакции на указанный кошелёк пользователем"""
    parameters = message.text.split(' ')
    if len(parameters) != 3:
        bot.send_message(
            chat_id=message.chat.id,
            text="Некорректный ввод параметров. \r\n"
            "Используйте команду /send_bnb <адрес получателя> <сумма>")
        return

    to_address = parameters[1]
    value = float(parameters[2])
    balance = get_balance_bnb(API_KEY_BNB, BNB_WALLET)
    if not is_valid_bnb_address(to_address):
        bot.send_message(
            chat_id=message.chat.id,
            text="Некорректный адрес получателя. Пожалуйста, убедитесь, что вы ввели правильный адрес."  
        )
    elif not is_valid_amount(value):
        bot.send_message(
            chat_id=message.chat.id,
            text="Некорректная сумма. Пожалуйста, убедитесь, что вы ввели правильную сумму."  
        )
    else:
        if value > balance:
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Введёная сумма {value} BNB превышает доступный баланс {balance:.6f} BNB '
            )
        else:
            result = transaction_bnb(BNB_PRIVATE_KEY, to_address, value)
            print(result)
            time.sleep(5)
            balance = get_balance_bnb(API_KEY_BNB, BNB_WALLET)
            bot.send_message(
                message.chat.id,
                text=f'Средства успешно отправлены.\r\n'
                    f'Обновлённый баланс: {balance:.6f} BNB'
            )