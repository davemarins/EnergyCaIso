import re
import csv
import requests
from scipy.interpolate import interp1d
from scipy.integrate import quad

# acquisition or elaboration
acquisition = False
# from 1/8/2018 to 31/7/2019
max_days = [31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31]
days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
'17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
months = ['08', '09', '10', '11', '12', '01', '02', '03', '04', '05', '06', '07']
years = ['2018', '2018', '2018', '2018', '2018', '2019', '2019', '2019', '2019', '2019', '2019', '2019']
ascending_number = 1566717234700

max_power_grid = -1
max_power_grid_date = ""
min_power_grid = 999999999999
min_power_grid_date = ""

max_energy_grid = -1
max_energy_grid_date = ""
min_energy_grid = 999999999999
min_energy_grid_date = ""

yearly_energy = 0

for i in range(12):
    monthly_energy = 0
    min_power_grid_month = 999999999999
    min_power_grid_month_date = ""
    for j in range(max_days[i]):
        date = years[i] + months[i] + days[j]
        if acquisition == True:
            url = "http://www.caiso.com/outlook/SP/History/" + date + "/demand.csv?_=" + str(ascending_number)
            ascending_number += 1
            reply = requests.get(url=url)
            if reply.status_code == 200:
                content = reply.content.decode('utf-8')
                file_name = date + '.csv'
                open(file_name, 'a').write(content)
                print("Acquisition of " + date + ".csv completed")
            else:
                print("Error request in " + date + ".csv acquisition")
                print("Status code is " + reply.status_code)
        else:
            X = []
            Y = []
            row_number = 0
            min_power_grid_local = 999999999999
            max_power_grid_local = -1
            start_time = False
            file_name = 'data/' + date + '.csv'
            file = open(file_name)
            csv_reader = csv.reader(file, delimiter=',')
            header = True
            for row in csv_reader:
                row_number += 1
                if header == True:
                    header = False
                else:
                    if start_time == True and row[0] == "00:00":
                        continue
                    time = row[0]
                    try:
                        demand = int(row[3])
                        if min_power_grid > demand:
                            min_power_grid = demand
                            min_power_grid_date = date
                        if max_power_grid < demand:
                            max_power_grid = demand
                            max_power_grid_date = date
                        if min_power_grid_local > demand:
                            min_power_grid_local = demand
                        if max_power_grid_local < demand:
                            max_power_grid_local = demand
                        if min_power_grid_month > demand:
                            min_power_grid_month = demand
                            min_power_grid_month_date = date
                    except ValueError:
                        print("demand = int(row[3]) did not contain a number in date " + date + " at row " + str(row_number))
                    if time == "00:00":
                        start_time = True
                    hour_value = time.split(':')
                    hour = hour_value[0]
                    minute = hour_value[1]
                    to_append = float(hour) + float(minute)/60
                    X.append(to_append)
                    Y.append(int(demand))
            print("Power demand between " + str(min_power_grid_local) + " and " + str(max_power_grid_local) + " MW")
            f = interp1d(X, Y, kind='cubic')
            energy = quad(f, 0, 23.83)[0]
            monthly_energy += energy
            yearly_energy += energy
            if max_energy_grid < energy:
                max_energy_grid = energy
                max_energy_grid_date = date
            if min_energy_grid > energy:
                min_energy_grid = energy
                min_energy_grid_date = date
            print("Daily energy request for " + date + " : " + str(energy) + " MWh")
    print("Monthly min power demand for month number " + months[i] + " " + str(min_power_grid_month) + " MW at date " + min_power_grid_month_date)
    reactors_power = int(min_power_grid_month/1660)
    print("Required reactors for min power: " + str(reactors_power) + " with power of " + str(reactors_power*1660) + " MW")
    print("Monthly energy demand for month number " + months[i] + " " + str(monthly_energy))
print("Power demand between " + str(min_power_grid) + " and " + str(max_power_grid) + " MW")
print("Min power demand global " + str(min_power_grid) + " in date " + min_power_grid_date)
print("Max power demand global " + str(max_power_grid) + " in date " + max_power_grid_date)
print("Min energy demand global " + str(min_energy_grid) + " in date " + min_energy_grid_date)
print("Max energy demand global " + str(max_energy_grid) + " in date " + max_energy_grid_date)
print("Total energy demand for the year considered: " + str(yearly_energy) + " MWh")