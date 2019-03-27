import numpy as np
import os
from zipfile import ZipFile
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


zip_dir = 'computer-go-dataset/TYGEM/Kifu'
out_dir = 'data/TYGEN'

S = 20
COLORS = {
    'B': -1,
    'W': 1,
    'N': 0,
}
FILE_NAME = 'go'


def n_from_alpha(alpha):
    return alpha.encode('utf-8')[0] - 97


def arr_from_kifu(kifu):
    lines = kifu.split('\n')
    mat = np.zeros((len(lines), S, S))
    for idx, line in enumerate(kifu.split('\n')):
        if line:
            row = np.zeros((S, S)) + COLORS['N']
            hands = line.split('\t')[1]
            for hand in hands.split(';'):
                if hand and len(hand) == 5:
                    row[n_from_alpha(hand[2]),
                        n_from_alpha(hand[3])] = COLORS[hand[0]]
            mat[idx, :] = row

    return mat


def arr_from_kifu_zip_dir():
    # list files and remove zip suffix
    names = map(lambda x: x[:-4], os.listdir(zip_dir))

    big = None

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
        arr = arr_from_kifu(kifu)
        if big is None:
            big = arr
        else:
            big = np.concatenate([big, arr], axis=0)

    return big


def arr_from_noise():
    N_FAKE = 140*1000
    arr = np.random.randint(0, 4, size=(N_FAKE, S, S)) / 3
    arr[(arr > 0) & (arr < 1)] = 0.5
    arr = arr * 2 - 1
    return arr


def make_pos_neg_csv():
    neg = arr_from_noise()
    neg['go'] = 0
    pos = arr_from_kifu_zip_dir()
    pos['go'] = 1

    big = np.concatenate([pos, neg], axis=0)
    big.to_csv(os.path.join(out_dir, 'go.csv'), index=None)


def make_pos_npy():
    pos = arr_from_kifu_zip_dir()
    np.savez_compressed(FILE_NAME, go=pos.reshape(pos.shape[0], S, S))


def viz_row(arr):
    row = arr[np.random.randint(0, arr.shape[0])]

    plt.figure()
    loc = MultipleLocator(base=1)
    plt.gca().xaxis.set_major_locator(loc)
    plt.gca().yaxis.set_major_locator(loc)
    plt.gca().set_axisbelow(True)
    plt.grid(linestyle='-', axis='both', linewidth='0.5', color='grey')
    for x in range(row.shape[0]):
        for y in range(row.shape[1]):
            if row[x][y] > 0.5:
                plt.scatter(x, y, c='black', s=50)
            elif row[x][y] < -0.5:
                plt.scatter(x, y, c='red', s=50)


def show():
    plt.show()


def compare():
    while True:
        pos = np.load(FILE_NAME + '.npz')['go']
        viz_row(pos)
        neg = arr_from_noise()
        viz_row(neg)
        show()
