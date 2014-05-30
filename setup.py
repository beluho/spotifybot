from distutils.core import setup
import py2exe
import os

sound_files = [
'sound/rewind.wav', 
'sound/klaxon.wav', 
'sound/boomsound.wav', 
'sound/give_it_to_me_hot.wav', 
'sound/listen.wav', 
'sound/roll_the_beat.wav', 
'sound/what_you_got.wav', 
'sound/yeaoh3.wav', 
'sound/you_what.wav', 
'sound/alright_now_were_flexing.wav', 
'sound/work_the_waistline.wav', 
'sound/larging_up_full_crew.wav', 
'sound/press_it_dont_distress_it.wav', 
'sound/vuvuzela.wav', 
'sound/wake_the_town.wav'
]

setup(
console= 'spotify_bot_2.0.py',
version= '0.2',
author= 'Luke Hodgkinson',
author_email= 'luke2442@gmail.com',
data_files= ['sounds', sound_files]
)
