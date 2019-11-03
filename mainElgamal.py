from elgamal import gen_key, encrypt, power, decrypt
from random import randint


def main():

    msg = 'encryption'
    print("Original Message :", msg)

    q = randint(pow(10, 20), pow(10, 50))
    g = randint(2, q)

    key = gen_key(q)  # Private key for receiver
    h = power(g, key, q)
    print("g used : ", g)
    print("g^a used : ", h)

    en_msg, p = encrypt(msg, q, h, g)
    dr_msg = decrypt(en_msg, p, key, q)
    dmsg = ''.join(dr_msg)
    print("Decrypted Message :", dmsg)


if __name__ == '__main__':
    main()
