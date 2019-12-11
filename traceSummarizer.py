import csv
import sys
import math
import random

class Trace:
    def __init__(self,mz,rt,intensity, mseMz, mseRt, mseIntensity,traceId,real):
        self.mz = float(mz)
        self.rt = float(rt)
        self.intensity = float(intensity)
        self.mseMz = float(mseMz)
        self.mseRt = float(mseRt)
        self.mseIntensity = float(mseIntensity)
        self.traceId = int(traceId)
        self.real = int(real)
class Point:
    def __init__(self, mz, rt, intensity, traceId):
        self.mz = float(mz)
        self.rt = float(rt)
        self.intensity = float(intensity)
        self.traceId = int(traceId)



if len(sys.argv) < 2:
    print("ERROR: Incorrect number of arguments.")
    print("Usage \"python3 traceSummarizer.py <tracedPoints.csv>\"\n")
    sys.exit()

def MSE(points, average):
    sum = 0
    for point in points:
        sum += (point - average)**2
    return sum/len(points)

with open(sys.argv[1]) as csv_file:
    traceDict = {}
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    traces = []

    #Read in all points into trace dictionary
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            pt = Point(row[0],row[1],row[2],row[3])
            if row[3] in traceDict.keys():
                traceDict[row[3]].append(pt)
            else:
                traceDict[row[3]] = [pt]

    #enumerate over all traces in dictionary
    for i,trace in enumerate(traceDict):
        if(i %1000 == 0):
            print(i/len(traceDict))
        meanMz = 0
        meanRt = 0
        meanIntensity = 0
        mzs = []
        rts = []
        intensities = []

        #Sum summary statistics for each trace
        for pt in traceDict[trace]:
            meanMz += pt.mz
            meanRt += pt.rt
            meanIntensity += pt.intensity
            mzs.append(pt.mz)
            rts.append(pt.rt)
            intensities.append(pt.intensity)

        #Calculate mean of all values for trace
        meanMz = meanMz/len(traceDict[trace])
        meanRt = meanRt/len(traceDict[trace])
        meanIntensity = meanIntensity/len(traceDict[trace])

        #Calculate MSE for all values for trace
        mseMz = MSE(mzs, meanMz)
        mseRt = MSE(rts, meanRt)
        mseIntensity = MSE(intensities, meanIntensity)

        #Add Traces to array
        traces.append(Trace(meanMz,meanRt,meanIntensity,mseMz,mseRt,mseIntensity,trace,1))

        #Pair trace with random existing trace for creating false data
        randTrace = random.choice(list(traceDict.keys()))

        #Create and append false trace
        for pt in traceDict[randTrace]:
            meanMz += pt.mz
            meanRt += pt.rt
            meanIntensity += pt.intensity
            mzs.append(pt.mz)
            rts.append(pt.rt)
            intensities.append(pt.intensity)

        meanMz = meanMz/len(traceDict[trace])
        meanRt = meanRt/len(traceDict[trace])
        meanIntensity = meanIntensity/len(traceDict[trace])

        mseMz = MSE(mzs, meanMz)
        mseRt = MSE(rts, meanRt)
        mseIntensity = MSE(intensities, meanIntensity)

        traces.append(Trace(meanMz,meanRt,meanIntensity,mseMz,mseRt,mseIntensity,trace,0))


    with open("traceSummaries.csv", mode = 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        counter = 0
        csv_writer.writerow(["mz","rt","intensity","mseMz","mseRt","mseIntensity","traceId"])
        for trace in traces:

            if counter % 1000 == 0:
                print(counter/len(traces)*100)

            csv_writer.writerow([trace.mz, trace.rt, trace.intensity, trace.mseMz, trace.mseRt, trace.mseIntensity, trace.traceId,trace.real])

            counter+=1
