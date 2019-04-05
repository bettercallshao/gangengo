import os
from zipfile import ZipFile
from hashlib import md5
from numpy import random


DEST_DIR = 'data/'
if not os.path.isdir(DEST_DIR):
    os.mkdir(DEST_DIR)


def _md5hash(b):
    """Calculate hash for some bytes"""
    m = md5()
    m.update(b)
    return m.hexdigest()


def _extract_pro():
    dpath = 'computer-go-dataset/Professional/'
    names = ['pro1940-1999', 'pro2000+']

    # loop thru
    for name in names:
        # open zip
        zf = ZipFile(dpath + name + '.zip')
        # get raw kifu
        lines = zf.read(name + '.txt')
        # keep appending
        for line in lines.split(b'\n'):
            if line:
                h = _md5hash(line)
                with open(DEST_DIR + h + '.txt', 'wb') as f:
                    f.write(line)


def _extract_ai():
    paths = os.popen("find computer-go-dataset/ -iname '*.sgf'").read()
    for path in paths.split('\n'):
        if path:
            with open(path, 'rb') as i:
                kifu = i.read()
                h = _md5hash(kifu)
                with open(DEST_DIR + h + '.txt', 'wb') as o:
                    o.write(kifu)


def _pack():
    os.popen("zip -r go data").read()


def extract_and_pack():
    _extract_pro()
    _extract_ai()
    _pack()


class KifuGen(object):
    def __init__(self):
        self.zf = ZipFile('go.zip')
        self.namelist = self.zf.namelist()

    def str_from_random(self):
        idx = random.randint(len(self.namelist))
        return self.zf.read(self.namelist[idx]).decode('utf-8')

