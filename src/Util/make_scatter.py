'''
Created on 15/09/2011

@author: Michael
'''

import sys
import matplotlib.pyplot as plt

bot1 = "Dave2Player"

if __name__ == '__main__':
    file = open(sys.argv[1]).read()
    x = []
    y1 = []
    y2 = []
    lines = file.split("\n")
    for line in lines:
        tokens = line.split(':')
        if len(tokens) <3:
            break
        x.append(int(tokens[0]))
        y1.append(int(tokens[4].split(',')[1]))
        y2.append(int(tokens[5].split(',')[1]))
        y2 = map(lambda i: -i,y2)

   
    #for each point, draw them on a bitmap
    plt.bar(x, y1, facecolor='#9999ff', edgecolor='white')
    plt.bar(x, y2, facecolor='#ff9999', edgecolor='white')
    plt.savefig('../scatter.pdf')
    plt.show()