from jabberbot import JabberBot, botcmd
from pytify import Spotify
import speech
import pyglet 
import datetime
import time
import logging
logging.basicConfig()
import sys
import os
import re
import sys
import thread
import subprocess
import winsound
from datetime import datetime
import pickle
from datetime import datetime
import webbrowser

#SoundBoard & Rewind
rewind = "sound/rewind.wav"
klaxon = "sound/klaxon.wav"
boomsound = "sound/boomsound.wav"
hot = "sound/give_it_to_me_hot.wav"
hlisten = "sound/listen.wav"
roll = "sound/roll_the_beat.wav"
what = "sound/what_you_got.wav"
yeah = "sound/yeaoh3.wav"
you_what = "sound/you_what.wav"
flexin = "sound/alright_now_were_flexing.wav"
waistline = "sound/work_the_waistline.wav"
cru = "sound/larging_up_full_crew.wav"
press = "sound/press_it_dont_distress_it.wav"
vuvuzela = "sound/vuvuzela.wav"
wake = "sound/wake_the_town.wav"
yeahh = "sound/yeaah.wav"
bliss = "sound/musical_bliss.wav"
taking = "sound/taking_you_through.wav"
yeahCAP = "sound/yeaahCAP.wav"
deeper = "sound/deeper_and_darker_we_go.wav"
fiesta = "sound/fiesta.wav"

#2001
dave = "sound/dave.wav"
silly = "sound/silly.wav"
sure = "sound/sure.wav"
cantdo = "sound/cantdo.wav"

# FastShow
scorchio = "sound/scorchio.wav"
winchester = "sound/winchester.wav"
waddle = "sound/chriswaddle.wav"

def paused():
    artist = pytify.getCurrentArtist()
    if artist == "None":
		return True
    else:
		return False


