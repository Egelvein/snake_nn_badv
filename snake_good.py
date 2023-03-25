import tensorflow
import numpy as np
from snake import *
from snake import Snake
from Agent_1 import Model_NN

status = [0, 0, 0, 0, 0, 0]
control = [0, 0, 0, 0, 0, 0]
encouragement = [0, 0, 0] 

def main():
    control_list = []
    status_list = []
    """ Handles game process """
    s = Snake()
    m = Model_NN()
    IN_GAME = 100
    while IN_GAME > 0:
        #print('IN_GAME')
        head_coords = s.c.coords(s.segments[-1])#.instance)
        x1, y1, x2, y2 = head_coords
        dist_w = WIDTH - x1
        dist_h = HEIGHT - y1
        dist_tail_x = x1 - x2
        dist_tail_y = y1 - y2
        dist_apple_x = x1 - s.posx
        dist_apple_y = y1 - s.posy
        # Check for collision with gamefield edges
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
            bad(encouragement, 2)
            #bad_control(control)
            m.training(np.array(status_list), np.array(bad_control(control_list)))
            status_list = []
            control_list = []
        # Eating apples
        elif head_coords == s.c.coords(s.BLOCK):
            s.add_segment()
            s.c.delete(BLOCK)
            s.create_block()
            good(encouragement)
            good_control(good)
            m.training(np.array(status_list), control_list)
            status_list = []
            control_list = []
        # Self-eating
        else:
            for index in range(len(s.segments)-1):
                if head_coords == s.c.coords(s.segments[index]):#.instance):
                    IN_GAME = False
                    bad(encouragement, 1)
                    bad_control(control)
                    m.training(np.array(status_list), control_list, m.model)
                    status_list = []
                    control_list = []
        #s.root.after(100, main)
        status = [int(dist_w), int(dist_h), int(dist_tail_x), 
                  int(dist_tail_y), int(dist_apple_x), int(dist_apple_y)]#, last_status]
        control = m.predict1(status)
        control_list.append(control)
        status_list.append(status)
        #print('control_list =', control_list)
        #print('status_list =', status_list)

        s.movement(control)
        s.root.update()
        IN_GAME -= 1
    # Not IN_GAME -> stop game and print message
    '''else:
        encouragement = [0, 0, 0]
        s.reset_snake()
        s.c.delete(s.BLOCK)
        IN_GAME = True'''

def good(list):
    for i in range(len(list)):
        list[i] += 0.1
    list[0] += 0.1    

def bad(list, num):
    list[num] = 0

def good_control(control):
    control[0][control[0].argmax()] = 1
    for i in range(3):
        if i != control[0].argmax():
            control[0][i] = 0
    return control

def bad_control(control):
    control[0][control[0].argmax()] = 0
    for i in range(3):
        if i != control[0].argmax():
            control[0][i] = 1
    return control

main()
