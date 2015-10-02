#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import time
import syslog
import os
import os.path
import ConfigParser
import datetime
import sys
import locale

DBG = 1

PROG_NAME = u'exer'
DEFAULT_INI_FILE_PATH = u'/home/smartuser/etc/default.ini'
INI_FILE_PATH = u''
MYNAME = u''
COMMAND_DIR_PATH = u''
COMMAND_FILE_PATH = u''
LOG_DIR_PATH = u''
CHECK_INTERVAL = 5


def Init():
    # get my host name
    global MYNAME
    global FILE_DIR
    global FILE_NAME
    global INI_FILE_PATH
    global COMMAND_FILE_PATH

    MYNAME = os.uname()[1]

    # open ini default ini file
    inifile = ConfigParser.SafeConfigParser()
    inifile.read(DEFAULT_INI_FILE_PATH)

    # get ini file path
    INI_FILE_PATH = unicode(inifile.get(PROG_NAME,'INI_FILE_PATH'))
    OpenIniFileLocal()

    # make FileName
    COMMAND_FILE_PATH = COMMAND_DIR_PATH + MYNAME + u'.exer'

    if DBG == 1:
        print ('Init: COMMAND_FILE_PATH' + COMMAND_FILE_PATH)


def logger(message):
    filePath = LOG_DIR_PATH + MYNAME + u'.exerlog'
    msg = datetime.datetime.today().strftime(u'%Y%m%d%H%M%S') + ': '
    msg += message
    if os.path.exists(filePath):
        f = open(filePath, 'w')
        f.write(msg)
        f.close
    else:
        f = open(filePath, 'a')
        f.write(msg)
        f.close

def OpenIniFileLocal():
    global COMMAND_DIR_PATH
    global CHECK_INTERVAL
    global LOG_DIR_PATH

    inifile = ConfigParser.SafeConfigParser()
    inifile.read(INI_FILE_PATH)

    COMMAND_DIR_PATH =  unicode(inifile.get(PROG_NAME,"COMMAND_DIR_PATH"))
    LOG_DIR_PATH =  unicode(inifile.get(PROG_NAME,"LOG_DIR_PATH"))

    CHECK_INTERVAL =  int(inifile.get(PROG_NAME,"CHECK_INTERVAL"))

    if DBG == 1:
        print ('OpenIniFileLocal: COMMAND_DIR_PATH' + COMMAND_DIR_PATH)
        print ('OpenIniFileLocal: CHECK_INTERVAL' + unicode(CHECK_INTERVAL))
        print ('OpenIniFileLocal: LOG_DIR_PATH' + unicode(LOG_DIR_PATH))


def ExecuteCommand(command):
    try:
        if DBG == 1:
            print ('ExecuteCommand: command = ' + command)
        os.system(command)
        logger('P ' + command)
        return True
    except Exception, e:
        logger('F ' + command)
        return False


def DeleteFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)


def ReadFile(filePath):
    if os.path.exists(filePath):
        f = open(filePath)
        cmds = f.readlines()
        f.close()
        for cmd in cmds:
            ExecuteCommand(cmd)
        DeleteFile(filePath)


if __name__ == '__main__':
    Init()

    try:
        while True:
            ReadFile(COMMAND_FILE_PATH)
            time.sleep(CHECK_INTERVAL)


    except KeyboardInterrupt:
        pass
