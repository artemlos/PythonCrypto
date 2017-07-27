# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 22:31:07 2017

@author: Artem Los
"""

# Solves the system of congruent equations.
# m - the list of moduli
# a - the list of coeficients, eg. X mod a_i (X is what we find)
# Based on algorithm on p. 170 in course lit.
def crtSolve(m, a):
    
    M = 1
    
    # Calculate M (by multiplying all modulii)
    for i in range(len(m)):
        M = M * m[i]

    x = 0
    # len(m) is the r
    for i in range(len(m)):
        Mi = M//m[i]
        x = x+ a[i]*Mi*modInverse(Mi, m[i])
    
    return mod(x, M)

# Computes the multiplicative inverse of the 'number' in modulo 'base'.
# If no inverse exists, '-1' will be returned. Inverse otherwise.
# Based on algorithm on p. 168 in course lit.
def modInverse(number, base):
    
    number0 = number
    base0 = base
    t0 = 0
    t = 1
    q = base0 // number0
    r = base0 - q * number0
    
    while r > 0:
        temp = mod(t0 - q*t, base)
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
    
# Computes number mod base
def mod(number, base):
    return number - base * (number//base)


import sys
# The code below is for Kattis only
# From https://open.kattis.com/help/python3
for i in sys.stdin:
    param = i.split()
    k = int(param[0])
    
    M = []
    for i in range(k):
        M.append(int(param[i+1]))
        
    A = []
    
    for i in range(k):
        A.append(int(param[k+i+1]))
    
    print(crtSolve(M,A))
    