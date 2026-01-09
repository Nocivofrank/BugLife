import pygame
import brain as Brain

class Bug():
    size = 10

    amount_detect_max = 2

    bugs = []

    def __init__(self, id , pos = pygame.Vector2(100 , 100)):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(0 , 0)
        self.speed = 1000
        self.brain = Brain.Brain()

        self.alive = True

        self.closest_other = [None] * Bug.amount_detect_max

        self.brain.brainMutate()
        Bug.bugs.append(self)

    def update(dt, screen):
        for bug in Bug.bugs:
            for other_bug in Bug.bugs:
                if other_bug == bug:
                    continue

                distance = bug.pos.distance_to(other_bug.pos)

                # Check if we have an empty slot
                if None in bug.closest_other:
                    # Find the first empty slot
                    empty_index = bug.closest_other.index(None)
                    bug.closest_other[empty_index] = other_bug
                else:
                    # Find the farthest bug currently stored
                    farthest_index = 0
                    max_distance = bug.pos.distance_to(bug.closest_other[0].pos)

                    for i in range(1, Bug.amount_detect_max):
                        d = bug.pos.distance_to(bug.closest_other[i].pos)
                        if d > max_distance:
                            max_distance = d
                            farthest_index = i

                    # If the new bug is closer than the farthest, replace it
                    if distance < max_distance:
                        bug.closest_other[farthest_index] = other_bug

            bug.brain.extract_information(bug)

            out = bug.brain.brainThink()
            bug.direction.x = out[0] - out[1]
            bug.direction.y = out[2] - out[3]

            if out[4] > .85:
                bug.brain.brainMutate()

            if bug.direction.length() != 0:
                bug.direction = bug.direction.normalize()
            bug.vel += bug.direction * (bug.speed) * dt
            bug.vel *= 0.85
            bug.pos += bug.vel * dt

            #wrap around edges
            if bug.pos.x < -Bug.size:
                bug.pos.x = screen.get_width() + Bug.size
            elif bug.pos.x > screen.get_width() + Bug.size:
                bug.pos.x = -Bug.size

            if bug.pos.y < -Bug.size:
                bug.pos.y = screen.get_height() + Bug.size
            elif bug.pos.y > screen.get_height() + Bug.size:
                bug.pos.y = -Bug.size

    def draw(screen):
        for bug in Bug.bugs:
            pygame.draw.circle(screen, "red", bug.pos, Bug.size)
            line_length = 30
            end_pos = bug.pos + bug.direction * line_length
            pygame.draw.aaline(screen, "yellow", bug.pos, end_pos)

            for i in range(Bug.amount_detect_max):
                if bug.closest_other[i] != None:
                    pygame.draw.aaline(screen, "green", bug.pos, bug.closest_other[i].pos)

    def death():
        for bug in Bug.bugs:
            if not bug.alive:
                Bug.bugs.remove(bug)