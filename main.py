import pygame as py
import bug
import os

os.system("cls ")

py.init()
screen = py.display.set_mode((1280, 720))
clock = py.time.Clock()
running = True
dt = 0

for i in range(100):
    bug.Bug(id=i)

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    screen.fill("black")

    bug.Bug.death()
    bug.Bug.update(dt, screen)
    bug.Bug.draw(screen)

    py.display.flip()

    dt = clock.tick(60) / 1000
py.quit()