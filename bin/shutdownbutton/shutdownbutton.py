#!/usr/bin/env python2.7

import RPi.GPIO as GPIO
import time
import syslog
import os

WatchPinNo = 21
LivePinNo = 20
shutdownFlg = 0
SleepStepSec = 0.01
ON = 1
OFF = 0
Second = 0
TimeShutdown = 0.3
TimeReboot = 0.05


def InitGpio():
    GPIO.setmode(GPIO.BCM)

    # GPIO 21 set up as input. It is pulled
    # up to stop false signals
    GPIO.setup(WatchPinNo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # GPIO 20 set up as output.
    GPIO.setup(LivePinNo, GPIO.OUT)

    # event
    GPIO.add_event_detect(WatchPinNo, GPIO.RISING)
    GPIO.add_event_callback(WatchPinNo, my_callback_one)


# def KeepWatchForSeconds(seconds):
#     GoFlag = True
#     LEDState = False
#     if seconds < 1:
#         seconds = 1
#     while seconds > 0:
#         LEDState = not LEDState
#         GPIO.output(LEDGpioNo, LEDState)
#         time.sleep(SleepStepSec)
#         seconds -= SleepStepSec
#         if (GPIO.input(WatchPinNo) == True):
#             GoFlag = False
#             break
#     return GoFlag

def Init():
    InitGpio()

def LivePin(state):
    GPIO.output(LivePinNo, state)

def my_callback_one(WatchPinNo):
    Second = 0

    while True:
        time.sleep(SleepStepSec)
        Second += SleepStepSec

        if GPIO.input(WatchPinNo) == False:
            break


    if Second > TimeShutdown:
        shutdown()
    elif Second > TimeReboot:
        reboot()

#    print (Second)
    return Second

def reboot():
#    print ('reboot')
    syslog.syslog(syslog.LOG_NOTICE, "Going shutdown by GPIO.")
    os.system("/sbin/shutdown -r now '\nREBOOT REBOOT REBOOT REBOOT REBOOT REBOOT\n\nR E B O O T             by shutdownbutton\n\nREBOOT REBOOT REBOOT REBOOT REBOOT REBOOT\n\n'")

def shutdown():
#    print ('shutdown')
    syslog.syslog(syslog.LOG_NOTICE, "Going shutdown by GPIO.")
    os.system("/sbin/shutdown -h now '\nSHUTDOWN SHUTDOWN SHUTDOWN SHUTDOWN SHUTDOWN\n\nS H U T D O W N            by shutdownbutton\n\nSHUTDOWN SHUTDOWN SHUTDOWN SHUTDOWN SHUTDOWN\n\n'")




if __name__ == '__main__':
    Init()
    LivePin(ON)

    try:
        while True:
            if shutdownFlg == 1:
                break

        GPIO.cleanup() # clean up GPIO on normal exit

    except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
