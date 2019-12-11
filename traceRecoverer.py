import csv
import sys
import math


if(len(sys.argv)!= 3):
    print("Usage: \"Python3 traceRecoverer.py <csv of Traces> <traceID1,traceID2,traceID3...>\"")
else:
    traceIds = sys.argv[2].split(',')
    traceIds = list(map(int,traceIds))
    for traceId in traceIds:
        with open(str(traceId)+"_singleTrace.csv",mode = 'w') as csv_write:
            csv_writer = csv.writer(csv_write,delimiter=',')

            with open(sys.argv[1]) as csv_read:
                csv_reader = csv.reader(csv_read,delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        if(int(row[3]) == traceId):
                            csv_writer.writerow(row)
