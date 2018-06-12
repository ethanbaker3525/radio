import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 16
PIN_ECHO = 18

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, GPIO.LOW)

def get_distance():

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

      time.sleep(0.00001)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      return round(pulse_duration * 17150, 2)

for i in range(30):
      print(str(get_distance()))
      time.sleep(0.25)

GPIO.cleanup()
