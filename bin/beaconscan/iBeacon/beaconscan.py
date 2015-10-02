#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# BLE Scan software
# shiu 2014/11/26

import blescan2 as blescan
import sys
import datetime
import locale
import time
import bluetooth._bluetooth as bluez
import os
import os.path
import ConfigParser
from operator import itemgetter, attrgetter


DEFAULT_INI_FILE_PATH = u'/home/smartuser/etc/default.ini'
INI_FILE_PATH = u''
SAVE_DIR_PATH = u''


MAJOR = u'1'
MIN_RSSI = -60
INTERVAL_IN_SEC = 1
UUID_TRIM_LENGTH = -8
MINOR = 2 #minor

MYNAME = ''
SAVE_INTERVAL = 100

def Init():
    global MYNAME
    MYNAME = os.uname()[1]
    inifile = ConfigParser.SafeConfigParser()
    inifile.read(DEFAULT_INI_FILE_PATH)
    global INI_FILE_PATH
    INI_FILE_PATH = unicode(inifile.get('beaconscan','INI_FILE_PATH'))
    OpenIniFileLocal()

def OpenIniFileLocal():
    global MAJOR
    global MIN_RSSI
    global INTERVAL_IN_SEC
    global UUID_TRIM_LENGTH
    global MINOR
    global SAVE_DIR_PATH
    global SAVE_INTERVAL

    inifile = ConfigParser.SafeConfigParser()
    inifile.read(INI_FILE_PATH)

    MAJOR = unicode(inifile.get("beaconscan","MAJOR"))
    MIN_RSSI =  int(inifile.get("beaconscan","MIN_RSSI"))
    INTERVAL_IN_SEC =  int(inifile.get("beaconscan","INTERVAL_IN_SEC"))
    UUID_TRIM_LENGTH =  int(inifile.get("beaconscan","UUID_TRIM_LENGTH"))
    MINOR = int(inifile.get("beaconscan","MINOR"))
    SAVE_DIR_PATH = unicode(inifile.get("beaconscan","SAVE_DIR_PATH"))
    SAVE_INTERVAL = int(inifile.get("beaconscan","SAVE_INTERVAL"))

def OpenIniFileServer():
    print('beaconscan.OpenIniFileServer:')

def SaveRealTime():
    print('beaconscan.SaveRealTime:')

def SaveDataFile(dateNow, st):
    DataFileName = SAVE_DIR_PATH + dateNow + '_' + MYNAME + '.bs'
    if len(dateNow) > 0:
        if os.path.exists(DataFileName):
            f = open(DataFileName, 'a')
            f.write(st)
            f.close()
        else:
            f = open(DataFileName, 'w')
            f.write(st)
            f.close()


def Read():
    # for bluez ---------------------------------------
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        # print "ble thread started"

    except:
        print "error accessing bluetooth device..."
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    #--------------------------------------------------

    # debug mode
    dbg = False



    udids = []
    majors = []
    rssis = []
    minors = []
    rssiSums = []
    rssiAves = []
    beaconIndexes = []
    recieveCounts = []

    dlmt1 = u'\t'
    dlmt2 = u','
    firstFlg = True

    timeOld = 0
    count = 0
    dateNow = ''
    dateOld = ''

    while True:

        # Init every sec.
        timeNow = time.time()

        if (timeNow - timeOld) > INTERVAL_IN_SEC and len(udids) > 0:
            timeOld = timeNow

            # Dont print at first Time
            if not firstFlg:

                # now
 ##               st = datetime.datetime.today().strftime(u'%Y/%m/%d %H:%M:%S')
                # st = datetime.datetime.today().strftime(u'%Y%m%d%H%M%S')

                dateNow2 = datetime.datetime.today().strftime(u'%H%M%S')
                dateNow = datetime.datetime.today().strftime(u'%Y%m%d')
                count += 1

                print(count)

                if dateOld != dateNow:
                    SaveDataFile(dateOld, st)
                    count = 0
                    st = u''

                if count == SAVE_INTERVAL:
                    SaveDataFile(dateNow, st)
                    count = 0
                    st = u''

                dateOld = dateNow


                # st += dateNow2
                # st += dlmt1
                # st += str(len(udids))

                # Make output string
                ibeacons = []
                for i in range(0, len(udids)):
                    ibeacon = udids[i], majors[i], minors[i], recieveCounts[i], rssiAves[i]
                    ibeacons.append(ibeacon)

                bu = sorted(ibeacons, key=itemgetter(MINOR))

                nearBeaconCount = 0

                for i in range(0, len(bu)):
                    if bu[i][4] > MIN_RSSI:

                        if i == 0:
                            st += dateNow2
                            st += dlmt1
                            st += str(len(udids))

                        st += dlmt1
                        st += bu[i][0][UUID_TRIM_LENGTH:] + dlmt2
                        st += u'{0:x}'.format(int(bu[i][1])) + dlmt2
                        st += u'{0:x}'.format(int(bu[i][2])) + dlmt2
                        st += u'{0:.2f}'.format(bu[i][4])
                        nearBeaconCount += 1
                    else:
                        count = 0
                        st = u''

                if nearBeaconCount > 0:
                    # print(st)
                    st += u'\n'
                else:
                    st = u''



            # for the first time
            else:
 #                # now
                st = u''
 # #               st += u'Date Time' + dlmt1
 # #               st += u'Num' + dlmt1
 # #               st += u'UDID' + dlmt2
 # #               st += u'MOINOR' + dlmt2
 # #               st += u'RSSI' + dlmt1
 #                st += u'Log Started at ' + dlmt1
 #                st += datetime.datetime.today().strftime(u'%Y/%m/%d %H:%M:%S')
 #                # dateNow = datetime.datetime.today().strftime(u'%Y%m%d%H%M')
 #                st += u'\n'
 #                SaveDataFile(dateNow, st)
 #                st = u''
 #                # print(st)

            # init lists
            udids = []
            majors = []
            minors = []
            rssis = []
            rssiSums = []
            rssiAves = []
            beaconIndexes = []
            recieveCounts = []

            firstFlg = False

        # When read iBeacon (Event)
        returnedList = blescan.parse_events(sock, 1)
        for dt in returnedList:
            s = dt.split(',')
            macAddress = str(s[0])
            udid = str(s[1])
            major = str(s[2])
            minor = str(s[3])
            rssi = float(s[4])

            if major == MAJOR:
                if udid not in udids:
                    udids.append(udid)
                    majors.append(major)
                    minors.append(minor)
                    rssis.append(float(rssi))
                    rssiSums.append(float(rssi))
                    rssiAves.append(float(rssi))
                    recieveCounts.append(1)


                else:
                    i = udids.index(udid)
                    rssis[i] = rssi
                    recieveCounts[i] += 1
                    rssiSums[i] += rssis[i]
                    rssiAves[i] = rssiSums[i] / recieveCounts[i]

                    # debug mode ---
                    if dbg:
                        st2 = u'rssis[i] = ' + str(rssis[i]) + u' '
                        st2 += u'rssiSums[i] = ' + str(rssiSums[i]) + u' '
                        st2 += u'recieveCounts[i] = ' + str(recieveCounts[i]) + u' '
                        st2 += u'rssiAves[i] = ' + str(rssiAves[i]) + u' '
                        st2 += u'\n'
                        print(st2)
                    # --------------

if __name__ == '__main__':
    Init()
    Read()
