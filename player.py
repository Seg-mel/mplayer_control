#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Player module
# Copyright (C) 2014 Musikhin Andrey <melomansegfault@gmail.com>

import os
import sys
from subprocess import PIPE
from psutil import Process, Popen, pid_exists
from tempfile import gettempdir
from functools import partial
from types import FunctionType
from player_properties import property_dict
from generators import CmdDictGenerator

# Constants
PLATFORM = sys.platform
if 'win' in PLATFORM:
    MPLAYER_PATH = 'C:\mplayer\mplayer.exe'
    PIPE_PATH = ''
elif 'linux' in PLATFORM:
    MPLAYER_PATH = 'mplayer'
    PIPE_PATH = os.path.join(gettempdir(), 'mplayer.pipe')
STDOUT_PATH = os.path.join(gettempdir(), 'mplayer.stdout')
PID_PATH = os.path.join(gettempdir(), 'mplayer.pid')



class Properties(object):
    '''
    MPlayer properties class.
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This class is an abstraction for all MPlayer properties. 
    It sets and gets the corresponding properties using MPlayer commands get_property and set_property.
    Example of a raw MPlayer command: get_property volume
    '''

    def _getter(self, item):
        '''
        Getter for the property.
        Gets an answer from stdout file
        '''
        command_string = 'pausing_keep get_property %s' % item['command']
        self._send_command(command_string)
        answer = ''
        # Skipping a line that is not an answer (and other garbage)
        while len(answer.split('=')) != 2 :
            answer = self._player_answer.readline()
        if self._debug: 
            print 'EXECUTED GET PROPERTY:', item['command'], answer[:-1]
        return answer.split('=')[-1][:-1]

    def _setter(self, args, item):
        ''' Setter for the property '''

        def type_test(arg):
            ## Type test function
            basic_type = item['type']
            gotten_type = str(type(arg))
            if basic_type not in gotten_type:
                # Allow passing integer arg in place of float arg
                if (basic_type == 'float') and ('int' in gotten_type):
                    pass
                # Test for flag type
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
            error_string = "property '%s' takes exactly 1 argument (%d given)"
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
        if self._debug: print 'EXECUTED SET PROPERTY:', item['command'], args

    def __new__(cls, *args, **kwargs):

        def _doc_creator(item):
            ## Doc creator for the property
            if item['comment'] == '':
                # doc_info = item['command']
                doc_info = ''
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

        # Creating new class properties from mplayer property_dict
        for item in property_dict.keys():
            doc = _doc_creator(property_dict[item])
            if property_dict[item]['set'] is True:
                # Creating property with set capacity
                prop = property(fget=partial(cls._getter,
                                             item=property_dict[item]),
                                fset=partial(cls._setter,
                                             item=property_dict[item]),
                                doc=doc)
            elif property_dict[item]['set'] is False:
                # Creating property without set capacity
                prop = property(fget=partial(cls._getter,
                                             item=property_dict[item]),
                                doc=doc)
            setattr(cls, item, prop)
        return super(Properties, cls).__new__(cls)

    def __init__(self, pipe=None, stdout=None, debug=False):
        self._pipe = pipe
        self._player_answer = stdout
        self._debug = debug

    def _send_command(self, command):
        ''' Sends command to the pipe '''
        command += '\n'
        self._pipe.write(command)
        self._pipe.flush()



