import csv

days = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
        '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
months = ['07', '08', '09', '10', '11', '12', '01', '02', '03', '04', '05', '06']
years = ['2018', '2018', '2018', '2018', '2018', '2018', '2019', '2019', '2019', '2019', '2019', '2019']
region1 = 'centre-north'
region2 = 'centre-south'
region_result = 'centre'

for i in range(12):
    file_region1 = open('terna/{}/{}-{}.csv'.format(region1, years[i], months[i]), 'r')
    file_region2 = open('terna/{}/{}-{}.csv'.format(region2, years[i], months[i]), 'r')
    result_file = open('terna/{}/{}-{}.csv'.format(region_result, years[i], months[i]), 'w')
    csv_reader_region1 = file_region1.readlines()
    csv_reader_region2 = file_region2.readlines()
    header = True
    header_result = True
    row_count_1 = sum(1 for row in csv_reader_region1)
    row_count_2 = sum(1 for row in csv_reader_region2)
    if row_count_1 != row_count_2:
        print('File dimensions don\'t match on i = {}, {} != {}, terminating...'.format(i, row_count_1, row_count_2))
        exit(-1)
    for j in range(row_count_1):
        if header:
            header = False
            continue
        else:
            row_array_1 = csv_reader_region1[j].split(',')
            row_array_2 = csv_reader_region2[j].split(',')
            date_1 = row_array_1[0]
            date_2 = row_array_2[0]
            if date_1 != date_2:
                print('Date time doesn\'t match on i = {} j = {}, date 1 = {} date 2 = {} terminating...'.format(i, j,
                                                                                                                 date_1,
                                                                                                                 date_2))
                exit(-2)
            if header_result:
                result_file.write('Date,Total Load [MW],Forecast Total load [MW],Bidding zone\n')
                header_result = False
            result_load = float(row_array_1[1]) + float(row_array_2[1])
            result_forecast = float(row_array_1[2]) + float(row_array_2[2])
            result_file.write('{},{},{},{}\n'.format(date_1, result_load, result_forecast, csv_reader_region1[j][3]))
