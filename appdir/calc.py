import csv

filename = 'sampledata.csv'

latarr = []
longarr = []
altarr = []
timearr = []

with open(filename) as data:
    reader = csv.reader(data, quoting = csv.QUOTE_NONNUMERIC)
    for row in reader:
        print(row)

        latarr.append(row[0])
        longarr.append(row[1])
        altarr.append(row[2])
        timearr.append(row[3])