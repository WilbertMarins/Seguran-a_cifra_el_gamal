from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
#funcoes especiais
# envio
def pre_proc(en_msg1):
    string = []
    for i in range(0, len(en_msg1)):
        string.append(str(en_msg1[i]))
    msg_pro = "-".join(string)  # msg processada para envio
    return msg_pro


# recebe
def pos_pro(msg_ci):
    processo = msg_ci.split("-")
    inteiro = []
    for i in range(0, len(processo)):
        inteiro.append(int(processo[i]))

    return inteiro

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

 k = gen_key(q)  # Public key for sender
 s = power(h, k, q)
 p = power(g, k, q)

 for i in range(0, len(msg)):
  en_msg.append(msg[i])


 for i in range(0, len(en_msg)):
  en_msg[i] = s * ord(en_msg[i])

 return en_msg, p


def decrypt(en_msg, p, key, q):
 dr_msg = []
 h = power(p, key, q)
 for i in range(0, len(en_msg)):
  dr_msg.append(chr(int(en_msg[i] / h)))

 return dr_msg



######MAIN ELGAMAL#######
q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)
k = gen_key(q)  # key public for sender tem q enviar
key = gen_key(q)  # Private key for receiver
h = power(g, key, q)

 ########################



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

        #############recebo 3 partes da chave apos iniciar a conexao ########
        z = tcp.recv(1024) #g
        x = tcp.recv(1024) #q
        l = tcp.recv(1024) #h
        print(str(z, 'utf-8'))
        print(str(x, 'utf-8'))
        print(str(l, 'utf-8'))

        while send.loop():
            # aceita uma mensagem
            msg = tcp.recv(1024)
            if not msg:
                break
            #[en_msg=str(msg)#, 'utf-8')
            #en_msg, p = encrypt(en_msg, q, k, g)

            #dr_msg = decrypt(en_msg, p, key, q)
            #dmsg = ''.join(dr_msg)
            #]print("Decrypted Message full :", dmsg);

            #print(str(dr_msg, 'utf-8'))
            print(str(msg, 'utf-8'))



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

#send.put(k)#envia a chave publica
msg=input()
while True:
 send.put(msg)
 msg=input()

processo.join()
tcp.close()
exit()
