import numpy as np
import thinker.bug as bg
import secrets

class Brain():    
    minimum_neuron_input = 27
    def __init__(self, input_neuron_min_limit = 0):
        self.neuron_input = input_neuron_min_limit + Brain.minimum_neuron_input

        self.hidden_size = [
            self.neuron_input,
            200,
            200,
            9
        ]

        self.W = []
        self.B = []

        for i in range(len(self.hidden_size) - 1):
            in_size = self.hidden_size[i]
            out_size = self.hidden_size[i + 1]

            self.W.append(np.array([[Brain.random_range(-1, 1) for _ in range(in_size)]for _ in range(out_size)]))

            self.B.append(np.array([Brain.random_range(-1, 1) for _ in range(out_size)]))

        self.information = np.zeros(self.neuron_input)

    def getWeights(self):
        return self.W
    
    def setWeights(self, inputW):
        self.W = inputW

    def getBias(self):
        return self.B
    
    def setBias(self, inputB):
        self.B = inputB

    def sigmoid(x):
        out = np.empty_like(x, dtype=float)

        pos_mask = x >= 0
        neg_mask = ~pos_mask

        # safe for positive x
        out[pos_mask] = 1 / (1 + np.exp(-x[pos_mask]))

        # safe for negative x
        ex = np.exp(x[neg_mask])
        out[neg_mask] = ex / (1 + ex)

        return out

    def extract_information(self , bug):
        self.information = np.zeros(self.neuron_input)
        self.information[0] = bug.pos.x
        self.information[1] = bug.pos.y
        self.information[2] = bug.direction.x
        self.information[3] = bug.direction.y
        self.information[4] = bug.energy
        self.information[5] = bug.attack
        self.information[6] = bug.amount_near
        self.information[7] = bug.been_attacked
        self.information[8] = bug.speed
        if bug.very_closest_other is not None:
            self.information[9] = True
            self.information[10] = bug.very_closest_other.pos.x
            self.information[11] = bug.very_closest_other.pos.y
            self.information[12] = bug.very_closest_other_distance
        if bug.very_closest_fruit is not None:
            self.information[13] = True
            self.information[14] = bug.very_closest_fruit.pos.x
            self.information[15] = bug.very_closest_fruit.pos.y
            self.information[16] = bug.very_closest_fruit_distance
        self.information[17] = bug.eat_cooldown
        self.information[18] = bug.eat_cooldown_timer
        self.information[19] = bug.distance_to_sides[0]
        self.information[20] = bug.distance_to_sides[1]
        self.information[21] = bug.distance_to_sides[2]
        self.information[22] = bug.distance_to_sides[3]
        if bug.quadrant is not None:
            self.information[23] = bug.quadrant

        self.information[24] = bug.brotein
        self.information[25] = bug.frutein
        self.information[26] = bug.spontanous_death_chance

        amount = Brain.minimum_neuron_input

        for j in range(bg.Bug.amount_detect_max):
            if bug.closest_other[j] != None:
                if amount >= self.neuron_input:
                    break
                self.information[amount] = bug.closest_other[j].pos.x
                amount += 1

                if amount >= self.neuron_input:
                    break
                self.information[amount] = bug.closest_other[j].pos.y
                amount += 1

                if amount >= self.neuron_input:
                    break
                self.information[amount] = bug.closest_other[j].direction.x
                amount += 1

                if amount >= self.neuron_input:
                    break
                self.information[amount] = bug.closest_other[j].direction.y
            if bug.closest_fruit[j] != None:
                if amount >= self.neuron_input:
                    break
                self.information[amount] = bug.closest_fruit[j].pos.x
                amount += 1

                if amount >= self.neuron_input:
                    break
                self.information[amount] = bug.closest_fruit[j].pos.y
                amount += 1

    def brainThink(self):
        h = np.array(self.information, dtype=float)
        energy_consumed = 0

        for i in range(len(self.W)):
            z = np.dot(self.W[i], h) + self.B[i]
            h = Brain.sigmoid(z)

        for layer in self.hidden_size:
            energy_consumed += layer

        energy_consumed /= 5000
        
        return h, energy_consumed

    def brainMutate(self, chance=0.5, super_chance=0.1, strength=0.5, super_strength=0.7, amount = 1):
        for i in range(amount):
            for W in self.W:
                # Normal mutation mask
                mask = np.random.rand(*W.shape) < chance
                
                # Super mutation mask
                super_mask = np.random.rand(*W.shape) < super_chance

                # Normal mutation
                mutation = np.random.uniform(-strength, strength, W.shape)
                W += mask * mutation

                # Super mutation overrides normal one
                mutation_super = np.random.uniform(-super_strength, super_strength, W.shape)
                W += super_mask * mutation_super

    def random_range(a, b):
        return a + (b - a) * (secrets.randbits(52) / (1 << 52))