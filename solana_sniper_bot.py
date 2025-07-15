import os
import requests
import json
from solana.rpc.api import Client
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, Updater

# ENVIRONMENT
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))
PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL", "https://api.mainnet-beta.solana.com")  # ✅ perbaikan di sini

# INIT
bot = Bot(token=BOT_TOKEN)
client = Client(RPC_URL)

# --- SNIPER LOGIC ---

def check_new_tokens():
    # Placeholder untuk deteksi token baru (nanti bisa dari webhook, websocket, atau API Solana)
    # Kirim notifikasi jika ada token baru
    token_address = "DEMO_TOKEN_ADDRESS"
    send_alert(token_address)

def send_alert(token_address):
    keyboard = [
        [
            InlineKeyboardButton("BUY $5", callback_data=f"buy_5_{token_address}"),
            InlineKeyboardButton("BUY $10", callback_data=f"buy_10_{token_address}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=TELEGRAM_USER_ID, text=f"Token baru terdeteksi:\n{token_address}", reply_markup=reply_markup)

# --- TELEGRAM HANDLER ---

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot sniper aktif dan siap mendeteksi token baru!")

def check(update: Update, context: CallbackContext):
    check_new_tokens()
    update.message.reply_text("✅ Token dummy dikirim (testing).")

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data.split("_")
    action = data[0]
    amount = data[1]
    token_address = "_".join(data[2:])
    if action == "buy":
        query.edit_message_text(text=f"✅ BUY ${amount} untuk {token_address} berhasil (simulasi).")
        # Tambahkan logic transaksi real di sini

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check))  # ✅ Tambahan untuk test manual
    dp.add_handler(CallbackQueryHandler(button))
    check_new_tokens()  # ✅ Trigger dummy token saat bot start
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
