# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 15:32:09 2017

@author: Artem Los
"""

nums = {}
# REMOVE LATER
def popWithSquares(a, b, p):
    for x in range(p):
        #y2 =( x*x*x+a*x+b )% p
        
        if x**2%p in nums:
            nums[x**2 % p].append(x)
        else:
            nums[x**2 % p] = [x]
        