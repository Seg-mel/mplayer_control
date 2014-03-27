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
    FIFO_PATH = '/Users/meloman/Desktop/segmplayer.fifo'
    STDOUT_PATH = '/Users/meloman/Desktop/segmplayer.stdout'
    MPLAYER_PATH = '/mplayer/mplayer.exe'
elif 'linux' in sys.platform:
    FIFO_PATH = '/tmp/segmplayer.fifo'
    STDOUT_PATH = '/tmp/segmplayer.stdout'
    MPLAYER_PATH = 'mplayer'



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
        ## Get answer from stdout file
        command_string = 'pausing_keep get_property %s' % item['command']
        self._send_command(command_string)
        answer = ''
        # Skipping line what not is answer(and other garbage)
        while len(answer.split('=')) != 2 :
            answer = self._player_answer.readline()
        print 'EXECUTED GET PROPERTY:', item['command'], answer
        return answer.split('=')[-1][:-1]

    def _setter(self, args, item):
        ## Setter for property

        def type_test(arg):
            ## Type test function
            basic_type = item['type']
            gotten_type = str(type(arg))
            if basic_type not in gotten_type:
                # Permit for setting integer arg in float arg
                if (basic_type == 'float') and ('int' in gotten_type):
                    pass
                # Type test for flag type
                elif ('int' in gotten_type) and (basic_type == 'flag'):
                    if (arg != 0) and (arg != 1):
                        error_string = 'the value must be 0 or 1'
                        raise ValueError(error_string)
                # Test for other types
                else:
                    error_string = "wrong type of input arg for '%s = <%s>'" %\
                                    (item['command'], item['type'])
                    raise TypeError(error_string)

        # Count args test
        if type(args) is tuple:
            args_length = len(args)
            error_string = "property '%s' takes exactly 1 arguments (%d given)"
            raise TypeError(error_string % (item['command'], args_length))
        # Type test
        type_test(args)
        # Min/max test
        if (item['min'] is not False) and (args < item['min']):
            error_string = "the value must be min=%d"
            raise ValueError(error_string % item['min'])
        if (item['max'] is not False) and (args > item['max']):
            error_string = "the value must be max=%d"
            raise ValueError(error_string % item['max'])
        # Sending the command
        command_string = 'pausing_keep set_property %s %s' %\
                                                   (item['command'], str(args))
        self._send_command(command_string)
        print 'EXECUTED SET PROPERTY:', item['command'], args

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

        # Create new class properties from mplayer property_dict
        for item in property_dict.keys():
            doc = _doc_creator(property_dict[item])
            if property_dict[item]['set'] is True:
                # Create property with set capacity
                prop = property(fget=partial(cls._getter, 
                                             item=property_dict[item]), 
                                fset=partial(cls._setter, 
                                             item=property_dict[item]),
                                doc=doc)
            elif property_dict[item]['set'] is False:
                # Create property without set capacity
                prop = property(fget=partial(cls._getter, 
                                             item=property_dict[item]),
                                doc=doc)
            setattr(cls, item, prop)
        return super(Properties, cls).__new__(cls)

    def __init__(self, fifofile=None, stdout=None):
        self._fifo = fifofile
        self._player_answer = stdout

    def _send_command(self, command):
        ## Write command in fifo file
        command += '\n'
        self._fifo.write(command)
        self._fifo.flush()



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

    properties = Properties

    def _new_get_method(self):
        ## Get answer method from stdout file
        command_string = 'pausing_keep %s' % item['command']
        self._send_command(command_string)
        answer = ''
        # Skipping line what not is answer(and other garbage)
        while len(answer.split('=')) != 2 :
            answer = self._player_answer.readline()
        print 'EXECUTED GET COMMAND:', item['command'], answer
        return answer.split('=')[-1][:-1]

    def _new_simple_method(self):
        ## Write mplayer command without an answer and arguments
        command_string = '%s' % item['command']
        print 'EXECUTED SIMPLE COMMAND:', command_string
        self._send_command(command_string)

    def _new_args_method(self, *args):
        ## Write mplayer command with arguments

        def get_args_error_string():
            ## Return error string for args type error
            args_string = ''
            for t in item['types']:
                args_string += ('<%s>, ' % t)
            error_string = 'wrong types of input args in %s(%s)' % \
                            (item['command'],args_string[:-2])
            return error_string

        def get_count_args_error_string():
            ## Return error string for args count error
            error_string = '%s() takes exactly %d arguments (%d given)' % \
                            (item['command'], count_args_types, count_args)
            return error_string

        def type_test(num, arg):
            ## Type test function
            basic_type = item['types'][num]
            gotten_type = str(type(arg))
            # print basic_type, gotten_type , arg
            if basic_type not in gotten_type:
                # Permit for setting integer arg in float arg
                if (basic_type == 'float') and ('int' in gotten_type):
                    pass
                else:
                    # self._send_command('quit')
                    raise TypeError(get_args_error_string())

        # For single value, because it is not a tuple
        if type(args) is not tuple:
            args = (args,)
        count_args = len(args)
        count_args_types = len(item['types'])
        # Test count input args
        if count_args <= count_args_types:
            command_string = item['command']
            # Append command string
            for num, value in enumerate(args):
                # Test on type
                type_test(num, value)
                # Create command string
                command_string += ' %s' % str(value)
            print 'EXECUTED VALUES COMMAND:', command_string
            # Sending the command
            self._send_command(command_string)
        else:
            # self._send_command('quit')
            raise TypeError(get_count_args_error_string())

    def __new__(cls, *args, **kwargs):

        def _doc_creator(item):
            ## Doc creator for command
            doc_info  = item['comment']
            py_command = item['pycommand']
            doc = '%s\n%s' % (py_command, doc_info)
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
                    new_method = FunctionType(cls._new_args_method.func_code, 
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

    def __init__(self, mplayer=MPLAYER_PATH, fifo=FIFO_PATH, 
                                                           stdout=STDOUT_PATH):
        # Reassigning class property 'properties'.
        # This operation is need for normal help of this class 
        self.properties = self.properties()
        # Only linux at this time...
        mplayer_slave_command = mplayer + ' -slave -quiet -idle -input file=%s'
        if os.path.exists(fifo):
            os.unlink(fifo)
        os.mkfifo(fifo) 
        self._stdout = open(stdout, 'w+b')
        command = (mplayer_slave_command % fifo).split()
        subprocess.Popen(command, stdout=self._stdout)
        self._fifo = open(fifo, 'w')
        self._player_answer = open(stdout, 'r')
        # Fifo and stdout passing to properties  class
        self.properties.__init__(self._fifo, self._player_answer)

    def _send_command(self, command):
        ## Write command in fifo file
        command += '\n'
        self._fifo.write(command)
        self._fifo.flush()



if __name__=='__main__':
    player = Player()
    # print help(player)
    player.loadfile("/home/meloman/data/tmp/audiotest/3_Door_Down_-_Here_Without_You.mp3")
    # player.loadfile("/home/meloman/data/tmp/audiotest/8march.ogg")
    # player.use_master()
    # player.volume(100)
    for i in range(101):
        time.sleep(0.1)
        player.properties.volume = i
    # a = 1
    # while a==1:
    #     time.sleep(1)
    #     print '~'*79
        # player.get_percent_pos()
        # player.get_time_pos()
        # player.get_time_length()
        # player.get_file_name()
        # player.get_meta_title()
        # player.properties.volume
        # player.properties.audio_bitrate
        # player.properties.channels
        # player.properties.length
        # player.properties.percent_pos
        # player.properties.stream_length