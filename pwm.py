import RPi.GPIO as GPIO
from time import sleep
ledPin = 4
try:
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(ledPin,GPIO.OUT)
  pwm=GPIO.PWM(ledPin,100)
  pwm.start(0)
  while True:
    for duty in range (100):
      print (duty)
      pwm.changeDutyCycle(duty)
      sleep(0.2)
      if(duty>100) : duty = 0
except KeyboardInterrupt:
  print("Complete")
  pass
finally:
  GPIO.cleanup()
