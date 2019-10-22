import datetime
import signal
import sys
import threading
import time
import mysql.connector

next_call = time.time()
cnx = 0


def foo():
    next_call = time.time()
    while True:
        tempProcess()
        next_call = next_call + 60
        time.sleep(next_call - time.time())


def tempProcess():
    global cnx
    #tFile = open('/sys/class/thermal/thermal_zone0/temp')
    tFile = open('/Users/vir/PycharmProjects/tempsensor/tempRaw')
    temp = float(tFile.read())
    tempC = temp / 1000
    if not cnx.is_connected():
        connectToDB()
    mycursor = cnx.cursor()
    sql = 'INSERT INTO `temperature`.`currentTemp` (`id`, `temp`, `station`, `date`) VALUES (NULL, %s, %s, %s);'
    val = (str(tempC), 'rassensor', str(datetime.datetime.now()))
    mycursor.execute(sql, val)
    cnx.commit()
    print("[" + str(datetime.datetime.now()) + "] Current temp: " + str(tempC))
    sys.stdout.flush()


def connectToDB():
    global cnx
    while True:
        try:
            cnx = mysql.connector.connect(user='root', password='temp',
                                  host='192.168.1.110', port='3306',
                                  database='temperature')

            break

        except:
            print("["+ str(datetime.datetime.now())+ "] MYSQL Connection Error, Retrying in 60s...")
            sys.stdout.flush()
            time.sleep(60)


if __name__ == "__main__":
    print("[" + str(datetime.datetime.now()) + "] Starting Application\n--------------\n")
    connectToDB()
    timerThread = threading.Thread(target=foo)
    timerThread.daemon = True
    timerThread.start()
    sys.stdout.flush()
    while True:
        try:
            signal.signal(signal.SIGINT, signal.default_int_handler)
        except:
            cnx.close()
            print("[" + str(datetime.datetime.now()) + "] Stopping application\n------------\n")
            sys.stdout.flush()
            sys.exit()
