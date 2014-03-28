#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
from player import Player



class TestPlayer(object):
    """Test Player class"""

    def __init__(self, *arg):
        super(TestPlayer, self).__init__()
        player = Player()
        # Look at the help for Player and Properties classes
        print help(player)
        print help(player.properties)
        # Setting the 'loadfile' command
        # player.loadfile("/home/meloman/data/tmp/audiotest/3_Door_Down_-_Here_Without_You.mp3")
        player.loadfile("/home/meloman/data/tmp/audiotest/8march.ogg")
        for i in range(11):
            time.sleep(0.3)
            print '~'*79
            # Getting the answer by using commands
            player.get_percent_pos()
            player.get_time_pos()
            player.get_time_length()
            player.get_file_name()
            player.get_meta_title()
            # Getting the answer by using properties
            player.properties.volume
            player.properties.audio_bitrate
            player.properties.channels
            player.properties.length
            player.properties.percent_pos
            player.properties.stream_length
            # Setting properties of player
            player.properties.volume = i*10



if __name__ == '__main__':
    test_player = TestPlayer()