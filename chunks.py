import thinker.brain as brain
import os, pygame

os.system('cls')

class Chunks:
    def __init__(self, width = 800, height = 600 , chunk_divide = 2):
        self.chunk_divide = chunk_divide

        self.width = width
        self.height = height

        self.chunk_size = (self.chunk_divide * self.chunk_divide)

        self.chunk_lists = {
            "bug_chunks": [None] * self.chunk_size,
            "fruit_chunks": [None] * self.chunk_size,
            "tree_chunks":[None] * self.chunk_size,
        }
        
        self.chunk_screen_horizontal_size = self.width / self.chunk_size
        self.chunk_screen_vertical_size = self.height / self.chunk_size
    
    def Update_window_size(self, screen):
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.chunk_screen_horizontal_size = self.width / self.chunk_size
        self.chunk_screen_vertical_size = self.height / self.chunk_size

    def Update(self, list, chunk_name = None, even = True):
        if chunk_name is not None:
            chunks = self.chunk_lists[chunk_name] = [[] for _ in range(self.chunk_size)]

            for index, item in enumerate(list):
                grid_num = 0

                for i in range(self.chunk_divide):
                    for j in range(self.chunk_divide):
                        h = (j + 1) * (self.chunk_screen_horizontal_size * self.chunk_divide)
                        v = (i + 1) * (self.chunk_screen_vertical_size * self.chunk_divide)
                        if item.pos.x <= h and item.pos.y <= v:
                            item.quadrant = grid_num
                            chunks[grid_num].append(index)
                            break
                        grid_num += 1
                    else:
                        continue
                    break