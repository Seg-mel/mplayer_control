#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
from pprint import pformat



class DictGenerator(object):
    """ Command list ditionary generator  """

    def __init__(self):
        self.txt_file = open(os.path.join(os.curdir,
                             'mplayer_cmdlist.txt'), 'r').readlines()

    def get_cmd_dict(self):
        """ Convert txt file to python dictionary """
        cmds_dict = {}
        for line in self.txt_file:
            line_dict = {}
            line_dict['property'] = False
            line_dict['comment'] = line[0:-1]
            list_line = line.split()
            line_dict['command'] = list_line[0]
            for num, item in enumerate(list_line):
                if num == 0: continue
                if '[' in item:
                    item = item[1:-1]
                line_dict['arg%d'%num] = item
            cmds_dict[list_line[0]] = line_dict
        print cmds_dict
        return cmds_dict

    def run(self):
        """ Run generation """
        output_prop_file = open(os.path.join(os.curdir,
                                'player_cmdlist.py'), 'w')
        text = 'cmdlist_dict = %s'
        output_prop_file.write(text % pformat(self.get_cmd_dict()))
        output_prop_file.close()



if __name__ == '__main__':
    DG = DictGenerator()
    #DG.get_cmd_dict()
    DG.run()