#!/usr/bin/python

import math
import fileinput

def fuelForMassWithFuel(mass):
    initFuel = fuelForMass(mass)
    addFuel = fuelForMass(initFuel)
    while addFuel > 0:
        initFuel += addFuel
        addFuel = fuelForMass(addFuel)
    return initFuel


def fuelForMass(mass):
    return max(0,math.floor(mass / 3) - 2)

totFuel = 0
for line in fileinput.input():
    fuel = fuelForMassWithFuel(int(line))
    totFuel += fuel
    print(fuel)
print("Total: {}".format(totFuel))
    

