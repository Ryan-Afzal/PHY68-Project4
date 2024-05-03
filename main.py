import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import hashing
import params

class RyanNHusamCachingAlgo:
    _singletons = {}
    csvCache = dict()      # key is a hash of the csv (to save space) and value is a pointer to distance array
    distanceCache = set() # key is a hash of the csv (to save space) and value is a pointer to the distance array
    csvPath = ""
    @classmethod
    def get_instance(cls, file_path):
        hash = hashing.hash_file(file_path)
        if hash not in cls._singletons:
            cls._singletons[hash] = cls()
        cls._singletons[hash].csvPath  = file_path
        return cls._singletons[hash]



    def getDataFromFile(self,filename):
        """
        Reads in a file and converts it into data
        filename: the name of the file

        ex: t, x, y = getDataFromFile("data.csv")
        """
        if 'time' in self.csvCache  and 'x' in self.csvCache and 'y' in self.csvCache:
            return self.csvCache['time'], self.csvCache['x'], self.csvCache['y']
        rows = []
        with open(filename, 'r', newline='') as csvfile:
            filereader = csv.reader(csvfile, dialect=csv.QUOTE_NONNUMERIC, delimiter='\n')
            for row in filereader:
                rows.append(row[0])

        t = []
        x = []
        y = []
        i = 0
        for row in rows:
            r = row.split(",")
            if i < 2 or r[0] == '' or r[1] == '' or r[2] == '':
                i += 1
                continue
            # if i == 1000:
            #     break
            t.append(float(r[0]))
            x.append(float(r[1]))
            y.append(float(r[2]))
            i += 1
        self.csvCache['time'] = np.array(t)
        self.csvCache['x'] = np.array(x)
        self.csvCache['y'] = np.array(y)
        return np.array(t), np.array(x), np.array(y)


    def timeSeriesPlot(self):
        """""
        Time Series Plot: plots distance over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        csv = self.csvPath
        t,x,y = self.getDataFromFile(csv)
        distance_arr = [self.distance_from_origin(i,j) for i, j in zip(x, y)]
        plt.plot(t,distance_arr)
        plt.ylabel('Position')
        plt.xlabel('time')
        plt.grid(True)
        plt.show()


    def phaseSpacePlot(self):
        """""
        Phase Space Plot: plots velocity over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        csv = self.csvPath
        t,x,y = self.getDataFromFile(csv)
        distance_arr = [self.distance_from_origin(i,j) for i, j in zip(x, y)]
        velocity_arr = [distance_arr[i]/t[i] for i in range(len(distance_arr))]
        plt.plot(t,velocity_arr)
        plt.xlabel('time ')
        plt.ylabel('velocity (m/s)')
        plt.grid(True)
        plt.show()


    def polar(self,x, y):
        """
        Converts (x, y) to polar coordinates (r, θ)
        x: number or numpy array-like of length N
        y: number or numpy array-like of length N

        ex: r, θ = polar(x, y)
        """

        r = np.sqrt(x**2 + y**2)
        θ = np.arctan2(x, y)
        # θ = np.arctan(y / x)

        # if (x < 0):
        #     if (y < 0):# x < 0, y < 0
        #         θ += np.pi
        #     else:# x < 0, y >= 0
        #         θ = np.pi / 2 - θ
        # elif (y < 0):# x >= 0, y < 0
        #     θ += 2*np.pi
        # else:# x >= 0, y >= 0
        #     pass

        return r, θ

    def distance_from_origin(self,i, j):
        return math.sqrt(i**2 + j**2)

    def phaseAnglePlot(self):
        """""
        Phase Angle Plot: plots angle over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        csv = self.csvPath
        t,x,y = self.getDataFromFile(csv)
        polarPoints = [self.polar(i,j) for i, j in zip(x, y)]
        angle_arr = [polarPoints[i][1] for i in range(len(polarPoints))]
        plt.plot(t,angle_arr)
        plt.xlabel('time (s)')
        plt.ylabel('angle (rad)')
        plt.grid(True)
        plt.show()

    # polar distance overtime
    def angularPositionPlot(self):
        """""
        Time Series Plot: plots distance over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        csv = self.csvPath
        t,x,y = self.getDataFromFile(csv)
        polarPoints = [self.polar(i,j)[1] for i, j in zip(x, y)]
        plt.plot(t, polarPoints, label='Data')

        p = params.getParams(t, polarPoints)
        plt.plot(t, params.dampedOscillation(t, *p), label='Curve Fit')
        # print(p)
        # print(f'α = {p[1]}')
        print(f'ω = {p[2]}')
        # print(f'ϴ = {p[4]}')

        print(f'κ = I(ω2 + α2) = {np.square(p[2]) * params.I}')

        plt.ylabel('Angle (rad)')
        plt.xlabel('Time (s)')
        plt.grid(True)
        plt.legend()
        plt.show()

def main():
    plottingSystem = RyanNHusamCachingAlgo.get_instance("data/45 degrees.csv")
    # print(plottingSystem.data)
    # plottingSystem.phaseAnglePlot()
    # plottingSystem.timeAnglePlot("data/45 degrees.csv")
    # plottingSystem.timeSeriesPlot()
    # plottingSystem.phaseSpacePlot()
    plottingSystem.angularPositionPlot()


main()