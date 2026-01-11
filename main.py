import pygame as py
import os, threading, chunks as ch, consumable.food as food, Menu.menu as menu
import thinker.bug as bug
os.system("cls ")

lock = threading.Lock()

screen = py.display.set_mode((1280, 720))
clock = py.time.Clock()
dt = 0

amount_bugs_create = 500
show_menu = True

skip_frames = 3
skipped_frames = 0

shared_info = {
    "running": True,
    "bugs_ready": False,
    "amount_bugs_loaded": 0
}

def Menu():
    for i in range(amount_bugs_create):
        bug.Bug(id=i, pos= (bug.Brain.Brain.random_range( 0 , screen.get_width()) , bug.Brain.Brain.random_range( 0 , screen.get_height())))
        shared_info["amount_bugs_loaded"] += 1
    print("Done")
    shared_info["bugs_ready"] = True
    menu.Menu()
    if show_menu:
        shared_info["running"] = False

threading.Thread(target=Menu , daemon=True).start()

game_Chunk = ch.Chunks(screen.get_width(), screen.get_height(), 5)

py.init()
font = py.font.Font(None, 36)

while shared_info["running"]:
    for event in py.event.get():
        if event.type == py.QUIT:
            shared_info["running"] = False
    screen.fill("black")

    if shared_info["bugs_ready"]:
        updated_bug_list = []
        for checked_bug in bug.Bug.bugs:
            if checked_bug.alive:
                updated_bug_list.append(checked_bug)
        count = 0 
        for i in updated_bug_list:
            if i.alive:
                count += 1

        bug.Bug.bugs = updated_bug_list

        game_Chunk.Update(bug.Bug.bugs)

        bug.Bug.death()
        if skipped_frames >= skip_frames:
            bug.Bug.update_detect(dt, game_Chunk)
            skipped_frames = 0
        else:
            skipped_frames += 1
        bug.Bug.update(dt, screen)
        bug.Bug.update_attacks()
        bug.Bug.draw(screen)

        food.Tree.Update(dt, screen=screen)
        food.Tree.Draw(screen=screen)

        food.Fruit.Update(dt)
        food.Fruit.Draw(screen=screen)
        food.Fruit.decay()

        if len(food.Tree.Trees) <= 100:
            food.Tree(pos= (bug.Brain.Brain.random_range( 0 , screen.get_width()) , bug.Brain.Brain.random_range( 0 , screen.get_height())))

        if len(bug.Bug.bugs) <= 100:
            bug.Bug(1, pos= (bug.Brain.Brain.random_range( 0 , screen.get_width()) , bug.Brain.Brain.random_range( 0 , screen.get_height())))
    else:
        text = font.render(f"Loading...", True , (255, 255, 255))
        loaded_stat = font.render(f" Amount bugs loaded: {shared_info['amount_bugs_loaded']}/{amount_bugs_create}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()/2 - 60, screen.get_height()/2 - 50))
        screen.blit(loaded_stat, (screen.get_width()/2 - 170, screen.get_height()/2 -20))
    py.display.flip()
    dt = clock.tick(60)
py.quit()