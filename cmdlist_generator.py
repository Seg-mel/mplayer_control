#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Cmdlist Generator module
# Copyright (C) 2014 Musikhin Andrey <melomansegfault@gmail.com>

import os
from subprocess import Popen, PIPE
from pprint import pformat



class CmdDictGenerator(object):
    """ Command list ditionary generator  """

    def __init__(self, mplayer='mplayer'):
        self._cmdlist = [line for line in Popen(
                      [mplayer, '-input', 'cmdlist'], stdout=PIPE).stdout][:-1]
        self._doc_file = open(os.path.join(os.curdir, 
                             'data/mplayer_cmdlist_docs.txt'), 'r').readlines()
        self._cmdlist_dict = {}

    def _get_cmd_dict(self):
        """ Convert txt file to python dictionary """
        # Creating the comments dictionary
        doc_string = 'MPlayer doc:\n'
        doc_key = ''
        doc_dict = {}
        for line in self._doc_file:
            if line == '\n':
                doc_dict[doc_key] = doc_string
                doc_string = 'MPlayer doc: '
                continue
            if line[0] == ' ':
                doc_string += line[5:]
            else: 
                doc_key = line.strip().split(' ')[0]
                doc_string += line
        # Creating the command dictionary
        cmds_dict = {}
        for line in self._cmdlist:
            line_dict = {}
            list_line = line.split()
            line_dict['command'] = list_line[0]
            if list_line[0] not in doc_dict.keys():
                line_dict['comment'] = self._new_cpt(line)[0]
                line_dict['pycommand'] = self._new_cpt(line)[1]
                line_dict['types'] = self._new_cpt(line)[2]
            else:
                line_dict['comment'] = '%s\n%s' % (self._new_cpt(line)[0],
                                                   doc_dict[list_line[0]])
                line_dict['pycommand'] = self._new_cpt(line)[1]
                line_dict['types'] = self._new_cpt(line)[2]
            cmds_dict[list_line[0]] = line_dict
        self._cmdlist_dict = cmds_dict

    def _new_cpt(self, comment):
        """ 
        Return new comment, python comment and type list 
        from comment line 
        """
        comment_list =  comment.split()
        _comment = ' '.join(comment_list)
        types = []
        _python_comment = ''
        for num, item in enumerate(comment_list[1:]):
            if 'Integer' in item:
                string = 'int'
            elif 'String' in item:
                string = 'str'
            elif 'Float' in item:
                string = 'float'
            else: pass
            types.append(string)
            if '[' in item and num!=0: 
                string = '[, <%s>]' % string
            elif '[' in item and num==0: 
                string = '[<%s>]' % string
            elif num != 0: string  = ', <%s>' % string
            elif num == 0: string = '<%s>' % string 
            _python_comment += string
        new_comment = 'MPlayer command: %s' % _comment
        python_comment = '%s(%s)' % (comment_list[0], _python_comment)
        return [new_comment, python_comment, types]

    def get_cmdlist(self):
        self._get_cmd_dict()
        return self._cmdlist_dict

    # def run(self):
    #     """ Run generation """
    #     output_prop_file = open(os.path.join(os.curdir,
    #                             'player_cmdlist.py'), 'w')
    #     text = 'cmdlist_dict = %s'
    #     output_prop_file.write(text % pformat(self._get_cmd_dict()))
    #     output_prop_file.close()



if __name__ == '__main__':
    DG = CmdDictGenerator()
    print pformat(DG.get_cmdlist())