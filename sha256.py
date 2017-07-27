# -*- coding: utf-8 -*-
"""
Created on Wed May 17 21:21:43 2017

@author: Artem Los
"""

# All instances of "Standard" refer to
# http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf


# Compute the SHA-256 hash of the message m.
# Based on #http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf and
# https://en.wikipedia.org/wiki/SHA-2
def SHA256(m):

    #Initialize hash values:
    # (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19):
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19
    
    #Initialize array of round constants:
    # (first 32 bits of the fractional parts of the cube roots of the first 64 primes 2..311):
    k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
    
    modulus = 2**32

    # each chunk is 512 bits (stored as byte arrays). we want to get a multiple
    # of 512.
    chunks = getChunks(m + getAppend(len(m)*8), 64)
    
    for chunk in chunks:
        
        # array of 32-bit words (4 bytes)
        w = [0]*64
        
        for i in range(0,16):
            w[i] = getWord(chunk, i*4)
        
        for i in range(16,64):

            t0 = ROTR(w[i-15],7) ^ ROTR(w[i-15],18) ^ SHR(w[i-15],3)             
            t1 = ROTR(w[i-2],17) ^ ROTR(w[i-2],19) ^ SHR(w[i-2],10) 
            
            w[i] = (t1 + w[i-7] + t0 + w[i-16]) % modulus
    
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        
        for i in range(64):
            S1 = ROTR(e,6) ^ ROTR(e, 11) ^ ROTR(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + k[i] + w[i]) % modulus
            S0 = ROTR(a,2) ^ ROTR(a, 13) ^ ROTR(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            
            temp2 = (S0 + maj) % modulus
            
            h = g
            g = f
            f = e
            e = (d + temp1) % modulus
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % modulus
            
        #Add the compressed chunk to the current hash value:
        h0 = (h0 + a) % modulus
        h1 = (h1 + b) % modulus
        h2 = (h2 + c) % modulus
        h3 = (h3 + d) % modulus
        h4 = (h4 + e) % modulus
        h5 = (h5 + f) % modulus
        h6 = (h6 + g) % modulus
        h7 = (h7 + h) % modulus
            
       
    res = h0
    res <<= 32
    res |= h1
    res <<= 32
    res |= h2
    res <<= 32
    res |= h3
    res <<= 32
    res |= h4
    res <<= 32
    res |= h5
    res <<= 32
    res |= h6
    res <<= 32
    res |= h7
    
    return "{0:#0{1}x}".format(res,66)[2:];



# Returns the number of zero-bits to append to the message.
# length is that of the original string.
def getAppend(length):
    bits = 448-(length+1) % 512
    
    bits = (bits +512) % 512
    size = (bits+1)//8

    #sometimes throws errors
    leftAppend = list((0x1 << bits).to_bytes(size, byteorder='big'))
    
    return leftAppend + list(reversed(list((length >> i) & 0xFF for i in range(0,64,8))))
    #return [1] + [0]*bits + list(reversed(list((length >> i) & 0xFF for i in range(0,64,8))))

# Convert integer to binary representation
def intToBin(number):
    return '{:064b}'.format(number)
    

# Get a word from a 4-byte array.
# The result is a 32-bit integer.
def getWord(a, start):
    r = a[start];
    
    for i in range(1,4):
        r <<= 8
        r |= a[i+start]
        
    return r

# See p. 5 in the standard.
def ROTR(x,n, w=32):
    return (x >> n) | (x << w-n)

# See p. 6 in the standard
def SHR(x,n):
    return x >> n

# http://stackoverflow.com/a/312464/1275924
def getChunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


import sys
for i in sys.stdin:
    i = i.replace("\n","")
    
    sha256 = SHA256(list(bytes.fromhex(i)))
    print(sha256)

    
print("\n")

#print(SHA256(list(bytes.fromhex("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"))))
#print(SHA256(list(bytes.fromhex("e5"))))

