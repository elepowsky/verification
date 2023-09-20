import numpy as np

def inverse_gumbel(cdf, a=0, b=1):
	z = a-b*np.log(-np.log(cdf))
	return z


print(inverse_gumbel(0.5))
print(inverse_gumbel(0.99))
