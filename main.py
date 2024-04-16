import numpy as np
import csv
import math
import matplotlib.pyplot as plt

def getDataFromFile(filename):
	"""
	Reads in a file and converts it into data
	filename: the name of the file

	ex: t, x, y = getDataFromFile("data.csv")
	"""
	rows = []
	with open(filename, 'r', newline='') as csvfile:
		filereader = csv.reader(csvfile, dialect=csv.QUOTE_NONNUMERIC, delimiter='\n')
		for row in filereader:
			rows.append(row[0])
    
	t = np.zeros(len(rows))
	x = np.zeros(len(rows))
	y = np.zeros(len(rows))
    
	i = 0
	for row in rows:
		r = row.split(", ")
		t[i] = r[0]
		x[i] = r[1]
		y[i] = r[2]
		i += 1
	return t, x, y

def polar(x, y):
	"""
	Converts (x, y) to polar coordinates (r, θ)
	x: number or numpy array-like of length N
	y: number or numpy array-like of length N
	
	ex: r, θ = polar(x, y)
	"""
	return (np.sqrt(x*x + y*y)), (np.arctan(y/x))



def distance_from_origin(i, j):
    return math.sqrt(i**2,j**2)



    

    
class ElTotosRyanNHusamCachingAlgo:
    _singleton = None
    csvCache = dict()      # key is a hash of the csv (to save space) and value is a pointer to distance array
    distanceCache = dict() # key is a hash of the csv (to save space) and value is a pointer to the distance array

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super().__new__(cls, *args, **kwargs)
        return cls._singleton

    def __init__(self, data):
        if not hasattr(self, 'initialized'):
            self.data = data
            self.initialized = True
            
    def phaseSpacePlot(csv):
        """""
        Phase Space Plot: plots velocity over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        t,x,y = getDataFromFile(csv)
        distance_arr = [distance_from_origin(i,j) for i, j in zip(x, y)]
        velocity_arr = [distance_arr[i]/t[i] for i in range(len(distance_arr))]
        plt.plot(velocity_arr,t,marker='o')
        plt.xlabel('Position')
        plt.ylabel('time')
        plt.grid(True)
        plt.show()
        
    def timeSeriesPlot(csv):
        """""
        Time Series Plot: plots distance over time in metric units
        csv: with 3 columns
            t - time in seconds
            x - position in x-coordinate m
            y - position in y-coordinate
        """
        t,x,y = getDataFromFile(csv)
        # polarPoints = [polar(i,j) for i, j in zip(x, y)]
        distance_arr = [distance_from_origin(i,j) for i, j in zip(x, y)]
        plt.plot(distance_arr,t,marker='o')
        plt.xlabel('Position')
        plt.ylabel('time')
        plt.grid(True)
        plt.show()
    
def main():
    plottingSystem = ElTotosRyanNHusamCachingAlgo("test")
    print(plottingSystem.data)