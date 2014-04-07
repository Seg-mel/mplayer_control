#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Example module
# Copyright (C) 2014 Musikhin Andrey <melomansegfault@gmail.com>

import atexit
import time
from player import Player, MPLAYER_PATH, STDOUT_PATH, PIPE_PATH, PID_PATH



class ExamplePlayer(object):
    """Example Player class"""

    def __init__(self, *arg):
        super(ExamplePlayer, self).__init__()
        # Initializing the player
        player = Player(mplayer=MPLAYER_PATH, pipe=PIPE_PATH, 
                        stdout=STDOUT_PATH, pid=PID_PATH, debug=False)
        # Adding the '-nolirc' option to the mplayer start command
        player.add_command_option(option='-nolirc')
        # Adding the 'equalizer' audio filter to the mplayer start command
        player.add_command_option(option='-af', 
                                value='equalizer=-5:-5:-5:8:8:8:-5:-5:-12:-12')
        # Create new mplayer process
        player.create_new_process()
        atexit.register(player.process.terminate)
        # Print process name
        print 'PROCESS NAME: ', player.process.name
        # Print process pid
        print 'PROCESS PID: ', player.process.pid
        # Print help text for Player class and it's properties
        print help(player)
        print help(player.properties)
        # Call 'loadfile' command
        player.loadfile("/home/user/music/sound.ogg") # For Unix
        # player.loadfile("C:\music\sound.ogg") # For Windows
        # Edit equalizer filter
        player.af_cmdline('equalizer', '0:0:0:0:0:0:0:0:0:0')
        for i in range(11):
            time.sleep(0.5)
            print '~'*79
            # Get an answer using commands
            print player.get_percent_pos()
            print player.get_time_pos()
            print player.get_time_length()
            print player.get_file_name()
            print player.get_meta_title()
            # Get an answer using properties
            print player.properties.volume
            print player.properties.audio_bitrate
            print player.properties.channels
            print player.properties.length
            print player.properties.percent_pos
            print player.properties.stream_length
            # Set player properties
            player.properties.volume = i*10
        time.sleep(2)
        # Unloadi equalizer filter
        player.af_del('equalizer')

        # Connection to the existing process (Only Unix)
        # player.connect_to_process()
        # print player.get_percent_pos()
        # print player.get_time_pos()
        # time.sleep(1)

        # Kill mplayer process
        player.quit()



if __name__ == '__main__':
    example_player = ExamplePlayer()