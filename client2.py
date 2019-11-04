from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from elgamal import gen_key, encrypt, power, decrypt
from random import randint


# classe para manipular o socket
class Send:
    def __init__(self):
        self.__msg = ''
        self.new = True
        self.cifra = list
        self.con = None

    def put(self, msg):
        self.__msg = msg
        if self.con != None:
            # envia um mensagem atravez de uma conexão socket
            self.con.send(str.encode(str(self.__msg)))

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
            print("antes if", msg)
            print(str.encode(str(msg, 'utf-8')))
            if not msg:
                break

            decifrada = decrypt(msg, gamma, k, p)
            print("decifrada", type(decifrada))
            str(decifrada)

            print(str(decifrada))


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

    p = randint(pow(10, 20), pow(10, 50))  # numero primo
    g = randint(2, p)
    k = gen_key(p)  # chave privada
    r = power(g, k, p)  # calcula a congruencia pra fazer algo
    chave_publica = (p, r, g)
    send.put(chave_publica)

    msg = input()
    msg_cifrada, gamma = encrypt(msg, p, r, g)

    while True:
        send.put(msg_cifrada)
        msg = input()
        msg_cifrada, gamma = encrypt(msg, p, r, g)

    processo.join()
    tcp.close()
    exit()
