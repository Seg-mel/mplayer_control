#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
from functools import partial
from player_property import property_dict
from player_cmdlist import cmdlist_dict

FIFO = u'/tmp/segmplayer_fifo'
AUDIO_OUTPUT = u'alsa'
COMMAND = u'mplayer -ao %s -slave -quiet -idle -input file=%s'
STDOUT = u'/tmp/segmplayer_stdout'
CMDLIST_COMMAND = 'mplayer -input cmdlist'




class Player(object):
    ''' MPlayer control class '''

    def _getter(self, item):
        ## Getter for property
        return item

    def _setter(self, value):
        ## Getter for property
        print value

    def __new__(cls):
        def _doc_creator(item):
            ## Doc creator
            if item['property'] is True:
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
            else:
                ## Doc creator for command
                doc_info  = item['comment']
                args_info = ''
                for key in item.keys():
                    if key == 'command': continue
                    args_info += '\n%s: %s' % (key, item[key])
                doc = '%s%s' % (doc_info, args_info)
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

    def __init__(self, fifo=FIFO, stdout=STDOUT):
        self.fifo = fifo
        self.stdout = stdout
        if os.path.exists(fifo):
            ## delete fifo file if existed it
            os.unlink(fifo)
        ## create fifo file
        os.mkfifo(fifo)
        ## set start flag
        self.start_player = False

    def run_player(self, output=AUDIO_OUTPUT, volume_control='master'):
        """ Run and configure the player """
        run_command = COMMAND % (output, self.fifo)
        run_command_list = run_command.split()
        self.progress_log_write = open(self.stdout,'w+b')
        subprocess.Popen(run_command_list, 
                         stdin=self.progress_log_write, 
                         stdout=self.progress_log_write)
        self.mplayer_client = open(self.fifo,'w')
        self.progress_log = open(self.stdout,'r')
        if volume_control=='master':
            self.send_command('use_master\n')
        else:
            pass





if __name__=='__main__':
    player = Player()
    # print help(player)
    # #print len(dir(player))
    # print player.audio_bitrate
    # print player.stream_pos
    # player.stream_pos = 123
    # print player.stream_pos
