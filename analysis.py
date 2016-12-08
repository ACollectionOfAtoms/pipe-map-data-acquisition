import csv
""" Quick script to calculate stats at end of web app """

with open('pipe-data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    data = {}
    for row in reader:
        if row[0] == 'uuid':  # skip the header
            continue
        row_id = row[0]
        city = row[1]
        state = row[2]
        ref_link = row[3]
        gallons = row[4]
        try:
            gallons = int(gallons)
        except ValueError:
            gallons = 0
        description = row[5]
        date = row[6]
        lat = row[7]
        accident_type = row[8]
        year = date.split('-')[0]
        # construct dict of years
        # with a list of accidents
        if year not in data:
            data[year] = [gallons]
        else:
            data[year].append(gallons)
    total_incidents = 0
    total_gallons = 0
    average_minimum_gallons = [] # list of minimum gallons spilt per year
    for year in data:
        gallons_spilt = [g for g in data[year] if g > 0]
        total_gallons += sum(gallons_spilt)
        average_minimum_gallons.append(min(gallons_spilt))
        total_incidents += len(data[year])
        print year, gallons_spilt
    print '************'
    print 'avg incidents a year:'
    print total_incidents / 17 # 23
    print 'average gallons spilt a year:'
    print total_gallons / 17
    print 'average of minimum gallons spilt'
    print sum(average_minimum_gallons) / 17
