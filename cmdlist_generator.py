#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
from pprint import pformat



class DictGenerator(object):
    """ Command list ditionary generator  """

    def __init__(self):
        self.txt_file = open(os.path.join(os.curdir,
                             'data/mplayer_cmdlist.txt'), 'r').readlines()

    def get_cmd_dict(self):
        """ Convert txt file to python dictionary """
        cmds_dict = {}
        for line in self.txt_file:
            line_dict = {}
            list_line = line.split()
            line_dict['property'] = False
            line_dict['command'] = list_line[0]
            line_dict['comment'], line_dict['pycommand'], line_dict['types'] =\
            self.new_cpt(line)
            cmds_dict[list_line[0]] = line_dict
        print cmds_dict
        return cmds_dict

    def new_cpt(self, comment):
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
            if '[' in item: string = '[, <%s>]' % string
            elif num != 0: string  = ', <%s>' % string
            elif num == 0: string = '<%s>' % string 
            _python_comment += string
        new_comment = 'MPlayer command: %s' % _comment
        python_comment = '%s(%s)' % (comment_list[0], _python_comment)
        return new_comment, python_comment, types

    def run(self):
        """ Run generation """
        output_prop_file = open(os.path.join(os.curdir,
                                'player_cmdlist.py'), 'w')
        text = 'cmdlist_dict = %s'
        output_prop_file.write(text % pformat(self.get_cmd_dict()))
        output_prop_file.close()



if __name__ == '__main__':
    DG = DictGenerator()
    DG.run()