class SpotifyJabberControlBot(JabberBot):



			
    @botcmd
    def playlists(self, mess, args):
	"""will return the current availabe playlists"""
        playlist = "80's Power Ballads: http://open.spotify.com/user/luke2442/playlist/0mlVYECc4C0GmdsaQqr2Wx \n\
                    81 Leonard Street: http://open.spotify.com/user/luke2442/playlist/3Fux7kQ4bI23ka2n1M5xfB \n\
                    "
        return playlist
                    
    @botcmd
    def veto(self, mess, args):
        """Will veto the currently playing track"""
        print "veto", mess.getFrom().getStripped().lower()
        pytify.playpause()
        speech.say("veto")
        pytify.next()
        return "Phew..."
		
    @botcmd
    def reload(self, mess, args):
        """Will restart the currently playing track"""
        print "reload", mess.getFrom().getStripped().lower()
        winsound.PlaySound(rewind, winsound.SND_ALIAS|winsound.SND_ASYNC)
        pytify.playpause()
        pytify.previous()
        time.sleep(1)
        pytify.playpause()
        return "Bound to the bound bound..."
		
    @botcmd	
    def fiesta(self, mess, args):
        """Special Request"""
        print "fiesta", mess.getFrom().getStripped().lower()
        if paused() == False:
            winsound.PlaySound(fiesta, winsound.SND_ALIAS|winsound.SND_ASYNC)
            pytify.playpause()
            time.sleep(13)
            pytify.playpause()
            return "Come with the music!"
        else:
            winsound.PlaySound(fiesta, winsound.SND_ALIAS|winsound.SND_ASYNC)
            return "Come with the music!"
		    
    @botcmd
    def mute(self, mess, args):
        """Will mute / unmute spotfiy"""    
        pytify.mute()   
    
    @botcmd
    def playing(self, mess, args):  
	"""will tell you the currently playing artist and track"""
        artist = pytify.getCurrentArtist()
        track = pytify.getCurrentTrack()
        something = "Now playing %s by %s" % (track, artist)
        return something



    @botcmd
    def volume(self, mess, args):
        """Followed by up or down then a number 1 - 500 will turn volume up/down accordingly"""
        print "volume", mess.getFrom().getStripped().lower()
        if args.split(' ')[0] == "up": updown = "up"
        elif args.split(' ')[0] == "down": updown = "down" 
        else: return "Please try again. Example: volume up 250"
        if args.split(' ')[1]:
            try:
                times = int(args.split(' ')[1])
                if times >= 1 and times <= 500:
                    while times > 0:
                        if updown == "down": pytify.volumeDown()
                        elif updown == "up": pytify.volumeUp() 
                        times -= 1
                    return_string = "Volume turned %s by %s" % (updown, args.split(' ')[1])
                    return return_string
                else:
                    if updown == "down": pytify.volumeDown() 
                    elif updown == "up": pytify.volumeUp() 
            except:
                if updown == "down": pytify.volumeDown() 
                elif updown == "up": pytify.volumeUp() 
                return "Volume turned %s" % updown
        else:
            if updown == "down": pytify.volumeDown() 
            elif updown == "up": pytify.volumeUp() 
            return "Volume turned %s" % updownpytify.volumeDown()
	    
    @botcmd
    def eagle(self, mess, args):
		"""slow volume increase over two minutes"""
		print "eagle", mess.getFrom().getStripped().lower()
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
		time.sleep(10)
		pytify.volumeUp()
	
	

    @botcmd
    def playpause(self, mess, args):
        """Plays if paused. Pauses if playing"""
        pytify.playpause()
        return False

    @botcmd
    def computer(self, mess, args):
		"""????"""
		if 'say' in args.lower():
			pytify.playpause()
			new_string = args.lower().replace("say", '')
			speech.say(new_string)
			pytify.playpause()
		else:
			return "I didn't understand that command"
	    
	   
	   
    @botcmd
    def unsuitable(self, mess, args):
		"""lets the audience know why you've skipped the track. syntax: 'unsuitable because: your reason'"""
		if 'because' in args.lower():
			pytify.playpause()
			new_string = args.lower().replace("because", '')
			speech.say(new_string)
			pytify.next()
			return str('This track is unsuitable because it is'+new_string)
	    
    @botcmd
    def klaxon(self, mess, args):
		"""?"""
		print "klaxon", mess.getFrom().getStripped().lower()
		winsound.PlaySound(klaxon, winsound.SND_ALIAS|winsound.SND_ASYNC)
		return "BIG TUNE"
    @botcmd	
    def scorchio(self, mess, args):
		"""nuffsaid"""
		print "scorchio", mess.getFrom().getStripped().lower()
		winsound.PlaySound(scorchio, winsound.SND_ALIAS|winsound.SND_ASYNC)
		return "Paula mit de neus meteirlogicos"

    @botcmd	
    def winchester(self, mess, args):
		"""Hi"""
		print "Hi Ed!", mess.getFrom().getStripped().lower()
		winsound.PlaySound(winchester, winsound.SND_ALIAS|winsound.SND_ASYNC)
		return "Hi Ed!"

    @botcmd	
    def waddle(self, mess, args):
		"""?"""
		print "waddle", mess.getFrom().getStripped().lower()
		winsound.PlaySound(waddle, winsound.SND_ALIAS|winsound.SND_ASYNC)
		return "Chris"
		
    @botcmd
    def sb(self, mess, args):
		"""soundboard: keys z-m and d-h return badman mc vocal chops"""
		if args.lower() == 'z':
			winsound.PlaySound(boomsound, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'x':
			winsound.PlaySound(hot, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'c':
			winsound.PlaySound(hlisten, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'v':
			winsound.PlaySound(roll, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'g':
			winsound.PlaySound(wake, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'n':
			winsound.PlaySound(yeah, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'm':
			winsound.PlaySound(you_what, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'f':
			winsound.PlaySound(flexin, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'd':
			winsound.PlaySound(cru, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'h':
			winsound.PlaySound(waistline, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'b':
			winsound.PlaySound(press, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'y':
			winsound.PlaySound(yeahCAP, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'k':
			winsound.PlaySound(bliss, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'j':
			winsound.PlaySound(taking, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'l':
			winsound.PlaySound(deeper, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'u':
			winsound.PlaySound(yeahh, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'q':
			winsound.PlaySound(fiesta, winsound.SND_ALIAS|winsound.SND_ASYNC)

		else:
			return "use keys z-m, d-h"

    @botcmd
    def space(self, mess, args):
		"""Top quotes from the Kubrick Masterpiece, follow with 'dave', 'sure', 'silly' or 'cantdo'"""
		if args.lower() == 'dave':
			winsound.PlaySound(dave, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'sure':
			winsound.PlaySound(sure, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'silly':
			winsound.PlaySound(silly, winsound.SND_ALIAS|winsound.SND_ASYNC)
		elif args.lower() == 'cantdo':
			winsound.PlaySound(cantdo, winsound.SND_ALIAS|winsound.SND_ASYNC)
		else:
			return "Accepted args: dave, sure, silly, cantdo"

#    @botcmd
#    def vuvuzela(self, mess, args):
#		"""go or stop"""
#		print "vuvuzela", mess.getFrom().getStripped().lower()
#		if args.lower() == 'go':
#			winsound.PlaySound(vuvuzela, winsound.SND_ALIAS|winsound.SND_ASYNC)
		
    @botcmd
    def purge(self, mess, args):
		winsound.PlaySound(vuvuzela, winsound.SND_ALIAS|winsound.SND_PURGE)
		
    @botcmd
    def log():
		return "not complete"

    @botcmd
    def selecta(self, mess, args):
        """Opens any web link you like and pauses the music"""
        new_string = args.strip()
        webbrowser.open_new(new_string)
        if paused() == False:
            pytify.playpause()
        else:
            return "Bo!"
		
		
username = 'your@user.com'
password = 'yourpass'
server = 'talk.google.com'

pytify = Spotify()
bot = SpotifyJabberControlBot(username,password)
bot.serve_forever()
