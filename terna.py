import csv
import numpy as np
import time


def find_max(array):
    result = -1
    for value in array:
        if value > result:
            result = value
    return result


def find_min(array):
    result = 999999999
    for value in array:
        if value < result:
            result = value
    return result


def calculate_energy(X, Y, monthly_energy, yearly_energy, header_result, result_file):
    energy = np.trapz(Y, x=X)
    monthly_energy += energy
    yearly_energy += energy
    if header_result:
        result_file.write("Date,Energy [MWh],Min load [MW],Max load [MW]\n")
        header_result = False
    result_file.write(current_date + ',' + str(energy / 1000) + ',' + str(find_min(Y)) + ',' + str(find_max(Y)) + '\n')
    return monthly_energy, yearly_energy, header_result


max_days = [31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30]
days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
        '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
months = ['07', '08', '09', '10', '11', '12', '01', '02', '03', '04', '05', '06']
years = ['2018', '2018', '2018', '2018', '2018', '2018', '2019', '2019', '2019', '2019', '2019', '2019']
# zones = ['north', 'centre-north', 'centre-south', 'south', 'sicilia', 'sardegna']
zones = ['north', 'centre', 'south', 'sicilia', 'sardegna']
dt1 = time.time()

for zone in zones:
    yearly_energy = 0
    min_per_month = []
    max_per_month = []
    for i in range(12):
        file = open('terna/{}/{}-{}.csv'.format(zone, years[i], months[i]), 'r')
        result_file = open('result-numpy/{}/out-{}-{}.csv'.format(zone, years[i], months[i]), 'w')
        csv_reader = csv.reader(file, delimiter=',')
        header = True
        header_result = True
        X = []
        Y = []
        local_monthly_max = -1
        local_monthly_min = 999999999
        monthly_energy = 0
        current_date = None
        for row in csv_reader:
            if header:
                header = False
                continue
            else:
                date_hour = row[0].split(' ')
                if current_date is None:
                    current_date = date_hour[0]
                if date_hour[0] != current_date:
                    monthly_energy, yearly_energy, header_result = calculate_energy(X, Y, monthly_energy, yearly_energy, header_result, result_file)
                    min_per_month.append(local_monthly_min)
                    max_per_month.append(local_monthly_max)
                    X = []
                    Y = []
                    current_date = date_hour[0]
                else:
                    hour = date_hour[1].split(':')
                    temp_value = float(hour[0]) + float(int(hour[1]) / 60)
                    timestamp = float(temp_value)
                    X.append(timestamp)
                    Y.append(float(row[1]))
                    if local_monthly_min > float(row[1]):
                        local_monthly_min = float(row[1])
                    if local_monthly_max < float(row[1]):
                        local_monthly_max = float(row[1])
        monthly_energy, yearly_energy, header_result = calculate_energy(X, Y, monthly_energy, yearly_energy, header_result, result_file)
        X = []
        Y = []
        current_date = date_hour[0]
        print('\nMonth: {} Year: {}'.format(months[i], years[i]))
        print('Monthly consumption of energy: {} TWh\n'.format(str(round((monthly_energy / 1000000), 2))))
    print('\nYearly consumption of energy for {}: {} TWh'.format(zone, str(round((yearly_energy / 1000000), 2))))
    print('Min load yearly: {} MW'.format(str(find_min(min_per_month))))
    print('Max load yearly: {} MW'.format(str(find_max(max_per_month))))
dt2 = time.time()
result = float(str((dt2 - dt1)))
print('\nScript execution in {} seconds'.format(str(round(result, 2))))
