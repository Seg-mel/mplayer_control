#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
from pprint import pformat



class DictGenerator(object):
    ''' Генератор словаря свойств mplayer '''
    def __init__(self):
        self.txt_file = open(os.path.join(os.curdir,
                             'mplayer_properties.txt'), 'r').readlines()

    def get_prop_dict(self):
        ''' Метод создания словаря со словарями свойств '''
        def convert_min_max(string):
            # конвертируем значение минимума и максимума
            try:
                if '.' in string:
                    value = float(string)
                    return value
                else:
                    value = int(string)
                    return value
            except: return False
        property_dict = {}
        for line in self.txt_file:
            command = line[:19].strip()
            if command:
                prop_dict = {
                    'command':  command,
                    'type':     line[19:29].strip(),
                    'min':      convert_min_max(line[29:37].strip()),
                    'max':      convert_min_max(line[37:45].strip()),
                    'get':      line[45:49].strip()=='X',
                    'set':      line[49:53].strip()=='X',
                    'step':     line[53:58].strip()=='X',
                    'comment':  line[58:].strip()
                }
            else:
                command = prop_dict['command']
                prop_dict['comment']+= '\n' + line[58:].strip()
            property_dict[command] = prop_dict
        return property_dict

    def run(self):
        ''' Метод запуска генератора '''
        output_prop_file = open(os.path.join(os.curdir,
                                'player_property.py'), 'w')
        text = 'property_dict = %s'
        output_prop_file.write(text % pformat(self.get_prop_dict()))
        output_prop_file.close()



if __name__ == '__main__':
    DG = DictGenerator()
    DG.run()
