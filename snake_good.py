#import tensorflow
import numpy as np
from snake import *
from snake import Snake
from Agent_1 import Model_NN

status = [0, 0, 0, 0, 0, 0]
control = [] 

def main():
    score = 0
    control_list = []
    status_list = []
    """ Handles game process """
    s = Snake()
    m = Model_NN()
    IN_GAME = True
    
    while IN_GAME == True:
        head_coords = s.c.coords(s.segments[-1])
        x1, y1, x2, y2 = head_coords
        dist_w = WIDTH - x1
        dist_h = HEIGHT - y1
        dist_tail_x = x1 - x2
        dist_tail_y = y1 - y2
        dist_apple_x = x1 - s.posx
        dist_apple_y = y1 - s.posy

        status = [int(dist_w), int(dist_h), int(dist_tail_x), 
                  int(dist_tail_y), int(dist_apple_x), int(dist_apple_y)]
        control = m.predict1(status)
        control_list.append(control)
        status_list.append(status)
        
        # Check for collision with gamefield edges
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
            m.training(np.array(status_list),bad_control(control_list))
            status_list = []
            control_list = []
            s.c.delete(s.BLOCK)
            s.create_block()
            s.restart_game()
            IN_GAME = True
            
        # Eating apples
        elif head_coords == s.c.coords(s.BLOCK):
            s.add_segment()
            s.c.delete(s.BLOCK)
            s.create_block()
            m.training(np.array(status_list), control_list)
            status_list = []
            control_list = []
            score += 1
            
        # Self-eating
        else:
            for index in range(len(s.segments)-1):
                if head_coords == s.c.coords(s.segments[index]):
                    IN_GAME = False
                    print('status = ', len(status_list))
                    print('control = ', len(control_list))
                    print('len segments = ', len(s.c.coords(s.segments[index])))
                    print('index = ', index)
                    if len(status_list) != 0 or len(control_list) != 0:
                        m.training(np.array(status_list), bad_control_self_eating(control_list))
                    s.c.delete(s.BLOCK)
                    s.create_block()
                    s.restart_game()
                    IN_GAME = True

        s.movement(control)
        s.root.update()

def good_control(control):
    control[-1][control[-1].argmax()] = 1
    for j in range(int((len(control)/100)*10)):
        idx  = control[-j][0].argmax()
        control[-j][0] = [1 if i == idx else 0 for i in range(3)]
    return control

def bad_control(control):
    for j in range (int((len(control)/100)*10)):
        idx  = control[-j][0].argmax()
        control[-j][0] = [0 if i == idx else 1 for i in range(3)]
    return control

def bad_control_self_eating(control):
    idx  = control[-1][0].argmax()
    control[-1][0] = [0 if i == idx else 1 for i in range(3)]
    return control

main()
