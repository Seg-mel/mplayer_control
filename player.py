#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
from functools import partial
from player_property import property_dict

FIFO = u'/tmp/segmplayer_fifo'
AUDIO_OUTPUT = u'alsa'
COMMAND = u'mplayer -ao %s -slave -quiet -idle -input file=%s'
STDOUT = u'/tmp/segmplayer_stdout'




class Player(object):
    ''' MPlayer control class '''

    def _getter(self, item):
        ## Getter for property
        return self._x

    def _setter(self, value):
        ## Getter for property
        print value

    def __new__(cls):
        def _doc_creator(item):
            ## Doc creator for property
            if item['comment'] == '':
                doc_info = item['command']
            else:
                doc_info  = item['comment']
            if item['set'] is False:
                set_info = '\n(read-only property)'
            else:
                set_info = ''
            if item['min'] is False:
                min_info = ''
            else:
                min_info = '\nmin:\t%s' % item['min']
            if item['max'] is False:
                max_info = ''
            else:
                max_info = '\nmax:\t%s' % item['max']
            type_info = 'type:\t%s' % item['type']
            doc  = '%s\n%s%s%s%s' % (doc_info, type_info, min_info, 
                                           max_info, set_info)
            return doc

        ## Create new class properties from mplayer property_dict
        for item in property_dict.keys():
            doc = _doc_creator(property_dict[item])
            if property_dict[item]['set'] is True:
                ## Create property with set capacity
                x = property(fget=partial(cls._getter, 
                                          item=property_dict[item]), 
                             fset=cls._setter, 
                             doc=doc)
            elif property_dict[item]['set'] is False:
                ## Create property without set capacity
                x = property(fget=partial(cls._getter, 
                                          item=property_dict[item]),
                             doc=doc)
            setattr(cls, item, x)
        return super(Player, cls).__new__(cls)

    def __init__(self):
        self._x = 'asd'
        pass

    def run_player(self):
        pass





if __name__=='__main__':
    player = Player()
    print help(player)
    #print len(dir(player))
    print player.audio_bitrate
    print player.stream_pos
    player.stream_pos = 123
    print player.stream_pos
