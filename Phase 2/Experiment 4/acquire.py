import RPi.GPIO as pi
from time import sleep, localtime
import usbtmc as u
import adafruit_dht
from board import D12
import serial

first = (2, 3, 4, 17, 27)

second = (14, 15, 18, 23, 24)

devices = u.list_devices()
dev = u.Instrument(devices[0])
dht = adafruit_dht.DHT11(D12)

com = serial.Serial("/dev/ttyACM0", 9600)
com.flush()

def vol_curr_read(device):

    device.write("meas:res? auto")
    sleep(1)
    res = device.read()
    res = res[11:]
    res = float(res)
    return  res

def switch(num, rpi = pi, device = dev, dht = dht):
    sleep(2)
    plant = open('plant{}.csv'.format(num), 'a')
    resistance = vol_curr_read(device)
    t = localtime()
    try:
     h, temp = (dht.humidity, dht.temperature)
    except RuntimeError:
     h, temp = (None, None)
    rpi.output(21, rpi.HIGH)
    voc = com.readline().decode('utf-8').replace("\n", "").replace(' ', ',')
    rpi.output(21, rpi.LOW)
    clock = '{0}:{1}:{2}'.format(t.tm_hour, t.tm_min, t.tm_sec)
    date = '{0}/{1}/{2}'.format(t.tm_mday, t.tm_mon, t.tm_year)
    plant.write('{0}, {1}, {2}, {3}, {4}, {5} \n'.format(date, clock, h, temp, resistance, voc))
    with open("voc.csv", 'a') as v:
        v.write(f"{date}, {clock}, {voc}")  # Capture the VOC data from MQ3s
    print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(plant.name, date, clock, h, temp, resistance, voc))
    plant.close()
try:
	while True:
		pi.setmode(pi.BCM)
		pi.setup(21, pi.OUT)
		pi.setup(16, pi.OUT)
		pi.output(21, pi.LOW)
		pi.output(16, pi.HIGH)
		
		for k in first + second :
			pi.setup(k, pi.OUT)
			pi.output(k, pi.HIGH)
		for i, val_first in enumerate(first):
			pi.output(val_first, pi.LOW)

			for j, val_second in enumerate(second):
				pi.output(val_second, pi.LOW)
				sleep(1)
				switch(5 * i + j + 1)
				pi.output(val_second, pi.HIGH)
			pi.output(val_first, pi.HIGH)
			sleep(0.5)

		pi.cleanup()

except KeyboardInterrupt:
	print('CTRL + C was pressed, aborting!!!')
	for k in first + second:
		pi.output(k, pi.HIGH)
		pi.cleanup()
		
		
