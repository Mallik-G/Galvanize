
from random import random
from collections import defaultdict
from operator import itemgetter


class PMF(object):
    def __init__(self, keys, vals):
        self.keys = keys
        self.vals = vals
        d = {}
        for i, k in enumerate(keys):
            d[k] = vals[i]
        self.d = d


    def prob(self, key):
        if key in self.d:
            return self.d[key]
        print "Out of discrete distribution"
        return

    def set(self, k, v):
        self.d[k] = v
        for key, val in self.d.iteritems():
            if key == k:
                pass
            else:
                self.d[key] = (1-v) / (len(self.d)-1)

    def print_pmf(self):
        print self.d




class RV(object):
    def __init__(self, pmf_obj):
        self.pmf_obj = pmf_obj


    def sample(self):
        proportions = defaultdict(float)
        old_v = 0.
        r = random()
        keys = []
        vals = []

        for k, v in self.pmf_obj.d.iteritems():
            old_v += v
            vals.append(old_v)
            keys.append(k)

        big_list = [list(x) for x in zip(*sorted(zip(keys, vals), key=itemgetter(0)))]
        new_keys = big_list[0]
        new_vals = big_list[1]

        for k, v in zip(new_keys, new_vals):
            if r >= v:
                pass
            else:
                return k


    def all_outcomes(self):
        return self.pmf_obj.d.keys()


    def pmf(self):
        return self.pmf















        #
