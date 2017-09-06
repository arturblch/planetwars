'''
Created on 15/09/2011

@author: Michael
'''

import sys
import matplotlib.pyplot as plt

bot1 = "Dave2Player"

if __name__ == '__main__':
    file = open(sys.argv[1]).read()
    game_num = []
    fleet_b1 = []
    fleet_b2 = [] 
    game_time = []

    lines = file.split("\n")
    for line in lines:
        tokens = line.split(':')
        if len(tokens) <3:
            break
        game_num.append(int(tokens[0]))
        if tokens[2] == bot1:
            game_time.append(int(tokens[3]))
        else:
            game_time.append(-int(tokens[3]))
        fleet_b1.append(int(tokens[4].split(',')[1]))
        fleet_b2.append(int(tokens[5].split(',')[1]))
    fleet_b2 = map(lambda i: -i,fleet_b2)

   
    #for each point, draw them on a bitmap
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.grid(True)
    ax1.vlines(game_num, [0], fleet_b1, colors='#9999ff')

    
    ax1.vlines(game_num, [0], fleet_b2, color='#ff9999')   

    ax2 = fig.add_subplot(212)
    ax2.vlines(game_num, [0], game_time)   
    plt.savefig('../scatter.pdf')
    plt.show()