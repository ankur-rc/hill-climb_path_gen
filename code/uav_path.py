import numpy as np
from sys import argv
import matplotlib.pyplot as plt

L = 40  # parameter to set granularity


def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts


def main():

    pdist_list = []
    last_line = ''

    myargs = getopts(argv)
    if "-f" in myargs:
        ip_file = myargs["-f"]
    else:
        print "Usage: uav_path.py -f <input file path>"
        exit()

    with open(ip_file, 'r') as heatmap:
        for line in heatmap:
            points = line.split()
            pdist_list.append(points[2])
        last_line = line
    x_max_coord = int(last_line.split()[0])
    y_max_coord = int(last_line.split()[1])
    # have the probability distribution in a matrix now
    pdist = np.reshape(np.array(pdist_list, dtype=float),
                       [x_max_coord+1, y_max_coord+1])

    C = np.max(pdist)/L

    gw_pdist = []
    for i in range(0, L):
        interim_gw = pdist - (C*i)
        interim_gw = interim_gw.clip(min=0)
        gw_pdist.append(interim_gw)
        #print interim_gw.max()


if __name__ == '__main__':
    main()
