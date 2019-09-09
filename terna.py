import csv
# import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import quad
import time

dt1 = time.time()

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

# Too slow
def save_result(X, Y, monthly_energy, yearly_energy, result_file, current_date, date_hour):
    f = interp1d(X, Y, kind='cubic')
    """
    if plot:
        plt.plot(X, Y, 'o', X, f(X), '--')
        plt.legend(['data', 'cubic'], loc='best')
        plt.show()
    """
    energy = quad(f, 15.0, 1425.0)[0]
    monthly_energy += energy
    yearly_energy += energy
    result_file.write(current_date + ',' + str(energy) + ',' + str(find_min(Y)) + ',' + str(find_max(Y)) + '\n')
    X = []
    Y = []
    current_date = date_hour[0]

yearly_energy = 0
max_days = [31, 31, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30]
days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
'17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
months = ['07', '08', '09', '10', '11', '12', '01', '02', '03', '04', '05', '06']
years = ['2018', '2018', '2018', '2018', '2018', '2018', '2019', '2019', '2019', '2019', '2019', '2019']
min_per_month = []

for i in range(12):
    file_name = 'terna/' + years[i] + '-' + months[i] + '.csv'
    file = open(file_name, 'r')
    result_file = open('result/out-' + years[i] + '-' + months[i] + '.csv', 'w')
    csv_reader = csv.reader(file, delimiter=',')
    header = True
    plot = False
    X = []
    Y = []
    local_monthly_min = 999999999
    monthly_energy = 0
    current_date = 'empty'
    for row in csv_reader:
        if header == True:
            header = False
        else:
            date_hour = row[0].split(' ')
            if current_date == 'empty':
                current_date = date_hour[0]
            if date_hour[0] != current_date:
                ########## ########## ########## ########## ##########
                f = interp1d(X, Y, kind='cubic')
                """
                if plot:
                    plt.plot(X, Y, 'o', X, f(X), '--')
                    plt.legend(['data', 'cubic'], loc='best')
                    plt.show()
                """
                energy = quad(f, 0.25, 23.75)[0]
                monthly_energy += energy
                yearly_energy += energy
                result_file.write(current_date + ',' + str(energy/1000) + ',' + str(find_min(Y)) + ',' + str(find_max(Y)) + '\n')
                min_per_month.append(local_monthly_min)
                X = []
                Y = []
                current_date = date_hour[0]
                ########## ########## ########## ########## ##########
            else:
                hour = date_hour[1].split(':')
                temp_value = float(hour[0]) + float(int(hour[1])/60)
                timestamp = float(temp_value)
                X.append(timestamp)
                Y.append(float(row[1]))
                if local_monthly_min > float(row[1]):
                    local_monthly_min = float(row[1])
    ########## ########## ########## ########## ##########
    f = interp1d(X, Y, kind='cubic')
    """
    if plot:
        plt.plot(X, Y, 'o', X, f(X), '--')
        plt.legend(['data', 'cubic'], loc='best')
        plt.show()
    """
    energy = quad(f, 0.25, 23.75)[0]
    monthly_energy += energy
    yearly_energy += energy
    result_file.write(current_date + ',' + str(energy/1000) + ',' + str(find_min(Y)) + ',' + str(find_max(Y)) + '\n')
    X = []
    Y = []
    current_date = date_hour[0]
    ########## ########## ########## ########## ##########
    print('\nMonth: ' + months[i] + ' Year: ' + years[i] + '\n')
    print('Monthly consumption of energy: ' + str(round((monthly_energy/1000000), 2)) + ' TWh\n')
print('\nYearly consumption of energy: ' + str(round((yearly_energy/1000000), 2)) + ' TWh\n')
print('Min load yearly: ' + str(find_min(min_per_month)) + ' MW\n')
dt2 = time.time()
result = float(str((dt2 - dt1)))
print('Script execution in ' + str(round(result, 2)) + ' seconds\n')
