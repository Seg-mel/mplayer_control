#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Test module
# Copyright (C) 2014 Musikhin Andrey <melomansegfault@gmail.com>

import atexit
import time
from player import Player, MPLAYER_PATH, STDOUT_PATH, PIPE_PATH, PID_PATH



class TestPlayer(object):
    """Test Player class"""

    def __init__(self, *arg):
        super(TestPlayer, self).__init__()
        # Initializing the player
        player = Player(mplayer=MPLAYER_PATH, pipe=PIPE_PATH, 
                        stdout=STDOUT_PATH, pid=PID_PATH, debug=False)
        # # Adding the option to the start mplayer command
        # player.add_command_option(option='-nolirc')
        # Adding the '-nolirc' option to the start mplayer command
        player.add_command_option(option='-nolirc')
        # Adding the 'equalizer' audio filter to the start mplayer command
        player.add_command_option(option='-af', 
                                value='equalizer=-5:-5:-5:8:8:8:-5:-5:-12:-12')
        # Creating a new mplayer process
        player.create_new_process()
        atexit.register(player.process.terminate)
        # Print process name
        print 'PROCESS NAME: ', player.process.name
        # Print process pid
        print 'PROCESS PID: ', player.process.pid
        # Print help text for Player class and it's properties
        print help(player)
        print help(player.properties)
        # Setting the 'loadfile' command
        player.loadfile("/home/user/music/sound.ogg") # For Unix
        # player.loadfile("C:\music\sound.ogg") # For Windows
        # Editing the equalizer filter
        player.af_cmdline('equalizer', '0:0:0:0:0:0:0:0:0:0')
        for i in range(11):
            time.sleep(0.5)
            print '~'*79
            # Getting the answer by using commands
            print player.get_percent_pos()
            print player.get_time_pos()
            print player.get_time_length()
            print player.get_file_name()
            print player.get_meta_title()
            # Getting the answer by using properties
            print player.properties.volume
            print player.properties.audio_bitrate
            print player.properties.channels
            print player.properties.length
            print player.properties.percent_pos
            print player.properties.stream_length
            # Setting properties of player
            player.properties.volume = i*10
        time.sleep(2)
        # Unloading the equalizer filter
        player.af_del('equalizer')

        # Connection to existing process (Only Unix)
        # player.connect_to_process()
        # print player.get_percent_pos()
        # print player.get_time_pos()
        # time.sleep(1)

        # Killing process
        player.quit()



if __name__ == '__main__':
    test_player = TestPlayer()