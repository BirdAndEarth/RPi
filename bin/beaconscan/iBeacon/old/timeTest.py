import time

timeOld = 0
while True:
    timeNow = time.time()
    if (timeNow - timeOld) > 1:
        timeOld = timeNow
        print("timeNow = " + str(timeNow) + " \n")