class Player(object):
    '''
    MPlayer control class.
    ~~~~~~~~~~~~~~~~~~~~~

    This class includes methods with the same names that MPlayer commands have.
    Example:
        Player().get_percent_pos()
        Player().loadfile('/home/user/music/sound.ogg')
    To get more detailed manual on commands you can use the command:
        help(Player())
    or the console command:
        mplayer -input cmdlist
    or the official documentation:
        http://www.mplayerhq.hu/DOCS/man/en/mplayer.1.html

    Commands 'get_property' and 'set_property', included in MPlayer 
    cmdlist, have been replaced with 'Properties' class.
    Example:
        Player().properties.volume
        Player().properties.volume = 10
    To get more detailed manual on properties you can use the command:
        help(Player().properies)
    '''

    @property
    def process(self):
        ''' 
        The MPlayer process.
        For more detailed manual check out the 
        documentation of psutil.Process(pid)
        (https://code.google.com/p/psutil/wiki/Documentation#Classes)
         '''
        return self._process

    def _new_get_method(self):
        ''' Getting answer method from stdout file '''
        command_string = 'pausing_keep %s' % item['command']
        self._send_command(command_string)
        answer = ''
        # Skipping a line that is not an answer(and other garbage)
        while len(answer.split('=')) != 2 :
            answer = self._player_answer.readline()
        if self._debug: 
            print 'EXECUTED GET COMMAND:', item['command'], answer[:-1]
        return answer.split('=')[-1][:-1]

    def _new_simple_method(self):
        ''' Writing mplayer command without the answer and arguments '''
        command_string = '%s' % item['command']
        if self._debug: print 'EXECUTED SIMPLE COMMAND:', command_string
        self._send_command(command_string)

    def _new_args_method(self, *args):
        ''' Writing mplayer command with arguments '''

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
                # Allow passing integer arg in place of float arg
                if (basic_type == 'float') and ('int' in gotten_type):
                    pass
                else:
                    raise TypeError(get_args_error_string())

        # For single value, because it is not a tuple
        if type(args) is not tuple:
            args = (args,)
        count_args = len(args)
        count_args_types = len(item['types'])
        # Testing count input args
        if count_args <= count_args_types:
            command_string = item['command']
            # Appending command to the string
            for num, value in enumerate(args):
                # Testing the type
                type_test(num, value)
                # Creating a command string
                command_string += ' %s' % str(value)
            if self._debug: print 'EXECUTED ARGS COMMAND:', command_string
            # Sending the command
            self._send_command(command_string)
        else:
            # self._send_command('quit')
            raise TypeError(get_count_args_error_string())

    def __new__(cls, mplayer=MPLAYER_PATH, pipe=PIPE_PATH, 
                     stdout=STDOUT_PATH, pid=PID_PATH, debug=False):

        def _doc_creator(item):
            ## Doc creator for the command
            doc_info  = item['comment']
            py_command = item['pycommand']
            doc = '%s\n%s' % (py_command, doc_info)
            return doc

        ## Creating new class methods from mplayer cmdlist_dict
        cmdlist_dict = CmdDictGenerator(mplayer).get_cmdlist()
        for item in cmdlist_dict.keys():
            if item == 'get_property': continue
            if item == 'set_property': continue
            #if item == 'set_property_osd': continue
            doc = _doc_creator(cmdlist_dict[item])
            # Creating a dictionary that would include variables from 
            # item and globals() (excluding locals()).
            # This is necessary for passing it to a new method.
            method_dict = {'item': cmdlist_dict[item]}
            for i in globals().keys():
                if i in locals().keys(): continue
                method_dict[i] = globals()[i]
            # Creating a function
            if 'get' not in item:
                if len(cmdlist_dict[item]['types']) != 0:
                    # If list of types contains some types
                    new_method = FunctionType(cls._new_args_method.func_code,
                                              method_dict,
                                              item)
                else:
                    # If list of types is empty
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
            # Adding function to this class as a method
            setattr(cls, item, new_method)
        # Create 'properties' property and 
        # making it use the doc from Properties class
        properties_class = Properties()
        def get_properties(self):
            return properties_class
        properties = property(fget=get_properties, 
                              doc=Properties.__doc__)
        setattr(cls, 'properties', properties)
        return super(Player, cls).__new__(cls)

    def __init__(self, mplayer=MPLAYER_PATH, pipe=PIPE_PATH, 
                       stdout=STDOUT_PATH, pid=PID_PATH, debug=False):
        self._command = [mplayer, '-slave', '-quiet', '-idle']
        self._pipe_path = pipe
        self._stdout_path = stdout
        self._pid_path = pid
        self._debug = debug
        self._pid = None
        self._process = None

    def _send_command(self, command):
        ''' Sending command to the pipe '''
        command += '\n'
        self._pipe.write(command)
        self._pipe.flush()

    def create_new_process(self):
        ''' Creating a new process '''
        if 'win' in PLATFORM:
            self._stdout = open(self._stdout_path, 'w+b')
            self._process = Popen(args=self._command,
                                  stdin=PIPE,
                                  stdout=self._stdout)
            self._pipe = self._process.stdin
        else:
            if os.path.exists(self._pipe_path):
                os.unlink(self._pipe_path)
            os.mkfifo(self._pipe_path)
            self._pipe = open(self._pipe_path, 'w+b')
            if os.path.exists(self._stdout_path):
                os.remove(self._stdout_path)
            self._stdout = open(self._stdout_path, 'w+b')
            self._process = Popen(args=self._command,
                                  stdin=self._pipe,
                                  stdout=self._stdout)
        self._player_answer = open(self._stdout_path, 'r')
        self._pid = self._process.pid
        # Writing pid to file
        pid_file = open(self._pid_path, 'w')
        pid_file.write(str(self._pid))
        pid_file.close()
        # Passing pipe and stdout to properties class
        self.properties.__init__(self._pipe, self._player_answer, self._debug)

    def connect_to_process(self):
        ''' 
        Connect to the existing process of mplayer.
        For example, if your GUI has crashed, 
        but the mplayer continues to play.
        (Only Unix)
        '''
        try:
            pid_file = open(self._pid_path, 'r')
            self._pid = int(pid_file.readline())
            pid_file.close()
        except: self._pid = None
        if (self._pid is not None) and (pid_exists(self._pid)):
            if self._debug: print 'PROCESS EXISTS'
            self._process = Process(self._pid)
            self._pipe = open(self._pipe_path, 'w+b')
            self._player_answer = open(self._stdout_path, 'r')
            self._player_answer.readlines()
            self.properties.__init__(self._pipe, self._player_answer, 
                                                                   self._debug)
        else:
            if self._debug: print 'PROCESS DOES NOT EXISTS'
            self._process = None

    def add_command_option(self, option, value=None):
        ''' Add an option to the mplayer start command list '''
        self._command.append(option)
        if value is not None:
            self._command.append(value)
        if self._debug: 
            print 'START MPLAYER COMMAND IS UPDATED: %s' %\
                                                        ' '.join(self._command)

    def send_raw_command(self, string):
        """ Sending a raw command """
        self._send_command(command=string)



if __name__=='__main__':
    player = Player()
    print help(player)
    print help(player.properties)