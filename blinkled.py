import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)
while True:
  GPIO.output(4,True)
  sleep(4)
  GPIO.output(4,False)
  sleep(2)
