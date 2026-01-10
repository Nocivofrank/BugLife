from tkinter import *
from tkinter import ttk
import bug as Bug

def Menu():
    root = Tk()
    root.geometry("250x100")

    bug = None
    selected_id = 5

    def Update():
        def die():
            bug.alive = False

        bug_id.config(text= f"ID: {selected_id}")
        if Bug.Bug.getBug(selected_id) is not None:
            bug = Bug.Bug.getBug(selected_id)
            bug_pos.config(text= f"Bug Pos: {bug.pos.x:.2f} , {bug.pos.y:.2f}")
            bug_direction.config(text= f"Bug Direction: {bug.direction.x:.2f} , {bug.direction.y:.2f}")
            death_button.grid(column=0, row=6)
            death_button.config(text="Kill Bug" ,command=die)

        else:
            bug_pos.config(text="No bug :(")
        root.after(25 ,Update)

    bug_pos = ttk.Label(root, text="")
    bug_pos.grid(column=0, row=0)
    bug_direction = ttk.Label(root, text="")
    bug_direction.grid(column=0, row=1)
    bug_id = ttk.Label(root, text="")
    bug_id.grid(column=1, row=0)

    def increment_id():
        nonlocal selected_id
        selected_id += 1
    def decrease_id():
        nonlocal selected_id
        selected_id -= 1

    increment_button = ttk.Button(root, text= "ID+", command=increment_id)
    increment_button.grid(column=1 , row=5)
    decrease_button = ttk.Button(root, text="ID--", command=decrease_id)
    decrease_button.grid(column=0, row=5)
    death_button = ttk.Button(root)


    Update()
    root.mainloop()