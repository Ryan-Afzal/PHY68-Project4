import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import hashing


class RyanNHusamCachingAlgo:
    _singletons = {}
    csvCache = dict()      # key is a hash of the csv (to save space) and value is a pointer to distance array
    distanceCache = set() # key is a hash of the csv (to save space) and value is a pointer to the distance array

    @classmethod
    def get_instance(cls, file_path):
        hash = hashing.hash_file(file_path)
        if hash not in cls._singletons:
            cls._singletons[hash] = cls()
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


    def timeSeriesPlot(self,csv):
        """""
        Time Series Plot: plots distance over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        t,x,y = self.getDataFromFile(csv)
        # polarPoints = [polar(i,j) for i, j in zip(x, y)]
        distance_arr = [self.distance_from_origin(i,j) for i, j in zip(x, y)]
        print(distance_arr)
        plt.plot(t,distance_arr)
        plt.ylabel('Position')
        plt.xlabel('time')
        plt.grid(True)
        plt.show()


    def phaseSpacePlot(self,csv):
        """""
        Phase Space Plot: plots velocity over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        t,x,y = self.getDataFromFile(csv)
        distance_arr = [self.distance_from_origin(i,j) for i, j in zip(x, y)]
        velocity_arr = [distance_arr[i]/t[i] for i in range(len(distance_arr))]
        plt.plot(t,velocity_arr)
        plt.xlabel('time')
        plt.ylabel('velocity')
        plt.grid(True)
        plt.show()


    def polar(self,x, y):
        """
        Converts (x, y) to polar coordinates (r, θ)
        x: number or numpy array-like of length N
        y: number or numpy array-like of length N

        ex: r, θ = polar(x, y)
        """
        return (np.sqrt(x**2 + y**2)), (np.arctan2(y/x))

    def distance_from_origin(self,i, j):
        return math.sqrt(i**2 + j**2)

    def phaseAnglePlot(self,csv):
        """""
        Phase Angle Plot: plots angle over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        t,x,y = self.getDataFromFile(csv)
        polarPoints = [self.polar(i,j) for i, j in zip(x, y)]
        angle_arr = [polarPoints[i][1] for i in range(len(polarPoints))]
        plt.plot(t,angle_arr)
        plt.xlabel('time')
        plt.ylabel('angle')
        plt.grid(True)
        plt.show()



def main():
    plottingSystem = RyanNHusamCachingAlgo.get_instance("data/45 degrees mass A.csv")
    # print(plottingSystem.data)
    # phaseAnglePlot("data/45 degrees mass A.csv")
    plottingSystem.timeSeriesPlot("data/45 degrees mass A.csv")
    plottingSystem.phaseSpacePlot("data/45 degrees mass A.csv")


main()