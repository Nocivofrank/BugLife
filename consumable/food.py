import pygame
import thinker.brain as brain

class Tree:
    size = 5

    Trees = []

    natural_energy_decay = 10
    natural_energy_gain = 5

    def __init__(self, pos = pygame.Vector2(100 , 100)):
        self.energy = 2000
        self.pos = pygame.Vector2(pos)
        self.quadrant = None
        self.alive = True

        Tree.Trees.append(self)
    
    def Update(dt, screen, gameChunk):
        for tree in Tree.Trees:
            chunk = gameChunk.chunk_lists["fruit_chunks"]

            density = len(Tree.Trees) / 1000

            tree.energy += Tree.natural_energy_gain * dt
            tree.energy -= Tree.natural_energy_decay * density * dt

            if tree.quadrant is not None:
                if brain.Brain.random_range(0 , 1) > .995:
                    Tree.CreateFruit(tree)

            if tree.energy <= 0:
                tree.alive = False

    def decay():
        for tree in Tree.Trees:
            if not tree.alive:
                Tree.Trees.remove(tree)

    def CreateFruit(tree):
        Fruit((tree.pos.x + brain.Brain.random_range( -30 , 30), tree.pos.y + brain.Brain.random_range(-30 , 30)))

    def Draw(screen, draw_debugs = False):
        for tree in Tree.Trees:
            pygame.draw.circle(screen, "darkgreen", tree.pos, Tree.size)

    def MasterUpdate(dt, screen, gameChunk):
        Tree.decay()
        Tree.Update(dt, screen=screen, gameChunk=gameChunk)
        Tree.Draw(screen=screen)

class Fruit():
    size = 1

    fruits = []

    def __init__(self, pos = pygame.Vector2(100 , 100)):
        self.energy = 500
        self.lifetime = 10000
        self.alive = True
        self.quadrant = None
        self.pos = pygame.Vector2(pos)
        Fruit.fruits.append(self)

    def Update(dt, gameChunk):
        for fruit in Fruit.fruits:
            fruit.lifetime -= dt
            if fruit.lifetime <= 0 or not fruit.alive:
                fruit.alive = False
                fruit.energy = 0
            else:
                chunk = gameChunk.chunk_lists["fruit_chunks"]
                if fruit.quadrant is not None:
                    if len(chunk[fruit.quadrant]) != 0:
                        if (brain.Brain.random_range(0 , 1) / len(chunk[fruit.quadrant])) > .9999:
                            fruit.alive = False
                            Tree(pos= (fruit.pos.x, fruit.pos.y))


    def decay():
        for fruit in Fruit.fruits:
            if fruit.alive is False:
                Fruit.fruits.remove(fruit)        

    def Draw(screen):
        for fruit in Fruit.fruits:
            pygame.draw.circle(screen, "green", fruit.pos, Fruit.size)

    def MasterUpdate(dt, screen, gameChunk):
        Fruit.Update(dt, gameChunk)
        Fruit.Draw(screen=screen)