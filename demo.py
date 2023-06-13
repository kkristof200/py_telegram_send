from ktg import Telegram

TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

tg = Telegram(
    token=TELEGRAM_TOKEN,
    chat_id=TELEGRAM_CHAT_ID
)

tg.send('message')