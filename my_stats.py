




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
