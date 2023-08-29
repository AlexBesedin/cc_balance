from message_handlers import get_balance_trx, send_trx
from config import bot


@bot.message_handler(commands=['trx_balance'])
def start_command_handler(message):
    """Хендлер команды /trx_balance"""
    get_balance_trx(message)   
    
    

@bot.message_handler(commands=['send_trx'])
def send_command_handler(message):
    """Хендлер команды /send_trx"""
    send_trx(message)

    
def main():
    bot.polling()



if __name__ == '__main__':
    main()