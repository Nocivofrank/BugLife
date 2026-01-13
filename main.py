import pygame as py
import threading, chunks as ch, consumable.food as food, Menu.menu as menu
import thinker.bug as bug

lock = threading.Lock()

screen = py.display.set_mode((1280, 720), py.RESIZABLE, py.SRCALPHA)
clock = py.time.Clock()
dt = 0

amount_bugs_create = 2000
amount_trees_create = 100
global_size = 2

bug.Bug.size *= global_size
food.Fruit.size *= global_size
food.Tree.size *= global_size

skip_frames = 1
skipped_frames = 0
debug = False
show_menu = True

shared_info = {
    "running": True,
    "bugs_ready": False,
    "amount_bugs_loaded": 0,
    "dt": 0,
    "screen": None
}

def Menu():
    for i in range(amount_bugs_create):
        bug.Bug(id=i, pos= (bug.Brain.Brain.random_range( 0 , screen.get_width()) , bug.Brain.Brain.random_range( 0 , screen.get_height())))
        shared_info["amount_bugs_loaded"] += 1
    print("Done")
    shared_info["bugs_ready"] = True
    # menu.Menu()
    # while shared_info["running"]:
        # bug.Bug.think(dt=shared_info["dt"])
    # if show_menu:
    #     shared_info["running"] = False

threading.Thread(target=Menu , daemon=True).start()

game_Chunk = ch.Chunks(screen.get_width(), screen.get_height(), 20)

py.init()
font = py.font.Font(None, 36)

while shared_info["running"]:
    for event in py.event.get():
        if event.type == py.QUIT:
            shared_info["running"] = False
        if event.type == py.WINDOWRESIZED:
            game_Chunk.Update_window_size(screen)
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                debug = not debug

    screen.fill("black")

    shared_info["dt"] = dt
    shared_info["screen"] = screen

    if shared_info["bugs_ready"]:
        bug.Bug.death()
        food.Fruit.decay()

        game_Chunk.Update(bug.Bug.bugs, "bug_chunks")
        game_Chunk.Update(food.Fruit.fruits, "fruit_chunks")
        game_Chunk.Update(food.Tree.Trees, "tree_chunks")

        bug.Bug.MasterUpdate(dt,screen, debug)
        food.Tree.MasterUpdate(dt, screen, game_Chunk)
        food.Fruit.MasterUpdate(dt, screen, game_Chunk)

        bug.Bug.think(dt=shared_info["dt"])

        if skipped_frames >= skip_frames:
            bug.Bug.update_detect(dt, game_Chunk)
            skipped_frames = 0
        else:
            skipped_frames += 1

        if len(food.Tree.Trees) < amount_trees_create:
            food.Tree(pos=(bug.Brain.Brain.random_range( 0 , screen.get_width()) , bug.Brain.Brain.random_range( 0 , screen.get_height())))
        if len(bug.Bug.bugs) < amount_bugs_create / 10:
            bug.Bug( id = len(bug.Bug.bugs) ,pos=(bug.Brain.Brain.random_range( 0 , screen.get_width()) , bug.Brain.Brain.random_range( 0 , screen.get_height())), energy_passed=1000)

    else:
        text = font.render(f"Loading...", True , (255, 255, 255))
        loaded_stat = font.render(f" Amount bugs loaded: {shared_info['amount_bugs_loaded']}/{amount_bugs_create}", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()/2 - 60, screen.get_height()/2 - 50))
        screen.blit(loaded_stat, (screen.get_width()/2 - 170, screen.get_height()/2 -20))
    py.display.flip()
    dt = clock.tick()
py.quit()