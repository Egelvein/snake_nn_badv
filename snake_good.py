import numpy as np
from sklearn import preprocessing
from snake import *
from snake import Snake
from Agent_1 import Model_NN

status = [0, 0, 0, 0, 0, 0, 0]
control = []

def main():
    h = 180
    control_list = []
    status_list = []
    """ Handles game process """
    s = Snake()
    m = Model_NN()
    IN_GAME = True
    
    while IN_GAME == True:
        head_coords = s.c.coords(s.segments[-1])
        x1, y1, x2, y2 = head_coords
        
        x_dir = x1 - x2
        y_dir = y1 - y2
        if x_dir>0 and y_dir==0: #right
            h = 180
        if x_dir>0 and y_dir==0: #left
            h = -180
        if x_dir==0 and y_dir>0: #down
            h = -90
        if x_dir==0 and y_dir<0: #up
            h = 90
        dist_w = WIDTH - x1
        dist_h = HEIGHT - y1
        dist_tail_x = x1 - x2
        dist_tail_y = y1 - y2
        dist_apple_x = x1 - s.posx
        dist_apple_y = y1 - s.posy
        
        norm_status = np.array([dist_w, dist_h, dist_tail_x,
                                dist_tail_y, dist_apple_x,
                                dist_apple_y, h])
        norm_status = preprocessing.normalize([norm_status])
        for i in range (7):
            status[i] = norm_status[0][1]
        control = m.predict1(status)
        print(control[0])
        control_list.append(control)
        status_list.append(status)

        s.drawScore()
        
        # Check for collision with gamefield edges
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
            m.training(np.array(status_list),bad_control(control_list))
            status_list = []
            control_list = []
            if s.score > s.best_score:
                s.best_score = s.score
            s.score = 0
            s.c.delete(s.BLOCK)
            s.create_block()
            s.restart_game()
            IN_GAME = True
            
        # Eating apples
        elif head_coords == s.c.coords(s.BLOCK):
            s.add_segment()
            s.c.delete(s.BLOCK)
            s.create_block()
            m.training(np.array(status_list), good_control(control_list))
            status_list = []
            control_list = []
            s.score += 1
            
        # Self-eating
        else:
            for index in range(len(s.segments)-1):
                if head_coords == s.c.coords(s.segments[index]):
                    IN_GAME = False
                    #print('status = ', len(status_list))
                    #print('control = ', len(control_list))
                    #print('len segments = ', len(s.c.coords(s.segments[index])))
                    #print('index = ', index)
                    if len(status_list) != 0 or len(control_list) != 0:
                        m.training(np.array(status_list), bad_control_self_eating(control_list))
                    if s.score > s.best_score:
                        s.best_score = s.score
                    s.score = 0
                    s.c.delete(s.BLOCK)
                    s.create_block()
                    s.restart_game()
                    IN_GAME = True

        s.movement(control)
        s.root.update()

def good_control(control):
    for j in range(int((len(control)/100)*10)):
        idx  = control[-j][0].argmax()
        control[-j][0] = [1 if i == idx else 0 for i in range(3)]
    return control

def bad_control(control):
    for j in range (int((len(control)/100)*20)):
        idx  = control[-j][0].argmax()
        control[-j][0] = [0 if i == idx else 1 for i in range(3)]
    return control

def bad_control_self_eating(control):
    idx  = control[-1][0].argmax()
    control[-1][0] = [0 if i == idx else 1 for i in range(3)]
    return control

main()
