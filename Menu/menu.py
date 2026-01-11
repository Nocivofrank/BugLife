from tkinter import *
from tkinter import ttk
import thinker.bug as Bug

def Menu():
    root = Tk()

    bug = None
    selected_id = 5
    text_rows = 0

    def Update():
        nonlocal text_rows
        nonlocal selected_id

        def die():
            bug.alive = False

        bug_id.config(text= f"ID: {selected_id}")
        count = 0 
        for bug_check in Bug.Bug.bugs:
            if bug_check.alive:
                count += 1
        total_bugs.config(text=f"Total Bugs: {count}")

        if selected_id > count:
            selected_id = 1
        if selected_id < 1:
            selected_id = count - 1
        
        if Bug.Bug.getBug(selected_id) is not None:
            bug = Bug.Bug.getBug(selected_id)

            bug_pos.config(text= f"Bug Pos: {bug.pos.x:.2f} , {bug.pos.y:.2f}")
            bug_direction.config(text= f"Bug Direction: {bug.direction.x:.2f} , {bug.direction.y:.2f}")
            bug_energy.config(text= f"Bug energy: {bug.energy:.2f}")
            bugs_detected.config(text= f"Bugs Nearby: {bug.amount_near}/{Bug.Bug.amount_detect_max}")

            if bug.attacking:
                bug_attacking.config(text= "Bug Attacking: True")
            else:
                bug_attacking.config(text= "Bug Attacking: False")
            if bug.been_attacked:
                bug_been_attacked.config(text= "Been Attacked: True")
            else:
                bug_been_attacked.config(text= "Been Attacked: False")
            
            bug_energy_gained.config(text= f"Enemy energy taken: {bug.amount_energy_gained:.2f}")
            bug_energy_lost.config(text= f"Enemy taken energy: {bug.amount_energy_lost:.2f}")
            bug_apple_eat_cooldown.config(text= f"Eating Cooldown: {bug.eat_cooldown_timer:.2f}")

            bug_neuron_input.config(text= f"Input Neurons: {bug.brain.hidden_size[0]}")
            bug_neuron_layer1.config(text= f"Neuron Layer 1: {bug.brain.hidden_size[1]}")
            bug_neuron_layer2.config(text= f"Neuron Layer 2: {bug.brain.hidden_size[2]}")
            bug_neuron_layer3.config(text= f"Neuron Layer 3: {bug.brain.hidden_size[3]}")
            bug_neuron_layer4.config(text= f"Neuron Layer 4: {bug.brain.hidden_size[4]}")
            bug_neuron_layer5.config(text= f"Neuron Layer 5: {bug.brain.hidden_size[5]}")
            bug_neuron_layer6.config(text= f"Neuron Layer 6: {bug.brain.hidden_size[6]}")
            bug_neuron_output.config(text= f"Output Neurons: {bug.brain.hidden_size[7]}")

            death_button.grid(column=0, row=text_rows)
            death_button.config(text="Kill Bug" ,command=die)
            text_rows += 1

        else:
            bug_pos.config(text="No bug :(")
        root.update_idletasks()
        root.after(25 ,Update)

    total_bugs = ttk.Label(root, text="")
    total_bugs.grid(column=0, row=text_rows)
    text_rows += 1

    menu_row = ttk.Label(root, text="=================================")
    menu_row.grid(row=text_rows)
    text_rows += 1

    bug_pos = ttk.Label(root, text="")
    bug_pos.grid(column=0, row=text_rows)
    bug_id = ttk.Label(root, text="")
    bug_id.grid(column=1, row=text_rows)
    text_rows += 1
    bug_direction = ttk.Label(root, text="")
    bug_direction.grid(column=0, row=text_rows)
    text_rows += 1

    bug_energy = ttk.Label(root, text="")
    bug_energy.grid(column=0, row=text_rows)
    text_rows += 1

    bugs_detected = ttk.Label(root, text="")
    bugs_detected.grid(column=0, row=text_rows)
    text_rows += 1

    bug_attacking = ttk.Label(root, text="")
    bug_attacking.grid(column=0, row=text_rows)
    text_rows += 1

    bug_been_attacked = ttk.Label(root, text="")
    bug_been_attacked.grid(column=0, row=text_rows)
    text_rows += 1
    
    bug_energy_gained = ttk.Label(root, text="")
    bug_energy_gained.grid(column=0, row=text_rows)
    text_rows += 1

    bug_energy_lost = ttk.Label(root, text="")
    bug_energy_lost.grid(column=0, row=text_rows)
    text_rows += 1

    bug_apple_eat_cooldown = ttk.Label(root, text="")
    bug_apple_eat_cooldown.grid(column=0, row=text_rows)
    text_rows += 1

    menu_row1 = ttk.Label(root, text="=================================")
    menu_row1.grid(row=text_rows)
    text_rows += 1

    #Neuron Count
    bug_neuron_input = ttk.Label(root, text="")
    bug_neuron_input.grid(column=0, row=text_rows)
    text_rows += 1

    bug_neuron_layer1 = ttk.Label(root, text="")
    bug_neuron_layer1.grid(column=0, row=text_rows)
    text_rows += 1

    bug_neuron_layer2 = ttk.Label(root, text="")
    bug_neuron_layer2.grid(column=0, row=text_rows)
    text_rows += 1

    bug_neuron_layer3 = ttk.Label(root, text="")
    bug_neuron_layer3.grid(column=0, row=text_rows)
    text_rows += 1

    bug_neuron_layer4 = ttk.Label(root, text="")
    bug_neuron_layer4.grid(column=0, row=text_rows)
    text_rows += 1

    bug_neuron_layer5 = ttk.Label(root, text="")
    bug_neuron_layer5.grid(column=0, row=text_rows)
    text_rows += 1

    bug_neuron_layer6 = ttk.Label(root, text="")
    bug_neuron_layer6.grid(column=0, row=text_rows)
    text_rows += 1

    bug_neuron_output = ttk.Label(root, text="")
    bug_neuron_output.grid(column=0, row=text_rows)
    text_rows += 1

    def increment_id():
        nonlocal selected_id
        selected_id += 1
    def decrease_id():
        nonlocal selected_id
        selected_id -= 1

    increment_button = ttk.Button(root, text= "ID+", command=increment_id)
    increment_button.grid(column=0 , row=text_rows)
    decrease_button = ttk.Button(root, text="ID--", command=decrease_id)
    decrease_button.grid(column=0, row=text_rows, sticky="w")
    death_button = ttk.Button(root)
    text_rows += 1

    Update()
    root.mainloop()