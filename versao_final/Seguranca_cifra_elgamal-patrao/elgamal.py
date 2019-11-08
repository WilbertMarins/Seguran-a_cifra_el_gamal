from random import randint
from math import pow

a = randint(2, 10)


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# Generating large random numbers
def gen_key(q):

    key = randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = randint(pow(10, 20), q)

    return key


# Modular exponentiation
# parte que calcular o r pra criar a chave publica r = g^k (mod p)
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)

    return x % c


# Asymmetric encryption
def encrypt(msg, p, r, g):

    en_msg = []

    b = gen_key(p)  # Private key for sender
    s = power(r, b, p)  # congruencia pra algo
    gamma = power(g, b, p)

    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    print("g^k used : ", gamma)
    print("g^ak used : ", s)
    for i in range(0, len(en_msg)):
        en_msg[i] = s * ord(en_msg[i])

    return en_msg, gamma


def decrypt(en_msg, p, key, q):

    dr_msg = []
    h = power(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i]/h)))

    return dr_msg


def gerar_chaves():
    p = randint(pow(10, 20), pow(10, 50))  # numero primo
    g = randint(2, p)
    k = gen_key(p)  # chave privada
    r = power(g, k, p)  # calcula a congruencia pra fazer algo
    public_key = (p, r, g)

    return public_key, k
