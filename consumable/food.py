import pygame
import thinker.brain as brain

class Tree:
    size = 5

    Trees = []

    natural_energy_decay = 10
    natural_energy_gain = 5

    def __init__(self, pos = pygame.Vector2(100 , 100)):
        self.my_fruits = []
        self.energy = 5000
        self.pos = pygame.Vector2(pos)
        self.been_attacked = False

        Tree.Trees.append(self)
    
    def Update(dt, screen):
        for tree in Tree.Trees:
            tree.energy -= Tree.natural_energy_decay * dt
            tree.energy += Tree.natural_energy_gain * dt

            if brain.Brain.random_range(0 , 1) > .9:
                Tree.CreateFruit(tree)

    def CreateFruit(tree):
        Fruit((tree.pos.x + brain.Brain.random_range( -30 , 30), tree.pos.y + brain.Brain.random_range(-30 , 30)))

    def Draw(screen, draw_debugs = False):
        for tree in Tree.Trees:
            pygame.draw.circle(screen, "darkgreen", tree.pos, Tree.size)

class Fruit():
    size = 1

    fruits = []

    def __init__(self, pos = pygame.Vector2(100 , 100)):
        self.energy = 500
        self.lifetime = 1000
        self.alive = True
        self.pos = pygame.Vector2(pos)
        Fruit.fruits.append(self)

    def Update(dt):
        for fruit in Fruit.fruits:
            fruit.lifetime -= dt

    def decay():
        for fruit in Fruit.fruits:
            if fruit.lifetime <= 0 or not fruit.alive:
                Fruit.fruits.remove(fruit)

    def Draw(screen):
        for fruit in Fruit.fruits:
            pygame.draw.circle(screen, "green", fruit.pos, Fruit.size)