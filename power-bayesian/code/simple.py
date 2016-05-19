import pymc
import numpy

numpy.random.seed(15)

#Let's generate some data, and try to recover the parameters
true_mu = 1.5 
true_scale = 5
N_samples = 500
#data = pymc.rnormal( true_mu, true_tau, size=(N_samples,) )
data = numpy.random.normal(true_mu,true_scale,size=N_samples)



#Assuming we don't know much about the data, we have a two priors-
mu = pymc.Uniform('mu', lower=-100.0, upper=100.0)
tau = pymc.Gamma('tau', alpha=0.1, beta=0.001)


y = pymc.Normal('y',mu,tau,value=data,observed=True)
