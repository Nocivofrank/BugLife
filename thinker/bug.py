import pygame, consumable.food as food
import thinker.brain as Brain

class Bug():
    size = 1

    amount_detect_max = 20
    detection_range = 100 * size
    attack_range = 10 * size
    reproduction_energy_minimum = 1000

    bugs = []

    def __init__(self, id , pos = pygame.Vector2(100 , 100), energy_passed = 1000, brain = None):
        #information passed to brain
        self.pos = pygame.Vector2(pos)
        self.distance_to_sides = [0] * 4
        self.direction = pygame.Vector2(0 , 0)
        self.speed = 10 / Bug.size
        self.energy = energy_passed
        self.attack = 10
        self.been_attacked = False
        self.eat_cooldown = 5
        self.eat_cooldown_timer = 0
        self.quadrant = None

        # Catalogs the nearest bug
        self.closest_other = [None] * Bug.amount_detect_max
        self.very_closest_other = None
        self.very_closest_other_distance = float("inf")

        #Catalogs the nearest tree
        self.closest_tree = [None] * Bug.amount_detect_max
        self.very_closest_tree = None
        self.very_closest_tree_distance = float("inf")
        
        #Catalogs the nearest fruit
        self.closest_fruit = [None] * Bug.amount_detect_max
        self.very_closest_fruit = None
        self.very_closest_fruit_distance = float("inf")

        self.amount_near = 0
        self.amount_energy_lost = 0
        self.amount_energy_gained = 0
        self.willing_to_reproduce = False
        self.time_alive = 0
        self.edgin = False

        self.attacking = False
        self.vel = pygame.Vector2(0, 0)

        if brain is None:
            self.brain = Brain.Brain(10)
        else:
            self.brain = brain

        self.alive = True

        self.id = id
        self.selected = False
        self.brain.brainMutate()
        Bug.bugs.append(self)

    def update_detect(dt, chunk):
        for bug in Bug.bugs:

            # ---------- BUG DETECTION ----------
            bug.closest_other = [None] * Bug.amount_detect_max
            bug.very_closest_other = None
            bug.very_closest_other_distance = float("inf")

            if bug.quadrant is not None:
                list = chunk.chunks[bug.quadrant]

                for i in range(len(list)):
                    other_bug = Bug.bugs[list[i]]
                    if other_bug is bug:
                        continue

                    distance = bug.pos.distance_to(other_bug.pos)

                    if distance < Bug.detection_range:
                        if distance < bug.very_closest_other_distance:
                            bug.very_closest_other_distance = distance
                            bug.very_closest_other = other_bug

                        if None in bug.closest_other:
                            bug.closest_other[bug.closest_other.index(None)] = other_bug
                        else:
                            farthest_index = max(
                                range(Bug.amount_detect_max),
                                key=lambda i: bug.pos.distance_to(bug.closest_other[i].pos)
                            )

                            if distance < bug.pos.distance_to(
                                bug.closest_other[farthest_index].pos
                            ):
                                bug.closest_other[farthest_index] = other_bug

            bug.amount_near = sum(1 for b in bug.closest_other if b)

            # ---------- FRUIT DETECTION ----------
            bug.closest_fruit = [None] * Bug.amount_detect_max
            bug.very_closest_fruit = None
            bug.very_closest_fruit_distance = float("inf")

            if bug.quadrant is not None:
                list = chunk.foodChunks[bug.quadrant]

                for i in range(len(list)):
                    fruit = food.Fruit.fruits[list[i]]
                    distance = bug.pos.distance_to(fruit.pos)

                    if distance < Bug.detection_range:
                        if distance < bug.very_closest_fruit_distance:
                            bug.very_closest_fruit_distance = distance
                            bug.very_closest_fruit = fruit

                        if None in bug.closest_fruit:
                            bug.closest_fruit[bug.closest_fruit.index(None)] = fruit
                        else:
                            farthest_index = max(range(Bug.amount_detect_max),key=lambda i: bug.pos.distance_to(bug.closest_fruit[i].pos))
                            if distance < bug.pos.distance_to(bug.closest_fruit[farthest_index].pos):
                                bug.closest_fruit[farthest_index] = fruit

    def update(dt, screen):
        for bug in Bug.bugs:
            if bug.energy <= 0:
                bug.alive = False
                continue
            else:
                bug.brain.extract_information(bug)

                out, energy_consumed = bug.brain.brainThink()
                bug.energy -= energy_consumed

                #Bug Controls where they go
                bug.direction.x = out[0] - out[1]
                bug.direction.y = out[2] - out[3]
                bug.speed = (out[4]) / (Bug.size * 500)

                bug.energy -= bug.speed / 100

                #This is where the attack is being handled
                if out[5] > .8:
                    bug.attacking = True
                    target = bug.very_closest_other


                    if target is not None and target.energy > 0:
                        distance = bug.pos.distance_to(target.pos)
                        if distance <= Bug.attack_range:
                            damage = min(bug.attack, target.energy)

                            target.energy -= damage
                            bug.energy += damage

                            bug.amount_energy_gained += damage
                            target.amount_energy_lost += damage

                            target.been_attacked = True
                else:
                    bug.attacking = False

                if bug.eat_cooldown_timer < bug.eat_cooldown:
                    bug.eat_cooldown_timer += dt

                if out[6] > .5 and bug.eat_cooldown_timer >= bug.eat_cooldown:
                    target_fruit = bug.very_closest_fruit
                    if target_fruit is not None:
                        distance = bug.pos.distance_to(target_fruit.pos)
                        if distance <= Bug.attack_range:
                            bug.energy += target_fruit.energy
                            bug.eat_cooldown_timer = 0
                            target_fruit.alive = False

                # REPORUDCE THIGNS HI
                if out[6] > .8 and bug.energy >= Bug.reproduction_energy_minimum:
                    bug.willing_to_reproduce = True
                    target = bug.very_closest_other

                    if target is not None:
                        distance = bug.pos.distance_to(target.pos)
                        if target.willing_to_reproduce and distance <= Bug.attack_range:
                            bug.energy -= 500
                            target.energy -= 500
                            dx = (bug.pos.x + target.pos.x) / 2
                            dy = (bug.pos.y + target.pos.y) / 2
                            if bug.time_alive > target.time_alive:
                                Bug(len(Bug.bugs), pos= (dx, dy), energy_passed= 500, brain=bug.brain)
                            else:
                                Bug(len(Bug.bugs), pos= (dx, dy), energy_passed= 500, brain=target.brain)

                if bug.direction.length_squared() > 0:
                    bug.direction = bug.direction.normalize()
                    bug.energy -= 0.01

                bug.vel += bug.direction * bug.speed * dt
                bug.vel *= 0.85
                bug.pos += bug.vel * dt

                wrap_padding = 4

                # wrap around edges
                if bug.pos.x  < -Bug.size * wrap_padding:
                    bug.pos.x = screen.get_width() + Bug.size
                elif bug.pos.x > screen.get_width() + Bug.size * wrap_padding:
                    bug.pos.x = -Bug.size

                if bug.pos.y < -Bug.size * wrap_padding:
                    bug.pos.y = screen.get_height() + Bug.size
                elif bug.pos.y > screen.get_height() + Bug.size * wrap_padding:
                    bug.pos.y = -Bug.size

                # # clamp
                # bug.pos.x = max(Bug.size, min(screen.get_width() - Bug.size, bug.pos.x))
                # bug.pos.y = max(Bug.size, min(screen.get_height() - Bug.size, bug.pos.y))

                bug.distance_to_sides[0] = bug.pos.x
                bug.distance_to_sides[1] = screen.get_width() - bug.pos.x
                bug.distance_to_sides[2] = bug.pos.y
                bug.distance_to_sides[3] = screen.get_height() - bug.pos.y

                bug.edging = False
                for i in range(4):
                    if bug.distance_to_sides[i] < 10:
                        bug.energy -= 10
                        bug.edging = True

                bug.time_alive += dt


    def update_attacks():
        for bug in Bug.bugs:
            bug.been_attacked = False

    def draw(screen, draw_debug = False):
        for bug in Bug.bugs:
            if bug.selected:
                pygame.draw.circle(screen, "green", bug.pos, Bug.size)
            elif bug.edging:
                pygame.draw.circle(screen, "purple", bug.pos, Bug.size)
            else:
                pygame.draw.circle(screen, "red", bug.pos, Bug.size)

            line_length = 3 * Bug.size
            end_pos = bug.pos + bug.direction * line_length
            pygame.draw.aaline(screen, "yellow", bug.pos, end_pos)

            if draw_debug:
                for i in range(Bug.amount_detect_max):
                    if bug.closest_other[i] != None:
                        distance = bug.pos.distance_to(bug.closest_other[i].pos)
                        if distance <= Bug.detection_range:
                            pygame.draw.aaline(screen, "green", bug.pos, bug.closest_other[i].pos)

                    if bug.closest_fruit[i] != None:
                        distance = bug.pos.distance_to(bug.closest_fruit[i].pos)
                        if distance <= Bug.detection_range:
                            pygame.draw.aaline(screen, "red", bug.pos, bug.closest_fruit[i].pos)

    def death():
        for bug in Bug.bugs:
            if not bug.alive:
                Bug.bugs.remove(bug)

    def getBug(id, debug = False):
        # for bug in Bug.bugs:
        #     bug.selected = False
        # for bug in Bug.bugs:
        #     if bug.id == id:
        #         if debug:
        #             print("Returning Bug: ", bug , bug.id)
        #         bug.selected = True
        #         return bug
        return None