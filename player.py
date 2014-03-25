#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import pipes
from functools import partial
from types import FunctionType
from player_property import property_dict
from player_cmdlist import cmdlist_dict

if 'win' in sys.platform:
    PIPE_PATH = '/Users/meloman/Desktop/segmplayer.fifo'
    STDOUT_PATH = '/Users/meloman/Desktop/segmplayer.stdout'
    MPLAYER_PATH = '/mplayer/mplayer.exe'
elif 'linux' in sys.platform:
    PIPE_PATH = '/tmp/segmplayer.fifo'
    STDOUT_PATH = '/tmp/segmplayer.stdout'
    MPLAYER_PATH = 'mplayer'
# COMMAND = MPLAYER_PATH + ' -ao %s -slave -quiet -idle -input file=%s'
COMMAND = MPLAYER_PATH + ' -slave -quiet -idle -input file=%s'



class CountValuesError(Exception):
        ''' 
        Exception class, when user passed more values 
        than needed.
        '''
        def __init__(self, count):
            self.count = count

        def __str__(self):
            string = 'Too many values. max=%s' % self.count
            return string



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
                prop = property(fget=partial(cls._getter, 
                                          item=property_dict[item]), 
                             fset=cls._setter, 
                             doc=doc)
            elif property_dict[item]['set'] is False:
                ## Create property without set capacity
                prop = property(fget=partial(cls._getter, 
                                          item=property_dict[item]),
                             doc=doc)
            setattr(cls, item, prop)
        return super(Properties, cls).__new__(cls)

    def __init__(self, fifofile=None, stdout=None):
        pass



class Player(object):
    '''
    MPlayer control class.
    ~~~~~~~~~~~~~~~~~~~~~

    Commands 'get_property', 'set_property' and 'set_property_osd', 
    which included into MPlayer cmdlist,
    have been replaced on 'properties',
    that is the properies class.
    Example: 
        Player().properties.volume
        Player().properties.volume = 10
    For getting more documetetion of properties you can use
    the command 'help(Player.properies)'
    '''

    properties = Properties(fifofile=PIPE_PATH, stdout=STDOUT_PATH)

    def _new_get_method(self):
        pass

    def _new_simple_method(self):
        command_string = '%s\n' % item['command']
        print command_string
        self._fifo.write(command_string)
        self._fifo.flush()

    def _new_values_method(self, *values):
        ## Getter for command
        # For single value, because it is not a tuple
        if type(values) is not tuple:
            values = (values,)
        count_values = len(values)
        count_args = len(item['types'])
        # Test count input values
        if count_values <= count_args:
            command_string = item['command']
            # Append command string
            for num, value in enumerate(values):
                # Test on type
                basic_type = item['types'][num]
                gotten_type = str(type(value))
                print basic_type, gotten_type
                if basic_type not in gotten_type:
                    # Permit for setting integer value in float value
                    if (basic_type == 'float') and ('int' in gotten_type):
                        pass
                    else:
                        self._fifo.write('quit\n')
                        self._fifo.flush()
                        raise TypeError
                command_string += ' %s' % str(value)
            command_string += '\n'
            print command_string
            self._fifo.write(command_string)
            self._fifo.flush()
        else:
            self._fifo.write('quit\n')
            self._fifo.flush()
            raise CountValuesError(count=count_args)

    def __new__(cls, *args, **kwargs):
        def _doc_creator(item):
            ## Doc creator for command
            doc_info  = item['comment']
            args_info = ''
            for key in item.keys():
                if key == 'command': continue
                if key == 'comment': continue
                if key == 'property': continue
                args_info += '\n%s: %s' % (key, item[key])
            doc = '%s%s' % (doc_info, args_info)
            return doc

        ## Create new class methods from mplayer cmdlist_dict
        for item in cmdlist_dict.keys():
            if item == 'get_property': continue
            if item == 'set_property': continue
            if item == 'set_property_osd': continue
            doc = _doc_creator(cmdlist_dict[item])
            # Creating a dictionary that would include variables contained
            # it item and globals() (excluding locals()). 
            # This is necessary for passing it to a new method.
            method_dict = {'item': cmdlist_dict[item]}
            for i in globals().keys():
                if i in locals().keys(): continue
                method_dict[i] = globals()[i]
            # Creating function
            if 'get' not in item:
                if len(cmdlist_dict[item]['types']) != 0:
                    # If the list of types containes types
                    new_method = FunctionType(cls._new_values_method.func_code, 
                                              method_dict,
                                              item)
                else:
                    # If the list of types is empty
                    new_method = FunctionType(cls._new_simple_method.func_code,
                                              method_dict,
                                              item)
            else:
                new_method = FunctionType(cls._new_get_method.func_code,
                                          method_dict,
                                          item)
            # Adding doc, editing name
            new_method.__doc__ = doc 
            new_method.__name__ = item
            # Adding function to this class as method
            setattr(cls, item, new_method)
        return super(Player, cls).__new__(cls)

    def __init__(self):
        fifo_template = pipes.Template()
        fifo_open = fifo_template.open(PIPE_PATH, 'w')
        self._stdout = open(STDOUT_PATH, 'w')
        command = (COMMAND % PIPE_PATH).split()
        subprocess.Popen(command, stdout=self._stdout)
        self._fifo = open(PIPE_PATH, 'w')
        # load_file_command = "loadfile '%s' 1\n" % ("/Users/meloman/Dropbox/music/my/7class.mp3")
        # load_file_command = "loadfile '%s'\n" % ("/home/meloman/data/tmp/audiotest/3_Door_Down_-_Here_Without_You.mp3") 
        # print load_file_command
        # self._fifo = open(PIPE_PATH, 'w')
        # self._fifo.write(load_file_command)
        # self._fifo.flush()




if __name__=='__main__':
    player = Player()
    print help(player)
    # player.loadfile("/home/meloman/data/tmp/audiotest/3_Door_Down_-_Here_Without_You.mp3",1)
    # player.volume(0)
    # player.use_master()
