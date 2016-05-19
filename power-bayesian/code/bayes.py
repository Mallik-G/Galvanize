import matplotlib.pyplot as plt
import dice
import biased_coin
import seaborn as sns
from coin import Coin
from collections import defaultdict

class Bayes(object):
    '''
    INPUT:
        prior (dict): key is the value (e.g. 4-sided die),
                      value is the probability

        likelihood_func (function): takes a new piece of data and the value and
                                    outputs the likelihood of getting that data
    '''
    def __init__(self, prior, likelihood_func):
        self.prior = prior
        self.likelihood_func = likelihood_func


    def normalize(self):
        '''
        INPUT: None
        OUTPUT: None

        Makes the sum of the probabilities equal 1.
        '''

        denom = float(sum(self.prior.values()))
        for k, v in self.prior.iteritems():
            self.prior[k]=v/denom


        pass




    def update(self, data):
        '''
        INPUT:
            data (int or str): A single observation (data point)

        OUTPUT: None

        Conduct a bayesian update. Multiply the prior by the likelihood and
        make this the new prior.
        '''

        try:
            for item in data:
                for k, v in self.prior.items():
                    self.prior[k] = self.likelihood_func(item, k) * self.prior[k]
                self.normalize()
        except:
            for k, v in self.prior.items():
                self.prior[k] = self.likelihood_func(data, k) * self.prior[k]
            self.normalize()
        pass


    def print_distribution(self):
        '''
        Print the current posterior probability.
        '''
        for k, v in sorted(self.prior.items()):
            print "{}: {}".format(k, v)


    def plot(self, color=None, title=None, label=None):
        '''
        Plot the current prior.
        '''

        keys = []
        vals = []
        for k, v in sorted(self.prior.items()):
            keys.append(k)
            vals.append(v)
        plt.plot(keys, vals, label=label)
        plt.title(title)
        plt.legend()

        pass


    def multi_plot(self, r, c, num_plots, update_list, title):
        b2 = Bayes(biased_coin.d.copy(), biased_coin.likelihood_func)
        for i in xrange(1,num_plots+1):
            plt.subplot(r,c,i)
            b2.update(update_list[i-1])
            b2.plot(title=title, label=update_list[i-1])

        plt.tight_layout()
        plt.show()

    def coin_iterations(self, coin, number_list):
        total = []
        holder = []
        prev_len = 0
        for item in number_list:
            curr_len = item - prev_len
            prev_len = item
            for i in xrange(curr_len):
                holder.append(coin.flip())
                print holder
            total.append(holder[:])
        return total




def main():

    update_list = [['H'],['T'],['H','H'],['T','H'],['H','H','H'],
                   ['T','H','T'],['H','H','H','H'],['H','T','H','T']]

    b2 = Bayes(biased_coin.d.copy(), biased_coin.likelihood_func)
    #b2.multi_plot(4,2,8,update_list,title='Bernoulli')
    mycoin = Coin()

    update_list = [1,2,5,10,50,250]
    total =  b2.coin_iterations(mycoin, update_list)
    for num, lst in zip(update_list, total):
        b2.update(lst)
        b2.plot(label=str(num))
    plt.show()





if __name__ == '__main__':
    main()
