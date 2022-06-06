import secrets

Q = 2**512

def encrypt(x, no_shares = 3): 
    """
    Splits the secret up into 'no_shares' shares
    """
    shares = [secrets.randbelow(Q+1) for i in range(no_shares - 1)]
    shares.append((x - sum(shares)) % Q)
    return shares

def decrypt(shares):
    """
    Combine all shares to retrieve the secret
    """
    return sum(shares) % Q