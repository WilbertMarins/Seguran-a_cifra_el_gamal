from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# classe para manipular o socket

class Send:
    def __init__(self):
        self.__msg = ''
        self.new = True
        self.con = None

    def put(self, msg):
        self.__msg = msg
        if self.con != None:
            # envia um mensagem atraves de uma conexão socket
            self.con.send(str.encode(self.__msg))

    def get(self):
        return self.__msg

    def loop(self):
        return self.new

# função esperar - Thread


def esperar(tcp, send, host='localhost', port=5000):
    destino = (host, port)
    # conecta a um servidor
    tcp.connect(destino)

    while send.loop():
        print('Conectado a ', host, '.')
        # atribui a conexão ao manipulador
        send.con = tcp
        while send.loop():
            # aceita uma mensagem
            msg = tcp.recv(1024)
            if not msg:
                break
            print(str(msg, 'utf-8'))

################ Algoritmo #####################

import random
from math import pow

a = random.randint(2, 10)


def gcd(a, b):
 if a < b:
  return gcd(b, a)
 elif a % b == 0:
  return b;
 else:
  return gcd(b, a % b)

 # Generating large random numbers


def gen_key(q):
 key = random.randint(pow(10, 20), q)
 while gcd(q, key) != 1:
  key = random.randint(pow(10, 20), q)

 return key


# Modular exponentiation
def power(a, b, c):
 x = 1
 y = a

 while b > 0:
  if b % 2 == 0:
   x = (x * y) % c;
  y = (y * y) % c
  b = int(b / 2)

 return x % c


# Asymmetric encryption
def encrypt(msg, q, h, g):
 en_msg = []

 k = gen_key(q)  # Private key for sender
 s = power(h, k, q)
 p = power(g, k, q)

 for i in range(0, len(msg)):
  en_msg.append(msg[i])

 print("g^k used : ", p)
 print("g^ak used : ", s)
 for i in range(0, len(en_msg)):
  en_msg[i] = s * ord(en_msg[i])

 return en_msg, p


def decrypt(en_msg, p, key, q):
 dr_msg = []
 h = power(p, key, q)
 for i in range(0, len(en_msg)):
  dr_msg.append(chr(int(en_msg[i] / h)))

 return dr_msg


# Driver code
#def main():
# print('Escreva sua menssagem')
# msg = 'encryption'
#msg = input()

# print("Original Message :", msg)
q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)
k = gen_key(q)  # Private key for sender
key = gen_key(q)  # Private key for receiver
h = power(g, key, q)
print("g used : ", g)
print("g^a used : ", h)
 ########################

if __name__ == '__main__':
    
    print('Digite o nome ou IP do servidor(localhost): ')
    host = input()

    if host == '':
        host = '127.0.0.1'

    # cria um socket
    tcp = socket(AF_INET, SOCK_STREAM)
    send = Send()
    # cria um Thread e usa a função esperar com dois argumentos
    processo = Thread(target=esperar, args=(tcp, send, host))
    processo.start()
    print('')

msg=input()
while True:
 en_msg, p = encrypt(msg, q, h, g)

 dr_msg = decrypt(en_msg, p, key, q)
 c = 0
 crip = []
 while (c < len(en_msg)):
  crip.append(str(en_msg[c]))
  c += 1
 crip_c = ''.join(dr_msg)

 send.put(crip_c)
 msg=input()

processo.join()
tcp.close()
exit()
