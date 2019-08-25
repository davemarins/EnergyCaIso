from scipy.interpolate import interp1d
from scipy.integrate import quad
import matplotlib.pyplot as plt
import numpy as np
from struct import unpack
import time

def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False

files = ['CAISO-demand-2019-01-01.csv', 'CAISO-demand-2019-07-01.csv']
for file in files:
    X = []
    Y = []
    print('Opening file ' + file)
    with open(file, 'r') as parameterFile:
        firstLine = parameterFile.readline()
        values = firstLine.split(',')
        for value in values:
            if isTimeFormat(value):
                hour_value = value.split(':')
                hour = hour_value[0]
                minute = hour_value[1]
                to_append = float(hour) + float(minute)/60
                X.append(to_append)
        secondLine = parameterFile.readline()
        values = secondLine.split(',')
        for value in values:
            if value.isnumeric():
                Y.append(int(value))
    f = interp1d(X, Y, kind='cubic')
    print("Consumo giornaliero: " + str(quad(f, 0, 23.83)[0]) + " MWh")
    plt.plot(X, Y, 'o', X, f(X), '--')
    plt.legend(['data', 'cubic'], loc='best')
    plt.show()