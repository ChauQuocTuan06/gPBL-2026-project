import RPi.GPIO as GPIO
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8120771917:AAGBwURu68ZVwN8oczrReAizuPDE-VdQS14"

LED = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

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
