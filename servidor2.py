from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread


#funcoes especiais:

# envio
def pre_proc(en_msg1):
 string = []
 for i in range(0, len(en_msg1)):
  string.append(str(en_msg1[i]))
 msg_pro = "-".join(string)  # msg processada para envio
 return msg_pro


#recebe
def pos_pro(msg_ci):
 processo = msg_ci.split("-")
 inteiro = []
 for i in range(0, len(processo)):
  inteiro.append(int(processo[i]))

 return inteiro


######  algoritmo  ######

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

 k = h  # Public key for sender
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
key = gen_key(q)  # key for receiver
h = power(g, key, q)

##########################





#classe para manipular o socket
class Send:
 def __init__(self):
  self.__msg=''
  self.new=True
  self.con=None
 def put(self,msg):
  self.__msg=msg
  if self.con != None:
   #envia um mensagem atraves de uma conexão socket
   self.con.send(str.encode(self.__msg))
   self.co.send(str.encode(self.__msg))

#funçao onde o invasor recebe a msg q chega ao servidor

 def put_interceptar(self,msg):
  self.__msg=msg
  if self.con != None:
   #envia um mensagem atraves de uma conexão socket

   self.co.send(str.encode(self.__msg))

 def get(self):
  return self.__msg
 def loop(self):
  return self.new
 
#função esperar - Thread
def esperar(tcp,send,host='',port=5000):
 origem=(host,port)
 #cria um vinculo
 tcp.bind(origem)
 #deixa em espera
 tcp.listen(2) # nº de usuários suportados na conexao no servidor

 while True:
  #aceita um conexão
  con,cliente=tcp.accept()
  co,wil=tcp.accept()


  print('Cliente ',cliente,' conectado!')
  print('Cliente ',wil,' conectado!')
  #atribui a conexão ao servidor
  send.con=con
  send.co=co



  while True:

   #aceita uma mensagem
   msg1=con.recv(1024)
   #msg2=co.recv(1024)
   if not msg: break
   print(str(msg1,'utf-8'))
   #print(str(msg2,'utf-8'))
   send.put_interceptar(str(msg1,'utf-8'))




#cria um socket
tcp=socket(AF_INET,SOCK_STREAM)
send=Send()
#cria um Thread e usa a função esperar com dois argumentos
processo=Thread(target=esperar,args=(tcp,send))
processo.start()

print('Iniciando o servidor de chat!')
print('Aguarde alguém conectar!')


msg=input()

#####alumas partes da chave sao enviadas no inicio da conexao#######
send.put(str(g))
send.put(str(q))
send.put(str(h))

while True:
 en_msg, p = encrypt(msg, q, k, g)
 manda=pre_proc(en_msg)
 a=manda
 send.put(a)
 msg=input()
  
processo.join()
tcp.close()
exit()
