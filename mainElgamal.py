from elgamal import gen_key, encrypt, power, decrypt
from random import randint


def gamaltop(msg):

    print("Original Message :", msg)

    p = randint(pow(10, 20), pow(10, 50))  # numero primo
    g = randint(2, p)
    k = gen_key(p)  # chave privada
    r = power(g, k, p)  # calcula a congruencia pra fazer algo
    print("g used : ", g)
    print("g^a used : ", r)
    chave1 = (p, r, g)

    en_msg, gamma = encrypt(msg, chave1)
    chave2 = (gamma, k, p)
    dr_msg = decrypt(en_msg, chave2)
    dmsg = ''.join(dr_msg)
    print("Decrypted Message :", dmsg)


if __name__ == '__main__':
    gamaltop("Tudo bom fofo")
