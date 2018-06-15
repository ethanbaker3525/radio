import RPi.GPIO as GPIO
import time

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
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        time.sleep(0.00001)
        return round(pulse_duration * 17150, 2)

    def quit(self):

        GPIO.cleanup()

class MyUltrasonicSensor(UltrasonicSensor):

    def __init__(self):

        UltrasonicSensor.__init__(self, PIN_TRIGGER, PIN_ECHO)

    def calibrate(self, num_tests=100, avg_w=0.7, min_w=0.3):

        tests = [self.get_distance() for i in range(num_tests)]
        self.threshold = (sum(tests)/num_tests)*avg_w + min(tests)*min_w
        print("THRESHOLD SET TO: " +str(self.threshold))

    def activation_meth():

        print('activated')

    def loop(self, rate_s=25, minimum_overhead_time_s=0.05, ma_number=3):

        sleep_time = 1/rate_s
        num_ticks = 1+rate_s*minimum_overhead_time_s
        counter = 0
        ma = []

        for i in range(ma_number):
            ma.append(self.get_distance())
            time.sleep(sleep_time)
        while 1:
            del ma[0]
            ma.append(self.get_distance())
            if sum(ma)/ma_number < self.threshold:
                counter += 1
                if counter >= num_ticks:
                    self.activation_meth()
            else:
                counter = 0
            time.sleep(sleep_time)

if __name__ == '__main__':

    x = MyUltrasonicSensor()
    input('Press enter to begin calibration.')
    x.calibrate()
    x.loop()
    x.quit()
