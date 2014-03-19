#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
from functools import partial
from player_property import property_dict
from player_cmdlist import cmdlist_dict

if 'win' in sys.platform:
    PIPE = '/Windows/Temp/segmplayer.fifo'
    STDOUT = '/Windows/Temp/segmplayer.stdout'
    # AUDIO_OUTPUT = ''
    COMMAND = '/mplayer/mplayer.exe -ao %s -slave -quiet -idle -input file=%s'
elif 'unix' in sys.patform:
    PIPE = '/tmp/segmplayer.fifo'
    STDOUT = '/tmp/segmplayer.stdout'
    # AUDIO_OUTPUT = 'alsa'
    COMMAND = 'mplayer -ao %s -slave -quiet -idle -input file=%s'



class Properties(object):
    ''' 
    MPlayer properties class. 
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This class includes MPlayer properies.
    The class is substitute two MPlayer commands (get_property, set_property)
    plus property.
    Example raw MPlayer query: get_property volume
    '''

    def _getter(self, item):
        ## Getter for property
        return item

    def _setter(self, value):
        ## Getter for property
        print value

    def __new__(cls, *args, **kwargs):
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
        return super(Properties, cls).__new__(cls)

    def __init__(self, fifofile=None, stdout=None):
        pass



class Player(object):
    '''
    MPlayer control class.
    ~~~~~~~~~~~~~~~~~~~~~

    Commands 'get_property', 'set_property' and 'set_property_osd', 
    which include into MPlayer cmdlist,
    have been replaced on 'properties',
    that is the properies class.
    Example: 
        Player().properties.volume
        Player().properties.volume = 10
    For getting more documetetion of properties you can use
    the command 'help(Player().properies)'
    '''

    properties = Properties(fifofile=PIPE, stdout=STDOUT)

    def _getter(self, item):
        ## Getter for command
        return item

    def _setter(self, value):
        ## Getter for command
        print value

    def __new__(cls, *args, **kwargs):
        def _doc_creator(item):
            ## Doc creator for command
            doc_info  = item['comment']
            args_info = ''
            for key in item.keys():
                if key == 'command': continue
                if key == 'comment': continue
                args_info += '\n%s: %s' % (key, item[key])
            doc = '%s%s' % (doc_info, args_info)
            return doc

        ## Create new class properties from mplayer cmdlist_dict
        for item in cmdlist_dict.keys():
            if item == 'get_property': continue
            if item == 'set_property': continue
            if item == 'set_property_osd': continue
            doc = _doc_creator(cmdlist_dict[item])
            if 'get' not in item:
                ## Create property with set capacity
                x = property(fget=partial(cls._getter, 
                                          item=cmdlist_dict[item]), 
                             fset=cls._setter, 
                             doc=doc)
            else:
                ## Create property without set capacity
                x = property(fget=partial(cls._getter, 
                                          item=cmdlist_dict[item]),
                             doc=doc)
            setattr(cls, item, x)
        return super(Player, cls).__new__(cls)

    def __init__(self):
        pass



if __name__=='__main__':
    player = Player()
    print help(player.properties)
    # #print len(dir(player))
    # print player.audio_bitrate
    # print player.stream_pos
    # player.stream_pos = 123
    # print player.stream_pos
