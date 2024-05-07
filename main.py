## main.py - Husam Adam, Ryan Afzal, Labib Afia
## This file gets our data from the csv files. This also plots our data, model,
## and error.

import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import hashing
import params

class RyanNHusamCachingAlgo:
    _singletons = {}
    _csvCache = None      # key is a hash of the csv (to save space) and value is a pointer to distance array
    _distanceCache = None # key is a hash of the csv (to save space) and value is a pointer to the distance array
    csvPath = ""
    @classmethod
    def get_instance(cls, file_path):
        hash = hashing.hash_file(file_path)
        if hash not in cls._singletons:
            cls._singletons[hash] = cls()
        cls._singletons[hash].csvPath  = file_path
        cls._singletons[hash]._csvCache = dict()
        cls._singletons[hash]._distanceCache = set()
        return cls._singletons[hash]

    def getDataFromFile(self,filename):
        """
        Reads in a file and converts it into data
        filename: the name of the file

        ex: t, x, y = getDataFromFile("data.csv")
        """
        if 'time' in self._csvCache  and 'x' in self._csvCache and 'y' in self._csvCache:
            return self._csvCache['time'], self._csvCache['x'], self._csvCache['y']
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
        self._csvCache['time'] = np.array(t)
        self._csvCache['x'] = np.array(x)
        self._csvCache['y'] = np.array(y)
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
        plt.title(self.csvPath)
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
        plt.title(self.csvPath)
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
        plt.title(self.csvPath)
        plt.xlabel('time (s)')
        plt.ylabel('angle (rad)')
        plt.grid(True)
        plt.show()

    # polar distance overtime
    def angularPositionPlot(self):
        """""
        Time Series Plot: plots angle over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        csv = self.csvPath
        t,x,y = self.getDataFromFile(csv)
        angles = [self.polar(i,j)[1] for i, j in zip(x, y)]
        plt.plot(t, angles, label='Data')

        p, model = params.getParams(t, angles)
        plt.plot(t, params.dampedOscillation(t, *p), label='Curve Fit')
        print(f'ω = {p[2]}')

        print(f'κ = I(ω2 + α2) = {params.I * (np.square(p[2]) + np.square(p[1]) )}')

        plt.title(self.csvPath)
        plt.ylabel('Angle (rad)')
        plt.xlabel('Time (s)')
        plt.grid(True)
        plt.legend()
        plt.show()
        return angles, p, model

    def plotError(self, polarPoints, model):
        """""
        plotError: plots error over time
        Takes the data, subtracts the models values, and plots it.
        """
        t,x,y = self.getDataFromFile(self.csvPath)
        error = polarPoints - model
        plt.plot(t, error, label='Error')
        plt.title(self.csvPath)
        plt.ylabel('Error (rad)')
        plt.xlabel('Time (s)')
        plt.grid(True)
        plt.legend()
        plt.show()


def main():
    files = ["data/45 degrees.csv", "data/90 degrees.csv", "data/135 degrees.csv"]
    for i, file in enumerate(files):
        print(file)
        plottingSystem = RyanNHusamCachingAlgo.get_instance(file)
        polarPoints, p, model = plottingSystem.angularPositionPlot()
        plottingSystem.plotError(polarPoints, model)
        if i != len(files) -1:
            print()

if __name__ == "__main__":
    main()