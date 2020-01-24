#coding:utf-8

import sys
import binascii
import textwrap
import re

class CommandTuplesForBytes(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

class push_command(object):
    def __init__(self, bloc_bytes=4, inc_assembly=0):
        '''
        The __init__ function has
        only one argument. __init__(self)
        '''
        self.argument_command = sys.argv[1]
        self.bloc_bytes       = bloc_bytes

    def __convert_testing__(self):
        '''
            The purpose of this function is to
            test arguments and parameters. __convert_testing__(self)
        '''
        if(len(self.argument_command) < 4):
            raise CommandTuplesForBytes("The string must measure at least 4 bytes.")

        self.wrapper_argument_output = textwrap.wrap(self.argument_command, 4)
        self.index_list_argument     = []

        for loop_wrapper_argument in self.wrapper_argument_output[::-1]:
            '''
                This loop allows you to invert the list and
                also find the last slash in the list. 
            '''
            if("/" in loop_wrapper_argument): # CHECK IN VAR NAME !
                loop_wrapper_argument = self.index_list_argument.append(self.wrapper_argument_output.index(loop_wrapper_argument))

        for loop_command_argument in self.wrapper_argument_output:
            '''
                In this loop it allows you to put the
                slashes in the right place in the argument in loop_command_argument.
            '''

            if(len(loop_command_argument) == 3):
                loop_command_argument = self.wrapper_argument_output[self.index_list_argument[0]].split("/")
                loop_command_argument = "//".join(loop_command_argument)

            elif(len(loop_command_argument) == 2):
                loop_command_argument = self.wrapper_argument_output[self.index_list_argument[0]].split("/")
                loop_command_argument = "///".join(loop_command_argument)

            elif(len(loop_command_argument) == 1):
                loop_command_argument = self.wrapper_argument_output[self.index_list_argument[0]].split("/")
                loop_command_argument = "////".join(loop_command_argument)

        self.wrapper_argument_output[self.index_list_argument[0]] = loop_command_argument    
        self.wrapper_argument_output = "".join(self.wrapper_argument_output)

        for loop_command_list_finaly in textwrap.wrap(self.wrapper_argument_output, 4):
            '''
                This loop makes it possible to
                recover the 4 block bytes in loop_command_list_finaly.
            '''
            loop_command_lists_finaly = loop_command_list_finaly.encode('hex')
            print("push 0x%s ; %s" %(loop_command_lists_finaly, loop_command_list_finaly))

if __name__ == "__main__":
    q = push_command()
    q.__convert_testing__()
