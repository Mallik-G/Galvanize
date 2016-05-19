
uniform_die = {4: 1/5., 6: 1/5., 8: 1/5., 12: 1/5., 20: 1/5.}
weighted_die = {4: .08, 6: .12, 8: .16, 12: .24, 20: .4}


def likelihood_func(data, key):

    #key will be the die
    #data will be the number rolled

    if data > int(key):
        prob = 0
    else:
        prob = 1./int(key)
    return prob
