import numpy as np

keys = np.linspace(0,.99,100)
vals = np.linspace(0.01,0.01,100)

d = {}
for x, y in zip(keys, vals):
    d[x]=y


def likelihood_func(string, value):
    if string=='H':
        return value
    elif string=='T':
        return 1-value
    else:
        return
