# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 15:36:08 2017

@author: Artem Los
"""
# Returns number of affine points on the elliptic curve (wihout point at inf).
def countResidues(a, b, p):
    
    counter  = 0
    for x in range(0,p):
        
        # the curve in 
        y2 = (x**3+a*x+b) % p
        
        # if x^3+ax+b = 0 (mod p), then there exists one point only.
        # i.e. the point is still on the curve even if there is no residue.
        if y2 == 0:
            counter += 1
            continue
        
        # if quadratic residues exists, two points are on the curve
        # i.e. the solutions to y^2 = x^3+ax+b (mod p)
        if isQuadRes(y2, p):
            counter +=2
    
    return counter


# Check if a curve is singular by checking that 4a^3+27b^2 = 0
# See p. 255 in course lit.
def isSingular(a, b, p):
    return ( -(4*a*a*a % p)-(27*b*b % p)) % p == 0


# Determines if there exists an x such that x^2=a (mod p), in other words,
# it will return true if the quadratic residue exists.
# Based on Euler's criterion, see course lit p. 180.
def isQuadRes(a,p):
    return squareAndMultiply(a,((p-1)//2), p) == 1

# Convert integer to binary representation
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
    p = int(param[0])
    a = int(param[1])
    b = int(param[2])
    
    singular = 0
    if(isSingular(a,b,p)):
        singular = 1
    
    
    print(str(singular) + " " + str(countResidues(a,b,p)))
    
