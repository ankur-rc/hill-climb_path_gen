import numpy as np
from sys import argv
import matplotlib.pyplot as plt
import random

L = 40  # parameter to set granularity
ip_file = ""
X_MAX, Y_MAX = [0, 0]


def get_neighbours(coord, max_coord):
    """ Input:- coord: a (1,2) ndarray
    Output:- the (n,2) coordinate list of legal neighbours of 'coord'
    """
    x = [x for x in [coord[0]-1, coord[0], coord[0]+1]
         if x >= 0 and x <= max_coord[0]]
    y = [y for y in [coord[1]-1, coord[1], coord[1]+1]
         if y >= 0 and y <= max_coord[0]]

    neighbours = []
    for i in x:
        for j in y:
            if [i, j] != coord:
                neighbours.append([i, j])

    return neighbours


def get_least_euclidean_dist_loc(start, end_list):
    """ Input:- start: a (1,2) ndarray, end_list: a (n, 2) ndarray
    Output:- the (1,2) coordinate in the end_list having the least euclidean distance from the 'start' node
    """

    dist = np.linalg.norm(end_list - start, axis=1)
    best_location = dist.argmin()
    return end_list[best_location]


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
    ip_file = ''

    myargs = getopts(argv)
    if "-f" in myargs:
        ip_file = myargs["-f"]
    else:
        print "Usage: python plan_path.py -f <input file path>"
        exit()

    print "Opened file '", ip_file, "' for reading."
    with open(ip_file, 'r') as heatmap:
        for line in heatmap:
            points = line.split()
            pdist_list.append(points[2])
        last_line = line

    X_MAX = int(last_line.split()[0])
    Y_MAX = int(last_line.split()[1])

    pdist = np.reshape(np.array(pdist_list, dtype=float), [X_MAX+1, Y_MAX+1])
    C = np.max(pdist)/L
    gw_pdist = []  # list of matrices where each matrix cell holds the 'global-warmed' pseudo probabilities

    for i in range(0, L):
        interim_gw = pdist - (C*i)
        interim_gw = interim_gw.clip(min=0)
        gw_pdist.append(interim_gw)

    # cumulative probabilities of all paths;
    # each element represents a path whose indices represent the accumulated probability at each step
    global_cp = []
    global_paths = []

    for i in range(len(gw_pdist)):

        print "Computing path", (i+1), "of", L, "..."

        T = 0                                         # time step
        robo_loc = [0, 0]                             # robot starting location

        # accumluate the probabllity covered of starting cell
        cp = [pdist[robo_loc[0], robo_loc[1]]]

        # set the pseudo-probability of starting cell to zero
        (gw_pdist[i])[robo_loc[0]][robo_loc[1]] = 0

        # reassigning current pseudo-prob matrix for brevity
        pseudo_pdist = gw_pdist[i]
        # maintins pont list for current iteration
        point_list = []
        # add robot starting location to point list
        point_list.append(robo_loc)

        while pseudo_pdist.any():

            # print "At T = ", T, " \t Current node is:", robo_loc

            neighbours = get_neighbours(robo_loc, [X_MAX, Y_MAX])
            # print "Neighbours being considered: ", neighbours

            max_prob = 0
            for neighbour in neighbours:
                if pseudo_pdist[neighbour[0], neighbour[1]] >= max_prob:
                    max_prob = pseudo_pdist[neighbour[0], neighbour[1]]

            best_neighbours = []
            for neighbour in neighbours:
                if pseudo_pdist[neighbour[0], neighbour[1]] == max_prob:
                    best_neighbours.append(neighbour)

            # print "Best neighbours: ", best_neighbours

            best_neighbour = None
            # no tie-breaker required!
            if len(best_neighbours) == 1:
                # print "Best neighbour is: ", best_neighbours[0]
                # set new robot location
                robo_loc = best_neighbours[0]
                best_neighbour = best_neighbours[0]

            # tie-breaker required!
            else:

                # get next highest probability node(s)
                hpn_locs = np.argwhere(pseudo_pdist == np.max(pseudo_pdist))
                # print len(hpn_locs), "possible locations being considered."
                best_hpn_loc = get_least_euclidean_dist_loc(np.array(robo_loc),  # get coord of HPN with least distance from
                                                            hpn_locs)            # current node
                # print "Nearest HPN location:", best_hpn_loc

                best_neighbour = get_least_euclidean_dist_loc(                  # get coord of neighbour with least distance
                    best_hpn_loc, np.array(best_neighbours))                    # from thr nearest HPN
                # print "Best beighbour is:", best_neighbour.tolist()

                # set new robot location
                robo_loc = best_neighbour.tolist()
                best_neighbour = best_neighbour.tolist()

            # get probability accumulated till last step
            last_step_cp = cp[-1]
            current_prob = 0
            if best_neighbour in point_list:
                current_prob = 0
            else:
                current_prob = pdist[best_neighbour[0], best_neighbour[1]]
            # add new probability
            cp.append(last_step_cp + current_prob)
            # append new location to node list
            point_list.append(robo_loc)
            # set visited node's pseudo prob value to zero
            pseudo_pdist[best_neighbour[0], best_neighbour[1]] = 0
            T += 1
            # print "-"*60

        global_cp.append(cp)
        global_paths.append(point_list)

    # best path for complete coverage
    best_path_cc = global_paths[0]
    # best path for max (cumulative probability) climb till T=900
    best_path_max_climb_index = None
    best_cp_at_900 = 0
    for i in range(len(global_cp)):
        cp = 0
        if len(global_cp[i]) > 900:
            cp = (global_cp[i])[899]
        else:
            cp = (global_cp[i])[-1]

        if cp > best_cp_at_900:
            best_cp_at_900 = cp
            best_path_max_climb_index = i

    print "Most efficient path index is:", best_path_max_climb_index

    print "Writing 'complete coverage' path to '", str(
        (ip_file.split("."))[0]) + "_complete_coverage.txt.'"
    op_file = open(
        str((ip_file.split("."))[0]) + "_complete_coverage.txt", 'w')
    for i in range(len(best_path_cc)):
        op_file.write(str(best_path_cc[i][0]) +
                      " " + str(best_path_cc[i][1]) + "\n")

    op_file.close()

    print "Writing 'most efficient' path to '", (ip_file.split("."))[
        0] + "_most_efficient.txt.'"
    op_file = open((ip_file.split("."))[0] + "_most_efficient.txt", 'w')
    for i in range(len(global_paths[best_path_max_climb_index])):
        op_file.write(str((global_paths[best_path_max_climb_index])[
                      i][0]) + " " + str((global_paths[best_path_max_climb_index])[i][1]) + "\n")
    op_file.close()

    print "Done."


if __name__ == '__main__':
    main()
