from jabberbot import JabberBot, botcmd
from pytify import Spotify
import speech
import datetime
import logging
logging.basicConfig()
import sys
import os
import re
import sys
import thread
import subprocess
from datetime import datetime
import pickle
import sqlite3
from datetime import datetime

class UserManager(object):
    def get_user_real_name(self, email):
        values = (email, )
        cursor.execute("SELECT * FROM users WHERE email=?", values)
        return cursor.fetchone()[1]

    def add_user(self, name, email):
        values = (name, email)
        cursor.execute("INSERT INTO users VALUES (null, ?, ?, 0, 0)", values)
        cursor.execute("SELECT * FROM users WHERE name=? and email=?", values)
        result = cursor.fetchone()
        conn.commit()
        return result

    def get_user(self, email):
        values = (email, )
        cursor.execute("SELECT * FROM users WHERE email=?", values)
        return cursor.fetchone()
    
    def add_veto(self, email):
        values = (email, )
        cursor.execute("SELECT * FROM users WHERE email=?", values)
        result = cursor.fetchone()
        if result:
            veto_count = result[3] + 1
            update = (veto_count, result[0])
            cursor.execute("UPDATE users SET veto_total=? WHERE id=?", update)
            conn.commit()

            track_values = (1, 1)            
            track_values = (pytify.getCurrentArtist(), pytify.getCurrentTrack())
            cursor.execute("SELECT * FROM playlist WHERE artist=? and title=?", track_values)
            track = cursor.fetchone()
            if track:
                vetoes_values = (result[0], track[0], datetime.now())
                cursor.execute("INSERT INTO vetoes VALUES (null, ?, ?, ?)", vetoes_values)
                conn.commit()
            else:
                cursor.execute("INSERT INTO playlist VALUES (null, ?, ?, 0)", track_values)
                conn.commit()
                cursor.execute("SELECT * FROM playlist WHERE artist=? and title=?", track_values)
                track_add = cursor.fetchone()
                if track_add:
                    vetoes_values = (result[0], track_add[0], datetime.now())
                    cursor.execute("INSERT INTO vetoes VALUES (null, ?, ?, ?)", vetoes_values)
                    conn.commit()
            #return "Song vetoed. %s has used their veto a total %s times" % (result[1], veto_count)
            return "%s used their veto." % (result[1])
        else:
            return "Unsuccessful in registering the veto in the database"

class VetoTableManager(object):
    def get_vetoes(self):
        cursor.execute("SELECT * FROM vetoes INNER JOIN users ON vetoes.user_id=users.id")
##        results = cursor.fetchall()
##        for result in results:
##            print result        
        return cursor.fetchall()

    def get_last_veto(self):
##        cursor.execute("SELECT users.name, vetoes.veto_time FROM vetoes INNER JOIN users ON vetoes.user_id=users.id ORDER BY vetoes.id DESC LIMIT 1")
##        name, date_time = cursor.fetchone()
##        cursor.execute("SELECT playlist.artist, playlist.title FROM vetoes JOIN playlist ON vetoes.playlist_id=playlist.id")
##        try:
##            artist, track = cursor.fetchone()
##        except:
##            artist, track = None, None

        cursor.execute("SELECT users.name, playlist.artist, playlist.title, vetoes.veto_time FROM users, playlist, vetoes WHERE vetoes.user_id=users.id AND vetoes.playlist_id=playlist.id ORDER BY vetoes.id DESC LIMIT 1")
        name, artist, track, date_time = cursor.fetchone()
        
        return "%s by %s was vetoed by %s at %s" % (track, artist, name, date_time.strftime('%Y-%m-%d %H:%M:%S'))
        


