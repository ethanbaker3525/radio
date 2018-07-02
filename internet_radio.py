import vlc
import threading
import time

from errorlogging import log
from streamer import Stream
from sensor import UltrasonicSensor


PIN_TRIGGER = 16
PIN_ECHO = 18
STREAM_URL = 'https://15903.live.streamtheworld.com/WYPR_HD2.mp3'
DESIRED_VOLUME = 50


class RadioUltrasonicSensor(UltrasonicSensor, Stream):

    def __init__(self, trigger_pin, echo_pin, stream_url, d_vol):
        UltrasonicSensor.__init__(self, trigger_pin, echo_pin)
        Stream.__init__(self, stream_url)
        self.d_vol = d_vol

    def calibrate(self, num_tests=1000):
        tests = [self.get_distance() for i in range(num_tests)]
        self.act_thresh = sum(tests)/num_tests * 0.5
        self.err_thresh = sum(tests)/num_tests * 1.5
        print('Calibration Completed')

    def loop(self):
        while 1:
            dist = self.get_distance()
            if dist < self.act_thresh:
                self.activate()
                while dist > self.err_thresh or dist < self.act_thresh:
                    dist = self.get_distance()
                    time.sleep(0.1)
            time.sleep(0.1)

    def activate(self):
        self.grad_change_vol(d_vol, 2)
        self.set_sleep_timer()

    def quit(self):
        UltrasonicSensor.quit()
        Stream.quit()

if __name__ == '__main__':

    device = RadioUltrasonicSensor(PIN_TRIGGER, PIN_ECHO, STREAM_URL, DESIRED_VOLUME)

    try:
        device.calibrate()
        device.loop()
    except Exception as e:
        log(e)
        device.quit()
