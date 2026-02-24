
import RPi.GPIO as GPIO
import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from time import sleep
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
  
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("on", led_on))
app.add_handler(CommandHandler("off", led_off))
app.run_polling()


def sendTelegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url,data=data)
while True:
    if GPIO.input(VIB)==1:
        sendTelegram("Open the door")
        sleep(5)
