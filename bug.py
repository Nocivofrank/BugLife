import pygame
import brain as Brain

class Bug():
    size = 5

    amount_detect_max = 10
    detection_range = 5 * size

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
        self.id = id
        self.selected = False
        Bug.bugs.append(self)

    def update_detect(dt):
        for bug in Bug.bugs:
            bug.closest_other = [None] * Bug.amount_detect_max
            for other_bug in Bug.bugs:
                if other_bug == bug:
                    continue
                
                if other_bug in bug.closest_other:
                    continue

                distance = bug.pos.distance_to(other_bug.pos)

                if distance < Bug.detection_range:
                    if None in bug.closest_other:
                        empty_index = bug.closest_other.index(None)
                        bug.closest_other[empty_index] = other_bug
                    else:
                        farthest_index = 0
                        max_distance = bug.pos.distance_to(bug.closest_other[0].pos)

                        for i in range(1, Bug.amount_detect_max):
                            d = bug.pos.distance_to(bug.closest_other[i].pos)
                            if d > max_distance:
                                max_distance = d
                                farthest_index = i

                        if distance < max_distance:
                            bug.closest_other[farthest_index] = other_bug

    def update(dt, screen):
        for bug in Bug.bugs:
            bug.brain.extract_information(bug)

            out = bug.brain.brainThink()
            bug.direction.x = out[0] - out[1]
            bug.direction.y = out[2] - out[3]

            if out[4] > .5:
                bug.direction.x = 0
                bug.direction.y = 0

            if bug.direction.length() != 0:
                bug.direction = bug.direction.normalize()
            bug.vel += bug.direction * (bug.speed) * dt
            bug.vel *= 0.85
            bug.pos += bug.vel * dt

            wrap_padding = 4

            #wrap around edges
            if bug.pos.x  < -Bug.size * wrap_padding:
                bug.pos.x = screen.get_width() + Bug.size
            elif bug.pos.x > screen.get_width() + Bug.size * wrap_padding:
                bug.pos.x = -Bug.size

            if bug.pos.y < -Bug.size * wrap_padding:
                bug.pos.y = screen.get_height() + Bug.size
            elif bug.pos.y > screen.get_height() + Bug.size * wrap_padding:
                bug.pos.y = -Bug.size
    
    def draw(screen, draw_debug = False):
        for bug in Bug.bugs:
            if bug.selected:
                pygame.draw.circle(screen, "green", bug.pos, Bug.size)
            else:
                pygame.draw.circle(screen, "red", bug.pos, Bug.size)

            line_length = 3 * Bug.size
            end_pos = bug.pos + bug.direction * line_length
            pygame.draw.aaline(screen, "yellow", bug.pos, end_pos)

            if draw_debug:
                for i in range(Bug.amount_detect_max):
                    if bug.closest_other[i] != None:
                        pygame.draw.aaline(screen, "green", bug.pos, bug.closest_other[i].pos)

    def death():
        for bug in Bug.bugs:
            if not bug.alive:
                Bug.bugs.remove(bug)

    def getBug(id, debug = False):
        for bug in Bug.bugs:
            bug.selected = False
        for bug in Bug.bugs:
            if bug.id == id:
                if debug:
                    print("Returning Bug: ", bug , bug.id)
                bug.selected = True
                return bug
        return None