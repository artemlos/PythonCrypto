# -*- coding: utf-8 -*-
"""
Created on Sun May 21 14:31:32 2017

@author: Artem Los
"""

import random

inf = 0

prime = 2**7-1
order = 143

# remember to check isSingular(a,b,p) == False
a = 1
b = 6


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
        return (q[0], q[1])


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


def find_g():
    g = random.randint(0,prime)
    
    if mod(prime,4) != 3:
        print("Cannot use this method to find the root.")
        return
    
    while not(isQuadRes(g, prime)):
        g = random.randint(0,prime)
    
    root = squareAndMultiply(g,3,prime)
    
    return (g,root)

def find_order():
    
    r = order_range()
    
    g = find_g()
    
    for i in range(int(r[0]), int(r[1])+1):
        
        if doubleAndAddOrSubtract(g, i) == inf:
            return i
    
    return -1 #countResidues(a, b, prime)+1


def order_range():
    
    import math
    
    return ( prime +1 -2*math.sqrt(prime), prime +1 +2*math.sqrt(prime) )


def find_public_key(g, secret):
    return doubleAndAddOrSubtract(g, secret)

def sign(g,secret, k_rnd, hash_val):
    m = secret
    k = k_rnd
    q = order
    u, v = doubleAndAddOrSubtract(g, k)
    r = mod(u,q)
    s = mod(modInverse(k, q) * mod(hash_val + m*r, q), q)
    
    # NOTE: if either r==0 or s==0, a new random
    # value k needs to be chosen
    
    return (r,s)

def verify(g, signature, public_key, hash_value):
    
    h = hash_value
    q = order

    r = signature[0]
    s = signature[1]
    
    w = modInverse(s, q)
    i = mod(w * h, q)
    j = mod(w*r, q)
    
    
    t1 = doubleAndAddOrSubtract(g, i)
    t2 = doubleAndAddOrSubtract(public_key, j)
    
    r1, _  = addPoints(t1, t2)
    
    #return addPoints(t1, t2)
    return r1 == r


print(isSingular(a,b,prime) == False)

secret = 111
g = find_g()
pub = find_public_key(g, secret)

res = sign(g, secret, 12, 44444)
print(res)
print(verify(g, res, pub, 44444))



# https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python:_Probably_correct_answers

def is_Prime(n):
    """
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n!=int(n):
        return False
    n=int(n)
    #Miller-Rabin test for prime
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
 
    if n==2 or n==3 or n==5 or n==7:
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
 
    for i in range(8):#number of trials 
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
 
    return True  

