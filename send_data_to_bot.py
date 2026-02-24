import RPi.GPIO as GPIO
import requests
from time import sleep

VIB = 4

TOKEN = "8120771917:AAGBwURu68ZVwN8oczrReAizuPDE-VdQS14"
CHAT_ID = "8411566618"

GPIO.setmode(GPIO.BCM)
GPIO.setup(VIB, GPIO.IN)

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
