# -*- coding: utf-8 -*-


# BLE Scan software
# shiu 2014/11/26

import blescan2 as blescan
import sys
import datetime
import locale
import time
import bluetooth._bluetooth as bluez
from operator import itemgetter, attrgetter

# for bluez ---------------------------------------
dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)
#--------------------------------------------------

# debug mode
dbg = False


MAJOR = u'1'
MIN_RSSI = -60
INTERVAL_IN_SEC = 1
UUID_TRIM_LENGTH = -4
SORT_ITEM = 2 #minor

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


while True:

    # Init every sec.
    timeNow = time.time()

    if (timeNow - timeOld) > INTERVAL_IN_SEC and len(udids) > 0:
        timeOld = timeNow

        # Dont print at first Time
        if not firstFlg:

            # now
            st = datetime.datetime.today().strftime(u'%Y/%m/%d %H:%M:%S')

            # Make output string
            beacons = []
            for i in range(0, len(udids)):
                beacons = udids[i], majors[i], minors[i], recieveCounts[i], rssiAves[i]
                beacons.append(beaconTuple)

            bu = sorted(beacons, key=itemgetter(SORT_ITEM))

            nearBeaconCount = 0
            for i in range(0, len(bu)):
                if bu[i][4] > MIN_RSSI:
                    st += dlmt1
                    st += bu[i][0][UUID_TRIM_LENGTH:] + dlmt2
                    st += u'{0:04x}'.format(int(bu[i][1])) + dlmt2
                    st += u'{0:04x}'.format(int(bu[i][2])) + dlmt2
                    st += u'{0:.2f}'.format(bu[i][4])
                    nearBeaconCount += 1
            if nearBeaconCount > 0:
                print(st)

        # for the first time
        else:
            # now
            st = u'#'
            st += u'Date Time' + dlmt1
            st += u'Num' + dlmt1
            st += u'UDID' + dlmt2
            st += u'MOINOR' + dlmt2
            st += u'RSSI' + dlmt1
            st += u'Log Started at ' + dlmt1
            st += datetime.datetime.today().strftime(u'%Y/%m/%d %H:%M:%S')
            print(st)

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
                    print(st2)
                # --------------

