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
SERVO = 13
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(VIB, GPIO.IN)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.output(LED,0)
GPIO.output(LED2,0)
pwm = GPIO.PWM(SERVO, 50)
pwm.start(0)
# Serial
ser = None

def connect_serial():
    global ser
    while True:
        try:
            ser = serial.Serial('/dev/serial/by-id/usb-Arduino_UNO_WiFi_R4_CMSIS-DAP_D885ACA775B4-if01', 9600, timeout=1)
            sleep(3)   # Arduino c?n th?i gian reset
            ser.reset_input_buffer()
            print("Serial connected")
            break
        except Exception as e:
            print("Waiting Arduino...", e)
            sleep(2)

connect_serial()

def sendTelegram(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url,data=data)

def setAngle(angle):
    duty = 2.5 + (angle / 180)*10
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)
    pwm.ChangeDutyCycle(0)
    
def check_serial():

    global ser

    while True:

        try:

            if ser and ser.is_open and ser.in_waiting > 0:

                data = ser.readline().decode("utf-8").strip()

                print("Arduino:",data)

                if data == "Open the door":

                    GPIO.output(LED,1)
                    sendTelegram("Password is correct!!! Do you want to open the door???")

                    sleep(3)
                    GPIO.output(LED,0)

        except Exception as e:

            print("Serial error:",e)

            try:
                ser.close()
            except:
                pass

            connect_serial()   # reconnect

        sleep(0.1)


async def handle_message(update,context):

    text = update.message.text.lower()

    if text == "on":
        GPIO.output(LED2,1)
        await update.message.reply_text("LED ON")

    elif text == "off":
        GPIO.output(LED2,0)
        await update.message.reply_text("LED OFF")
        
    elif txt == "open":
        setAngle(90)
        await update.message.reply_text("THE DOOR IS OPENED")
        
    elif txt == "close":
        setAngle(0)
        await update.message.reply_text("THE DOOR IS CLOSED")
    
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
    pwm.stop()
    GPIO.cleanup()
