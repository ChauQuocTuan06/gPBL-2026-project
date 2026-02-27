import RPi.GPIO as GPIO
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import requests
from time import sleep
import threading
import serial

TOKEN = "8120771917:AAGBwURu68ZVwN8oczrReAizuPDE-VdQS14"
CHAT_ID = "8411566618"

LED = 4
LED2 = 22
VIB = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(VIB, GPIO.IN)

GPIO.output(LED,0)
GPIO.output(LED2,0)

# Serial
ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
sleep(2)
ser.reset_input_buffer()

def sendTelegram(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url,data=data)


def check_serial():

    while True:

        try:

            if ser.in_waiting > 0:

                data = ser.readline().decode("utf-8").strip()

                print("Arduino:",data)

                if data == "Open the door":

                    GPIO.output(LED,1)

                    sendTelegram("Door Opened")

                    sleep(3)

                    GPIO.output(LED,0)

        except Exception as e:

            print("Serial error:",e)

        sleep(0.1)


async def handle_message(update,context):

    text = update.message.text.lower()

    if text == "on":

        GPIO.output(LED2,1)

        await update.message.reply_text("LED ON")

    elif text == "off":

        GPIO.output(LED2,0)

        await update.message.reply_text("LED OFF")

def checkVibration():

    while True:

        if GPIO.input(VIB) == 1:

            sendTelegram("Hello there")

            sleep(5)

        sleep(0.1)

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    threading.Thread(target=check_serial,daemon=True).start()
    threading.Thread(target=checkVibration, daemon=True).start()
    print("Bot running...")

    app.run_polling()


try:
    main()

except KeyboardInterrupt:

    GPIO.cleanup()
