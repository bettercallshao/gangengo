import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


def show_single_arr(arr):
    s = int(np.sqrt(arr.size))
    arr = arr.reshape((s,s))

    plt.figure()
    loc = MultipleLocator(base=1)
    plt.gca().xaxis.set_major_locator(loc)
    plt.gca().yaxis.set_major_locator(loc)
    plt.gca().set_axisbelow(True)
    plt.grid(linestyle='-', axis='both', linewidth='0.5', color='grey')
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            if arr[x][y] > 0:
                plt.scatter(x, y, c='black', s=50)
            elif arr[x][y] < 0:
                plt.scatter(x, y, c='red', s=50)

    plt.show()
