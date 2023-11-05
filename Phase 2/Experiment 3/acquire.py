import usbtmc as u
from time import sleep, localtime
import RPi.GPIO as pi
import Adafruit_DHT


devices = u.list_devices()
dev = u.Instrument(devices[0])
dht = Adafruit_DHT.DHT11

sig = (2, 3, 14, 15, 18, 17, 27, 22)

def switch2(num, plant):
    pi.output(num, pi.HIGH)
    resistance = vol_curr_read(dev)
    t = localtime()
    clock = '{0}:{1}:{2}'.format(t.tm_hour, t.tm_min, t.tm_sec)
    date = '{0}/{1}/{2}'.format(t.tm_mday, t.tm_mon, t.tm_year)
    plant.write('{0}, {1}, {2} \n'.format(date, clock, resistance))
    print('{0}, {1}, {2}, {3}'.format(plant.name, date, clock, resistance))
    pi.output(num, pi.LOW)

def vol_curr_read(device):

    device.write("meas:res? auto")
    sleep(1)
    res = device.read()
    #res = res.lstrip("#9000000016")
    res = res[11:]
    res = float(res)
    return res

def switch(num, plant, rpi = pi, device = dev, dht = dht):
    sleep(9)
    rpi.output(num, rpi.LOW)
    resistance = vol_curr_read(device)
    t = localtime()
    h, temp = Adafruit_DHT.read(dht, 4)
    clock = '{0}:{1}:{2}'.format(t.tm_hour, t.tm_min, t.tm_sec)
    date = '{0}/{1}/{2}'.format(t.tm_mday, t.tm_mon, t.tm_year)
    plant.write('{0}, {1}, {2}, {3}, {4} \n'.format(date, clock, h, temp, resistance))
    print('{0}, {1}, {2}, {3}, {4}, {5}'.format(plant.name, date, clock, h, temp, resistance))
    rpi.output(num, rpi.HIGH)

try:
    while True:
        pi.setmode(pi.BCM)
        for i in sig:
	        pi.setup(i, pi.OUT)
	        pi.output(i, pi.HIGH)
        plant1 = open('plant1.csv', 'a')  # Data of the first plant will be stored in this file
        plant2 = open('plant2.csv', 'a')  # Similarly data of consecutive plants will be stored in these files
        plant3 = open('plant3.csv', 'a')
        plant4 = open('plant4.csv', 'a')
        plant5 = open('plant5.csv', 'a')
        plant6 = open('plant6.csv', 'a')
        plant7 = open('plant7.csv', 'a')
        plant8 = open('plant8.csv', 'a')
        #plant9 = open('plant9.csv', 'a')
        #plant10 = open('plant10.csv', 'a')
        #plant11 = open('plant11.csv', 'a')
        #plant12 = open('plant12.csv', 'a')
        obj = [plant1, plant2, plant3, plant4, plant5, plant6, plant7, plant8] # [plant10, plant11, plant12]
        sleep(0.5)

        for s, p in zip(sig, obj):
            switch(s, p)
            p.close()
        pi.cleanup()
        
        
except KeyboardInterrupt:
    print('CTRL + C was pressed, aborting!!!')
    for i in sig:
        pi.output(i, pi.HIGH)
