import RPi.GPIO as GPIO
from time import sleep

PIN_TRIGGER = 16
PIN_ECHO = 18

class UltrasonicSensor:

    def __init__(self, trigger_pin, echo_pin, gpio_mode=GPIO.BOARD):
        GPIO.setmode(gpio_mode)
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        GPIO.output(trigger_pin, GPIO.LOW)

    def get_distance(self):
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()
         pulse_duration = pulse_end_time - pulse_start_time
         sleep(0.00001)
         return round(pulse_duration * 17150, 2)

    def quit(self):
        GPIO.cleanup()

class MyUltrasonicSensor(UltrasonicSensor):
    def __init__(self):
        UltrasonicSensor.__init__(self, PIN_TRIGGER, PIN_ECHO)

    def calibrate(self, num_tests=100):
        tests = [self.get_distance() for i in range(num_tests)]
        self.threshold = (sum(tests)/num_tests)*0.7 + min(tests)*0.3
        print("THRESHOLD SET TO: " +str(self.threshold))

    def run(self, rate):
        sleep_time = 1/rate

if __name__ == '__main__':
    x = MyUltrasonicSensor()
    for i in range(10):
        print(str(x.get_distance()))
        sleep(0.5)
    x.calibrate()
