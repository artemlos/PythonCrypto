# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 22:25:54 2017

@author: Artem Los
"""

import random
import math as m

# Finds the prime numbers p and q given n = p*q and ab=1 (mod phi(n))
# A definite answer is guaranteed if such exists.
def findPrimesRSA(n,a,b):
    while True:
        p =  findPrimesRSALasVegas(n,a,b)
        
        if(p != -1 and p != n):
            return (p, n//p)
        

# Finds the prime number p (q is derived by devision) with a probability 
# of at least 1/2 given n = p*q and ab=1 (mod phi(n)).
# Based on the algorithm on p. 204 in course lit
def findPrimesRSALasVegas(n, a, b):
    w = random.randint(1, n-1)
    
    x = m.gcd(w, n)
    
    if 1 < x and x < n:
        # x is a factor of n
        return x
    
    v = squareAndMultiply(w, getIntPart(a*b-1) , n)
    
    if v % n == 1:
        return -1
    
    v0 = 0
    while v % n != 1:
        v0 = v
        v = squareAndMultiply(v, 2 ,n)
    
    # watch out, how is mod defined
    if v0 % n == -1: 
        return -1
    
    p = m.gcd(v0 + 1, n)
    
    return p

# Finds r such that number = (2^s)*r, i.e. the odd part of the number.
def getIntPart(number):

    # loop while number is even.
    # once it's odd, we've found r.
    while number % 2 == 0:
        # division by two using shifting
        number = number >> 1
        
    return number

# Return an array that contains the binary representation of the number.
def intToBin(number):
    return '{:b}'.format(number)

# Computes number mod base
def mod(number, base):
    return number - base * (number//base)

# Calculate 'x^c mod n' using square-and-multiply algorithm.
def squareAndMultiply(x,c,n):
    
    # get the binary representation of c, the exponent.
    b = intToBin(c) 
    
    z = 1
    
    # the main algorithm, adjusted from p. 177 from course lit.
    for i in range(len(b)):
        z = mod(z*z, n)
        
        if b[i] == '1':
            z = mod(z*x, n)
    return z


import sys

# The code below is for Kattis only
# From https://open.kattis.com/help/python3
for i in sys.stdin:
    param = i.split()
    x = int(param[0])
    a = int(param[1])
    b = int(param[2])
    
    p,q = findPrimesRSA(x,a,b)
    if p < q:
        print(str(p) + " " + str(q))
    else:
        print(str(q) + " " + str(p))
    