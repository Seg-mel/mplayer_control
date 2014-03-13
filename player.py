#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
from player_property import property_dict

FIFO = u'/tmp/segmplayer_fifo'
AUDIO_OUTPUT = u'alsa'
COMMAND = u'mplayer -ao %s -slave -quiet -idle -input file=%s'
STDOUT = u'/tmp/segmplayer_stdout'




class Player(object):
    ''' Player class '''
    def __init__(self):
        pass



if __name__=='__main__':
    pass
