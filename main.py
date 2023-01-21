import argparse
import time

from easy_dc.utils import get_G
from easy_dc.weave import weave_discocube


parser = argparse.ArgumentParser(description='Welcome to solve_dc package! Installing this package created the first 25 instances, from order 32 to 26208. You can solve higher instances but the graphs will have to be produced first.')
parser.add_argument('--help', action='store_true', help='Show help message')
parser.add_argument('order', type=int, help='The order of the problem instance')
args = parser.parse_args()


if args.help:
    print("Installing this package created the first 25 instances, from order 32 to 26208. You can solve higher instances but the graphs will have to be produced first.")
    print("\nThe following orders available are:")
    print([32, 80, 160, 280, 448, 672, 960, 1320, 1760, 2288, 2912, 3640, 4480, 5440, 6528, 7752, 9120, 10640, 12320, 14168, 16192, 18400, 20800, 23400, 26208, 29232, 32480, 35960, 39680, 43648, 47872, 52360, 57120, 62160, 67488, 73112, 79040, 85280, 91840, 98728, 105952, 113520, 121440, 129720, 138368, 147392, 156800, 166600, 176800, 187408, 198432, 209880, 221760, 234080, 246848, 260072, 273760, 287920, 302560, 317688, 333312, 349440, 366080, 383240, 400928, 419152, 437920, 457240, 477120, 497568, 518592, 540200, 562400, 585200, 608608, 632632, 657280, 682560, 708480, 735048, 762272, 790160, 818720, 847960, 877888, 908512, 939840, 971880, 1004640, 1038128, 1072352, 1107320, 1143040, 1179520, 1216768, 1254792, 1293600, 1333200, 1373600])
    exit()


def solve(order):
    G = get_G(order)
    A, V, VI, E, EA = G['A'], G['V'], G['VI'], G['E'], G['EA']
    print("solving order ", order)
    start = time.time()
    weave_discocube(A, V, VI, EA)
    dur = time.time() - start
    print("Time taken: ", dur)


solve(args.order)
