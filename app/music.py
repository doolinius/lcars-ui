import vlc
import time

url = 'https://streamingv2.shoutcast.com/1005-womp-fm'

#define VLC instance
instance = vlc.Instance()

#Define VLC player
player=instance.media_player_new()

#Define VLC media
media=instance.media_new(url)

#Set player media
player.set_media(media)

#Play the media
player.play()

time.sleep(120)

'''

p = vlc.MediaPlayer(url)

p.play()
'''
