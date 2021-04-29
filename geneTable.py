
# Sample list
# lst = [(' ', 'Mean', 'Standard deviation', 'Min', 'Max'),
# 	   (1, 444, 'Pune', 18),
# 	   (2, 'Vaishnavi', 'Mumbai', 20),
# 	   (3, 'Rachna', 'Mumbai', 21),
# 	   (4, 'Shubham', 'Delhi', 21)]

import numpy as np

def geneTable(numFI, csvPath):
    y = np.loadtxt(csvPath, delimiter='\n', unpack=True)
    cols = 5
    rows = len(y)/numFI
    lst = []
    titleTuple = (' ', 'Mean', 'Standard deviation', 'Min', 'Max')
    lst.append(titleTuple)
    print()
    for i in range(rows):
        y1 = y[i*numFI: (i+1)*numFI]
        for j in range(cols):
            mean = sum(y1)/len(y1)
            std = sum((x - mean) ** 2 for x in y1) / len(y1)
            mint = min(y1)
            maxt = max(y1)
            oTuple = ( i+1, mean, std, mint, maxt)
        lst.append(oTuple)
    return lst


if __name__ == '__main__':
    lst = geneTable(10, './accuracy.csv')
    print(lst)