import numpy as np


S = 20
COLORS = {
    'B': -1,
    'W': 1,
    'N': 0,
}


def _n_from_alpha(alpha):
    """Convert an alphabetic to a integer"""
    return alpha.lower().encode('utf-8')[0] - 97


def _hands_from_kifu(kifu):
    """Make hands from kifu"""
    kifu = kifu.replace('(', '').replace(')', '').replace('\n', '').replace('\r', '')
    out = []
    for hand in kifu.split(';'):
        if hand and len(hand) == 5 and hand[0] in COLORS.keys():
            out.append((_n_from_alpha(hand[2]), _n_from_alpha(hand[3]), COLORS[hand[0]]))
    return out


def _list_copy_mutated_arr(arr):
    """Make a list of mutated arrays"""
    arr = arr.copy()
    l = [
        arr,
        np.flip(arr, axis=0),
        np.flip(arr, axis=1),
        np.flip(np.flip(arr, axis=0), axis=1),
    ]
    l += [a.T for a in l]
    return l


def list_arr_from_kifu(kifu):
    """Make a list of arrays from a kifu game"""
    l = []
    arr = np.zeros((S, S), dtype='int8') + COLORS['N']

    # iterate over hands
    for x, y, v in _hands_from_kifu(kifu):
        arr[x,y] = v
        l += _list_copy_mutated_arr(arr)

    return l


def arr_from_rand_list(l, n):
    """Stitch list of kifu array randomly to a 3D array"""
    l = l.copy()
    if len(l) < n:
        print('warning: list is too short to stitch')
        l = l * (int(n / len(l)) + 1)

    # take first n items after shuffle
    np.random.shuffle(l)
    l = l[:n]

    return np.concatenate([a.reshape((1, S, S)) for a in l], axis=0)


def arr_from_rand_kifu(kifu, n):
    """Get random kifu array from a kifu str"""
    return arr_from_rand_list(list_arr_from_kifu(kifu), n)


if __name__ == '__main__':
    sample = """
(;FF[4]CA[UTF-8]KM[7.5]OT[3x60 byo-yomi]PB[AlphaGo Zero]PW[AlphaGo Zero]RE[W+R]
RU[Chinese]TM[7200];B[dp];W[pd];B[pp];W[dd];B[qf];W[cq];B[cp];W[dq];B[ep];W[eq]
;B[fq];W[fr];B[cc];W[dc];B[cd];W[de];B[cf];W[df];B[cg];W[ce];B[be];W[bf];B[bd];
W[ch];B[bg];W[dg];B[bh];W[jd];B[qc];W[pc];B[qd];W[pe];B[rg];W[qq];B[qp];W[pq];
B[op];W[nr];B[lc];W[le];B[og];W[ld];B[ci];W[ic];B[mq];W[nq];B[np];W[mp];B[lq];
W[rp];B[ro];W[rq];B[qn];W[gq];B[fp];W[bq];B[ml];W[li];B[fi];W[gp];B[go];W[ho];
B[hn];W[io];B[ko];W[gn];B[fo];W[kn];B[hm];W[fm];B[fl];W[gl];B[gm];W[in];B[km];
W[el];B[fk];W[fn];B[cn];W[lp];B[hp];W[hr];B[kp];W[hl];B[im];W[jm];B[il];W[lm];
B[jl];W[kl];B[kk];W[lo];B[ll];W[mm];B[nm];W[ip];B[nf];W[nl];B[nb];W[mc];B[pb];
W[nk];B[mj];W[pk];B[ql];W[qk];B[pl];W[ni];B[nj];W[oj];B[ol];W[ok];B[lj];W[oh];
B[mi];W[mh];B[lh];W[lg];B[pi];W[nn];B[om];W[kh];B[oi];W[nh];B[ji];W[pf];B[ph];
W[qe];B[re];W[qg];B[rf];W[rm];B[gr];W[gs];B[jn];W[jo];B[km];W[jn];B[mn];W[ln];
B[on];W[kl];B[jj];W[ki];B[km];W[rn];B[iq];W[hq])
"""

    a = arr_from_rand_kifu(sample, 256)

