import pandas as pd
import numpy as np
import os
from zipfile import ZipFile
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


zip_dir = 'computer-go-dataset/TYGEM/Kifu'
out_dir = 'data/TYGEN'

S = 19
COLORS = {
    'B': 0,
    'W': 1,
    'N': 0.5,
}


def n_from_alpha(alpha):
    return alpha.encode('utf-8')[0] - 97


def df_from_kifu(kifu):
    lines = kifu.split('\n')
    mat = np.zeros((len(lines), S*S))
    for idx, line in enumerate(kifu.split('\n')):
        if line:
            row = np.zeros((S, S)) + COLORS['N']
            hands = line.split('\t')[1]
            for hand in hands.split(';'):
                if hand and len(hand) == 5:
                    row[n_from_alpha(hand[2]),
                        n_from_alpha(hand[3])] = COLORS[hand[0]]
            mat[idx, :] = row.reshape((1, S*S))

    return pd.DataFrame(mat)


def df_from_kifu_zip_dir():
    # list files and remove zip suffix
    names = map(lambda x: x[:-4], os.listdir(zip_dir))

    # loop thru
    for idx, name in enumerate(names):
        if idx > 10:
            break
        print('processing ' + name)
        # open zip
        zf = ZipFile(os.path.join(zip_dir, name + '.zip'))
        # get raw kifu
        kifu = zf.read(name).decode('utf-8')
        # convert to pandas
        df = df_from_kifu(kifu)
        df.to_csv(os.path.join(out_dir, name + '.csv'), index=None)


def viz():
    df = pd.read_csv(os.path.join(out_dir, '2016-07.csv'))
    row = df.iloc[90]

    plt.figure()
    loc = MultipleLocator(base=1)
    plt.gca().xaxis.set_major_locator(loc)
    plt.gca().yaxis.set_major_locator(loc)
    plt.gca().set_axisbelow(True)
    plt.grid(linestyle='-', axis='both', linewidth='0.5', color='grey')
    for idx in range(row.shape[0]):
        if row[idx] > 0.75:
            plt.scatter(idx % S, int(idx / 19), c='black', s=50)
        elif row[idx] < 0.25:
            plt.scatter(idx % S, int(idx / 19), c='red', s=50)
    plt.show()
