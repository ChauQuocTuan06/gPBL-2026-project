import RPi.GPIO as GPIO
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import requests
from time import sleep
import threading

# ====== TELEGRAM CONFIG ======
TOKEN = "8120771917:AAGBwURu68ZVwN8oczrReAizuPDE-VdQS14"
CHAT_ID = "8411566618"

# ====== GPIO CONFIG ======
LED = 4
VIB = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(VIB, GPIO.IN)

# ====== TELEGRAM MESSAGE SENDER ======
def sendTelegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

# ====== VIBRATION SENSOR THREAD ======
def check_vibration():
    while True:
        if GPIO.input(VIB) == 1:
            sendTelegram("Open the door")
            sleep(5)   # ch?ng spam
        sleep(0.1)

# ====== HANDLE TELEGRAM MESSAGE ======
async def handle_message(update, context):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()

    if text in ["on", "/on"]:
        GPIO.output(LED, 1)
        await update.message.reply_text("LED ON")

    elif text in ["off", "/off"]:
        GPIO.output(LED, 0)
        await update.message.reply_text("LED OFF")

# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # ch?y thread c?m bi?n
    threading.Thread(target=check_vibration, daemon=True).start()

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
