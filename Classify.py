import numpy as np
from sklearn.neighbors import KNeighborsClassifier

if __name__ == '__main__':
    X = np.loadtxt("test.txt", dtype={'names': ('Contrast', 'Energy', 'Homogenity', 'Correlation'),
                            'formats': (np.float, np.float, np.float, np.float)})
    Y = [1,0,1,0,1]

    print X
    print Y
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(X, Y)
    print(neigh.predict([[100.0,0.5,0.2,0.1]]))
