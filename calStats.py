# Show statistic results (average, standard deviation, min & max)
import numpy as np
import math

# Calculate the average
def calAve(csvPath):
    y = np.loadtxt(csvPath, delimiter='\n', unpack=True)
    return sum(y)/len(y)

# Calculate the standard deviation
def calmsd(csvPath):
    y = np.loadtxt(csvPath, delimiter='\n', unpack=True)
    mean = sum(y)/len(y)
    var = sum((x - mean) ** 2 for x in y) / len(y)
    std_dev = math.sqrt(var)
    return std_dev

# Calculate the min
def calMin(csvPath):
    y = np.loadtxt(csvPath, delimiter='\n', unpack=True)
    return min(y)

# Calculate the max
def calMax(csvPath):
    y = np.loadtxt(csvPath, delimiter='\n', unpack=True)
    return max(y)

if __name__ == '__main__':
    ave = calmsd('./accuracy')
    print(ave)