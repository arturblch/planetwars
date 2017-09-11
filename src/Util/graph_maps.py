'''
Created on 02/10/2011

@author: Michael
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from math import ceil, sqrt

def read_map(data):
    '''
    Returns (game_id, a list of (x, y, owner)) - the planets on the map
    '''
    result = []
    
    for line in data:
        tokens = line.split(" ")
        if tokens[0] == "P":
            result.append((float(tokens[1]), float(tokens[2]), float(tokens[6]), tokens[4]))
        elif tokens[0] == "M":
            mapid = int(tokens[1])
    return (mapid, result)
    
def read_map_from_file(map_name):
    mapfile = open(map_name, 'r')
    game_data = mapfile.read().split("\n")
    mapfile.close()
    return read_map(game_data)



def draw_map(id, map):
    '''
    Takes a list of planet (x, y, growth, owner) data and draws it onto a matplotlib
    plot. Returns the plot.
    '''
    fig = plt.figure()
    plt.gca().invert_yaxis()
    
    x = []
    y = []
    size = []
    color = []
    for planet in map:
        x.append(planet[0])
        y.append(planet[1])
        size.append((10 + planet[2] * 2) ** 2)
        if planet[3] == "0":
            color.append([0.25, 0.25, 0.25])
        elif planet[3] == "1":
            color.append([0, 0, 1])
        else:
            color.append([1, 0, 0])
    ax = fig.add_subplot(111)
    ax.scatter(x, y, c=color, s=size)
    ax.set_title("test_map")
    

    return fig


if __name__ == '__main__':
    id, map = read_map_from_file('../../newmaps/map0.txt')
    fig = draw_map(id, map)
    fig.savefig('map.pdf')
    plt.show()
