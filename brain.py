import numpy as np
import bug as bg
import secrets

class Brain():    
    minimum_neuron_input = 15
    def __init__(self, neuron_min_limit = 0):
        self.neuron_input = neuron_min_limit + Brain.minimum_neuron_input

        self.hidden_size = [
            self.neuron_input,
            100,
            100,
            500,
            100,
            100,
            5
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
        self.information[0] = bug.pos.x
        self.information[1] = bug.pos.y
        self.information[2] = bug.vel.x
        self.information[3] = bug.vel.y

        amount = self.neuron_input

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

    def brainThink(self):
        h = np.array(self.information, dtype=float)

        for i in range(len(self.W)):
            z = np.dot(self.W[i], h) + self.B[i]
            h = Brain.sigmoid(z)

        return h

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