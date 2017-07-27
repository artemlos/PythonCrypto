# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:42:17 2017

@author: Artem Los
"""
p = 1907
q = 953 # (p-1)/2

c=[910, 114, 1803]
g= 507

# Finds the secret given the list of correct shares.
# Based on algorithm on p. 482 in the course literature.
def joinShares(shares):
    result = 0
    
    for i in range(len(shares)):
        b = 1
        for j in range(len(shares)):
            if i != j:
                b = b * shares[j][0] * modInverse(shares[j][0]-shares[i][0], q)
                b = b % q
        b = b % q
        
        result = (result + b*shares[i][1]) % q
        
    return result

# Checks if a given share is correct.
# Note, global settings for c, g, p, q are used.
def correctShare(share):
    res=c[0]
    
    for i in range(1,len(c)):
        res = res * squareAndMultiply(c[i], share[0]**i, p) % p

    return res == squareAndMultiply(g,share[1], p)

# Extracts the shares that are correct.
def getCorrectShares(shares):
    
    shares = [x for x in shares if correctShare(x)]

    
# Computes the multiplicative inverse of the 'number' in modulo 'base'.
# If no inverse exists, '-1' will be returned. Inverse otherwise.
# Based on algorithm on p. 168 in course lit.
def modInverse(number, base):
    
    number0 = number % base
    base0 = base
    t0 = 0
    t = 1
    q = base0 // number0
    r = base0 - q * number0
    
    while r > 0:
        temp = (t0 - q*t) % base
        t0 = t
        t = temp
        base0 = number0
        number0 = r
        q = base0 // number0
        r = base0 - q* number0
        
    if number0 != 1:
        return -1
    else:
        return t
    
# Calculate 'x^c mod n' using square-and-multiply algorithm.
def squareAndMultiply(x,c,n):
    
    # get the binary representation of c, the exponent.
    b = intToBin(c) 
    
    z = 1
    
    # the main algorithm, adjusted from p. 177 from course lit.
    for i in range(len(b)):
        z = z*z % n
        
        if b[i] == '1':
            z = z*x % n
    return z

# Return an array that contains the binary representation of the number.
def intToBin(number):
    return '{:b}'.format(number)


# This is for Kattis only.
import sys
for i in sys.stdin:
    param = i.split()
    p = int(param[0])
    q = (p-1)//2
    g = int(param[1])
    d = int(param[2])
    
    c= []
    
    for j in range(3,d+4):
        c.append(int(param[j]))
        
    k = int(param[d+4])
    
    #print(c)

    
    shares = []
    for j in range(d+5, d+k+5):
        # should start with 1.
        share = (j-d-4,int(param[j]))
        if correctShare(share):
            shares.append(share)
            
    print(joinShares(shares))