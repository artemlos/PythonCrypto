# -*- coding: utf-8 -*-
"""
Created on Sun May 21 14:31:32 2017

@author: Artem Los
"""

prime = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
b =0x22123dc2395a05caa7423daeccc94760a7d462256bd56916

g =  (0x7d29778100c65a1da1783716588dce2b8b4aee8e228f1896, 0x38a90f22637337334b49dcb66a6dc8f9978aca7648a943b0)

inf = 0


# Uses the idea of squareAndMultiply to compute c*p quickly in E. 
# Based on algorithm on p. 266 in course literature.
# Using NAF representation (and adding subtract step) makes our implementation
# a bit faster.
def doubleAndAddOrSubtract(p, c):
    
    q = inf
    
    b = intToNAF(c)

    for i in range(len(b)-1,-1, -1):
        
        q = addPoints(q,q)
        if b[i] == 1:
            q = addPoints(p,q)
        elif b[i] == -1:
            q = addPoints(negPoint(p),q)

    if q == inf:
        return inf
    else:
        return ((q[0]), (q[1]))


# Adds two points P and Q in E.
# P and Q should be tuples of the form (x,y)
# This method returns a tuple representing the new coordinates.
# See p. 258 in course lit.
def addPoints(p,q):
    
    if q == inf:
        return p
    
    if p == inf:
        return q
    
    if q[0] == p[0] and q[1] == -p[1] % prime:
        return inf

    l = 0
    
    if p != q:
        #maybe need add prime to q1-p1
        l = ((q[1] - p[1] ) * modInverse(q[0]-p[0], prime)) % prime
    else:
        l = ((3 *p[0]**2 + a) * modInverse(2*p[1], prime)) % prime
    
    x3 = (l**2 - p[0]-q[0]) % prime

    return (x3, (l*(p[0] - x3) - p[1]) % prime);


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

# Convert a number to Non-adjacent form
# Based on pseudo-code at https://en.wikipedia.org/wiki/Non-adjacent_form
def intToNAF(number):
    i = 0
    z = []
    #z = [0]*(math.floor(math.log2(number) +1) +10)
    while number > 0:
        if number % 2 == 1:
          z.append(2 - (number % 4))
          number = number - z[i]
        else:
            z.append(0)
          
        number = number // 2
        i = i +1
      
    return z

# Get the negative point, eg. -p, given p.
def negPoint(point):
    return (point[0], (-point[1]) % prime)

# Return an array that contains the binary representation of the number.
def intToBin(number):
    return '{:b}'.format(number)


import sys

# The code below is for Kattis only
# From https://open.kattis.com/help/python3
for i in sys.stdin:  
    res = doubleAndAddOrSubtract(g,int(i,0))
    
    print(res[0] + " " +res[1])
    