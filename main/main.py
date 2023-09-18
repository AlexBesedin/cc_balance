from message_handlers import (
    get_balance_trx, 
    send_trx, 
    get_bnb_balance,
    get_info,
    send_bnb)
from config import bot


@bot.message_handler(commands=['trx_balance'])
def trx_balance_command_handler(message):
    """Хендлер команды /trx_balance"""
    get_balance_trx(message)   
    
    
@bot.message_handler(commands=['send_trx'])
def trx_send_command_handler(message):
    """Хендлер команды /send_trx"""
    send_trx(message)


@bot.message_handler(commands=['bnb_balance'])
def bnb_balance_command_handler(message):
    """Хендлер команды /bnb_balance"""
    get_bnb_balance(message)
    

@bot.message_handler(commands=['info'])
def info_command_handler(message):
    """Хендлер команды /info"""
    get_info(message)
    

@bot.message_handler(commands=['send_bnb'])
def bnb_send_command_handler(message):
    """Хендлер команды /send_bnb"""
    send_bnb(message)    
    

def main():
    bot.polling()

if __name__ == '__main__':
    main()