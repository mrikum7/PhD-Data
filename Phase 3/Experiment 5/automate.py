import usbtmc as u
from time import sleep

dev1 = u.Instrument(u.list_devices()[0])
dev2 = u.Instrument(u.list_devices()[1])

l = 0.025
A = 0.0040 ##Values have been taken as an example

file = "again/0-38-2-8.86"

#print("dev1", dev1.ask("*idn?"))
#("dev2", dev2.ask("*idn?"))

with open(f"{file}.csv", 'a') as file:
    for i in range(0, 501, 5):

        volt = i / 100
        dev2.write(":apply ch1,{}".format(volt))
        sleep(1)
        dev1.write(":meas:curr?")
        curr = dev1.read()
        curr = float(curr[11:])
        file.write(f"{volt}, {curr}\n")
        print(f"{volt}, {curr}")

dev2.write(":apply ch1,0")




