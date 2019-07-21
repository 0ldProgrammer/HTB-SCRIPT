#coding:utf-8
# @Author: 0xEX75
# @Date:   01/05/19
# @Last Modified by: 0xEX75

import os as m_remote_command
import sys
import time

class m_remote(object):
    def __init__(self, packet_send="cmd /k echo ", allow_check=True):
        '''
            So this function will find the 
            password on the mremoteng software __init__()
        '''
        self.__packet_send = packet_send + sys.argv[1]
        self.__allow       = allow_check

    def execute_function(self):
        '''
            So this function will execute
            the command to have the password __execute_function__()
        '''
        if(self.__packet_send):
            m_remote_command.system(self.__packet_send)
        sys.exit(1)

if __name__ == "__main__":
    remote = m_remote()
    remote.execute_function()
