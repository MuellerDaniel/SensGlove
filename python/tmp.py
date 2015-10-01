import numpy as np
import time

def primesPy(kmax):    
    start = time.time()
    result = []
    p = np.zeros((1000,))
    if kmax > 1000:
        kmax = 1000
    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] != 0:
            i = i + 1
        if i == k:
              p[k] = n
              k = k + 1
              result.append(n)
        n = n + 1
    print "time needed: ", time.time()-start
    return result
    
print "with kmax = 4"
#start = time.time()
primesPy(500)
#print primesPy(500)
#print "time spent: ", time.time()-start