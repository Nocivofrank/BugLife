import thinker.brain as brain
import os, pygame

os.system('cls')

class Chunks:
    def __init__(self, width = 800, height = 600 , chunk_divide = 2):
        self.chunk_divide = chunk_divide

        self.width = width
        self.height = height

        self.chunks = [None] * (self.chunk_divide * self.chunk_divide)
        self.foodChunks = [None] * (self.chunk_divide * self.chunk_divide)
        
        self.chunk_screen_horizontal_size = self.width / len(self.chunks)
        self.chunk_screen_vertical_size = self.height / len(self.chunks)

        grid_init_num = 0
        for i in range(self.chunk_divide):
            for j in range(self.chunk_divide):
                self.chunks[grid_init_num] = []
                grid_init_num += 1

        grid_init_num = 0
        for i in range(self.chunk_divide):
            for j in range(self.chunk_divide):
                self.foodChunks[grid_init_num] = []
                grid_init_num += 1
    
    def Update(self, list):
        Chunks.ResetChunk(self)
        count = 0
        for bug in list:
            grid_num = 0
            done = False
            counti = 1
            for i in range(self.chunk_divide):
                countj = 1
                for j in range(self.chunk_divide):
                    if not done:
                        h = countj * (self.chunk_screen_horizontal_size * self.chunk_divide)
                        v = counti * (self.chunk_screen_vertical_size * self.chunk_divide)
                        if (bug.pos.x <= h and bug.pos.y <= v):
                            bug.quadrant = grid_num
                            done = True
                            self.chunks[grid_num].append(count)
                    grid_num += 1
                    countj += 1
                counti += 1
            count += 1
    
    def Update_Food(self, list):
        Chunks.ResetFoodChunk(self)
        count = 0
        for bug in list:
            grid_num = 0
            done = False
            counti = 1
            for i in range(self.chunk_divide):
                countj = 1
                for j in range(self.chunk_divide):
                    if not done:
                        h = countj * (self.chunk_screen_horizontal_size * self.chunk_divide)
                        v = counti * (self.chunk_screen_vertical_size * self.chunk_divide)
                        if (bug.pos.x <= h and bug.pos.y <= v):
                            bug.quadrant = grid_num
                            done = True
                            self.chunks[grid_num].append(count)
                    grid_num += 1
                    countj += 1
                counti += 1
            count += 1

    def ResetFoodChunk(self):
        self.foodChunks = [None] * (self.chunk_divide * self.chunk_divide)
        
        grid_init_num = 0
        for i in range(self.chunk_divide):
            for j in range(self.chunk_divide):
                self.foodChunks[grid_init_num] = []
                grid_init_num += 1

    def ResetChunk(self):
        self.chunks = [None] * (self.chunk_divide * self.chunk_divide)
        
        grid_init_num = 0
        for i in range(self.chunk_divide):
            for j in range(self.chunk_divide):
                self.chunks[grid_init_num] = []
                grid_init_num += 1