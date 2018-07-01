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
        self.volume = 50

    def calibrate(self, num_tests=100):

        tests = [self.get_distance() for i in range(num_tests)]
        self.act_thresh = sum(tests)/num_tests * 0.9
        self.err_thresh = sum(tests)/num_tests * 1.5

    def loop(self, rate_s=50, minimum_overhead_time_s=0.05, ma_number=6):

        while 1:
            dist = self.get_distance()
            if dist < self.act_thresh:
                print('activated')
                while dist > self.err_thresh or dist < self.act_thresh:
                    dist = self.get_distance()
                    time.sleep(0.1)
            time.sleep(0.1)



if __name__ == '__main__':

    x = MyUltrasonicSensor()
    input('Press enter to begin calibration.')
    x.calibrate()
    x.loop()
    x.quit()
