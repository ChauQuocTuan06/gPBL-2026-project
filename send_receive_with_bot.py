import RPi.GPIO as GPIO
from telegram.ext import ApplicationBuilder, CommandHandler
import requests
from time import sleep
import threading

TOKEN = "8120771917:AAGBwURu68ZVwN8oczrReAizuPDE-VdQS14"
CHAT_ID = "8411566618"

LED = 4
VIB = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(VIB, GPIO.IN)


async def led_on(update, context):
    GPIO.output(LED, 1)
    await update.message.reply_text("LED ON")

async def led_off(update, context):
    GPIO.output(LED, 0)
    await update.message.reply_text("LED OFF")


def sendTelegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)


def check_vibration():
    while True:
        if GPIO.input(VIB) == 1:
            sendTelegram("Open the door")
            sleep(5)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("on", led_on))
app.add_handler(CommandHandler("off", led_off))
threading.Thread(target=check_vibration).start()
app.run_polling()
