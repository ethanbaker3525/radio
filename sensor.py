import RPi.GPIO as GPIO
import time

class UltrasonicSensor:

    def __init__(self, trigger_pin, echo_pin, gpio_mode=GPIO.BOARD):
        GPIO.setmode(gpio_mode)
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        GPIO.output(trigger_pin, GPIO.LOW)

    def get_distance(self):
        while 1:
            
            try:
                GPIO.output(PIN_TRIGGER, GPIO.HIGH)
                time.sleep(0.00001)
                GPIO.output(PIN_TRIGGER, GPIO.LOW)
                while GPIO.input(PIN_ECHO)==0:
                    pulse_start_time = time.time()
                while GPIO.input(PIN_ECHO)==1:
                    pulse_end_time = time.time()
                pulse_duration = pulse_end_time - pulse_start_time
                time.sleep(0.00001)
                return round(pulse_duration * 17150, 2)

            except Exception as e:
                open('error_logs.txt', 'w').write(e+'\n')
                print('get_distance() ERROR WRITTEN TO error_logs.txt')

    def quit(self):
        GPIO.cleanup()
