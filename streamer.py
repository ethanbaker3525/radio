from vlc import MediaPlayer
from time import sleep
from json import loads

def fade_volume(p, time):
	secs_per_step=time/100
	for i in range(100):
		p.audio_set_volume(99-i)
		sleep(secs_per_step)

def raise_volume(p, time):
	secs_per_step=time/100
	for i in range(100):
		p.audio_set_volume(i+1)
		sleep(secs_per_step)

def get_streams(dir='streams.json'):
	with open('streams.json') as f:
		return loads(f.read())

streams = get_streams()

player = MediaPlayer(streams['rap']['station1']['url'])
player.play()

while 1:
	data = input('Genere/Station: ').split('/')
	streams = get_streams()
	fade_volume(player, 3)
	player.stop()
	player = MediaPlayer(streams[data[0]][data[1]]['url'])
	player.play()
	player.audio_set_volume(0)
	sleep(2)
	raise_volume(player, 3)


'''player.play()
player.audio_set_volume(0)
raise_volume(player, 10)
sleep(10)
fade_volume(player, 10)
player.stop()'''
