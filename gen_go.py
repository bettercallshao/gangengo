from extractor import KifuGen
from renderer import arr_from_rand_kifu
from visualizer import show_single_arr


class GenGo(object):
    def __init__(self):
        self.kifu = KifuGen()

    def arr_from_random(self, n):
        return arr_from_rand_kifu(self.kifu.str_from_random(), n)

    def show_random(self):
        show_single_arr(arr_from_rand_kifu(self.kifu.str_from_random(), 1))
