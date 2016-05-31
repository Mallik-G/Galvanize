import numpy as np
import math

class Prob_flip(object):
    def __init__(self, prob, iters):
        self.iters = iters
        self.prob = prob

    def play(self):
        win_list = []
        for i in range(self.iters):
            heads = 0
            count = 0
            while heads == 0:
                count += 1
                if np.random.random() < (1-self.prob):
                    pass
                else:
                    heads = 1
                    win_list.append(2*count-1)
        return win_list


    def confidence(self):
        win_list = self.play()
        mean_wl = np.mean(win_list)
        stderr = np.std(win_list) / math.sqrt(self.iters)
        return mean_wl-(1.96*stderr), mean_wl+(1.96*stderr)



#Expected value of n: 2
#2*(2)-1 = 3
