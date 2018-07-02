from vlc import MediaPlayer
from time import sleep
from multiprocessing import Process

class My_Sleep_Timer(Process):

	def __init__(self, s):
		assert isinstance(s, Stream)
		Process.__init__(self)

	def run(self):
		sleep(600)
		s.grad_change_vol(s.volume/2, 240)
		s.grad_change_vol(0, 60)

class Stream:

	def __init__(self, url):
		self.player = MediaPlayer(url)
		self.stream_url = url
		self._volume = 0
		self.player.audio_set_volume(self._volume)
		self.player.play()
		self.timer = None

	@property
	def volume(self):
		return self._volume

	@volume.setter
	def volume(self, val):
		assert int(val) == val
		self._volume = int(val)
		self.set_volume(int(val))

	def grad_change_vol(self, d_vol, time):
		mod = d_vol - self.volume
		if not mod == 0:
			one_step_mod = mod/abs(mod)
			secs_per_step=time/abs(mod)
			for _ in range(abs(mod)):
				self.volume += one_step_mod
				sleep(secs_per_step)

	def set_volume(self, vol):
		self.player.audio_set_volume(vol)

	def set_sleep_timer(self, sleep_timer_class=My_Sleep_Timer):
		if self.timer != None:
			self.timer.terminate()
		self.timer = sleep_timer_class(self)
		self.timer.start()

	def quit(self):
		self.timer.terminate()
		self.player.stop()
