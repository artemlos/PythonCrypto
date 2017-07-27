# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 22:12:34 2017

@author: Artem Los
"""

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
    c = int(param[1])
    n = int(param[2])
    
    print(squareAndMultiply(x,c,n))
    