class SpotifyJabberControlBot(JabberBot):
    @botcmd
    def playlists(self, mess, args):
        playlist = "80's Power Ballads: http://open.spotify.com/user/luke2442/playlist/0mlVYECc4C0GmdsaQqr2Wx \n\
                    81 Leonard Street: http://open.spotify.com/user/luke2442/playlist/3Fux7kQ4bI23ka2n1M5xfB \n\
                    "
        return playlist
                    
    @botcmd
    def veto(self, mess, args):
        """Will veto the currently playing track"""
        print mess.getFrom().getStripped().lower()
        registered = usermanager.get_user_real_name(mess.getFrom().getStripped().lower())
        
        if registered:
            vetoed = usermanager.add_veto(mess.getFrom().getStripped().lower())
            if vetoed:
                pytify.playpause()
                speech.say(vetoed)
##            self.broadcast("Veto! %s vetoed: %s by %s" % (mess.getFrom().getStripped().lower(), pytify.getCurrentTrack(), pytify.getCurrentArtist()))
                pytify.next()
                return "Vetoed"
            else:
                return "You already vetoed a song today!"
        else:
            return "You are not authorised to use this system"
			
	def reload(self, mess, args):
		"""Will reload the currently playing track"""
		print mess.getFrom().getStripped().lower()
        pytify.playpause()
        speech.say("Bound to the reload!")
##      self.broadcast("Veto! %s vetoed: %s by %s" % (mess.getFrom().getStripped().lower(), pytify.getCurrentTrack(), pytify.getCurrentArtist()))
        pytify.previous()
        return "Reloaded"

    @botcmd
    def lastveto(self, mess, args):
        """Show what was veteod and by whom"""    
        registered = usermanager.get_user_real_name(mess.getFrom().getStripped().lower())
        if registered:
            return vetomanager.get_last_veto()
        else:
            return "You are not authorised to use this system"
    
    @botcmd
    def mute(self, mess, args):
        """Will mute / unmute spotfiy"""
        registered = usermanager.get_user_real_name(mess.getFrom().getStripped().lower())
        if registered:        
            pytify.mute()   
            return False
        else:
            return "You are not authorised to use this system"
    
    @botcmd
    def playing(self, mess, args):
        """Returns what is playing"""
        registered = usermanager.get_user_real_name(mess.getFrom().getStripped().lower())
        if registered:        
            artist = pytify.getCurrentArtist()
            track = pytify.getCurrentTrack()
            something = "Now playing %s by %s" % (track, artist)
            return something
        else:
            return "You are not authorised to use this system"            

    @botcmd
    def volume(self, mess, args):
        """Followed by up or down then a number 1 - 500 will turn volume up/down accordingly"""
        registered = usermanager.get_user_real_name(mess.getFrom().getStripped().lower())
        if registered:
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
        else:
            return "You are not authorised to use this system"

    @botcmd
    def playpause(self, mess, args):
        """Plays if paused. Pauses if playing"""
        registered = usermanager.get_user_real_name(mess.getFrom().getStripped().lower())
        if registered:        
            pytify.playpause()
            return False
        else:
            return "You are not authorised to use this system"

    @botcmd(hidden=True)
    def add(self, mess, args):
        print mess, args
        registered = usermanager.get_user_real_name(mess.getFrom().getStripped().lower())
        if registered:
            args_split = args.split(' ')
            if args_split[0].lower() == 'user':
                name = args_split[1] + " " + args_split[2]
                email = args_split[3]
                added =usermanager.add_user(name, email)
                print added
                return "Added: %s - %s" % (added[1], added[2])
        else:
            return "You are not authorised to use this system"
    @botcmd(hidden=True)
    def computer(self, mess, args):
        if 'i order you to say' in args.lower():
            pytify.playpause()
            new_string = args.lower().replace("i order you to say", '')
            speech.say(new_string)
            pytify.playpause()
        else:
            return "I didn't understand that command"


conn = sqlite3.connect("spotify.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()

username = 'jar.spotify@gmail.com'
password = 'jarhead01'

usermanager = UserManager()
vetomanager = VetoTableManager()
pytify = Spotify()
bot = SpotifyJabberControlBot(username,password)
bot.serve_forever()
