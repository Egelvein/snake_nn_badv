import random
from tkinter import Tk, Canvas

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20

class Snake(object):
    """ Simple Snake class """
    def __init__(self):
        #print('OKNO')
        self.root = Tk()
        self.root.title("Game 'Snake'")
        self.c = Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#003300")
        self.c.grid()
        #self.root.mainloop()
        self.segments = [self.create_snake_part(SEG_SIZE, SEG_SIZE),
                         self.create_snake_part(SEG_SIZE*2, SEG_SIZE),
                         self.create_snake_part(SEG_SIZE*3, SEG_SIZE)]
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.vector = self.mapping["Right"]
        self.last_move = 1
        self.create_block()
        
    def add_segment(self):
        """ Adds segment to the snake """
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, self.create_snake_part(x, y))
        
    def change_direction(self, event):
        """ Changes direction of snake """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]
            
    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)
            
    def create_block(self):
        """ Creates an apple to be eaten """
        self.posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
        self.posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
        self.BLOCK = self.c.create_oval(self.posx, self.posy, self.posx+SEG_SIZE, self.posy+SEG_SIZE, fill="red")
        return self.BLOCK
    
    " Single snake segment """
    def create_snake_part(self, x, y):
        #print(self.c.coords)
        return self.c.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="white")
    
    def movement(self, control = []):
        self.contr = control[0].argmax()
        if self.last_move == 1:
            if self.contr == 0: #поворот налево
                self.vector = (-1, 0) 
                self.last_move = 0
            elif self.contr == 1: #поворот направо
                self.vector = (1, 0)
                self.last_move = 1
            elif self.contr == 2: #движение прямо
                self.vector = (0, 1)
                self.last_move = 2
        elif self.last_move == 0:
            if self.contr == 0: #поворот налево
                self.vector = (0, -1) 
                self.last_move = 0
            elif self.contr == 1: #поворот направо
                self.vector = (0, 1)
                self.last_move = 1
            elif self.contr == 2: #движение прямо
                self.vector = (-1, 0)
                self.last_move = 3
        elif self.last_move == 2:
            if self.contr == 0: #поворот налево
                self.vector = (-1, 0) 
                self.last_move = 0
            elif self.contr == 1: #поворот направо
                self.vector = (1, 0)
                self.last_move = 1
            elif self.contr == 2: #движение прямо
                self.vector = (0, 1)
                self.last_move = 2
        else:
            if self.contr == 0: #поворот налево
                self.vector = (0, -1) 
                self.last_move = 0
            elif self.contr == 1: #поворот направо
                self.vector = (0, 1)
                self.last_move = 1
            elif self.contr == 2: #движение прямо
                self.vector = (-1, 0)
                self.last_move = 3
                
        for index in range(len(self.segments)-1):
            segment = self.segments[index]
            x1, y1, x2, y2 = self.c.coords(self.segments[index+1])
            self.c.coords(segment, x1, y1, x2, y2)
            
        x1, y1, x2, y2 = self.c.coords(self.segments[-2])
        self.c.coords(self.segments[-1],
                      x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                      x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

                






