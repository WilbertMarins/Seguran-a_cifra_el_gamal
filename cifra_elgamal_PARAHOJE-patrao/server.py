"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from user import User
from elgamal import gerar_chaves
import pickle

# PICKLES.DUMPS() FUNÇAO PARA ENVIAR MSG
# PICKLES.LOAD() FUNÇAO PARA CARREGAR MSG

def accept_incoming_connections():
    """Configura o manuseio para clientes recebidos"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s ihhhh tem gente." % client_address)
        msg="Qual teu nome ?"
        msg_tratada = pickle.dumps(msg)
        client.send(msg_tratada)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Toma o sockt do cliente como argumento.
    """Lida com uma única conexão de cliente."""

    nome = client.recv(BUFSIZ) #nome recebido
    name=pickle.loads(nome)
    #user = User(name, gerar_chaves())
    #user.add_public_key(user.name, user.get_my_public_key())
    #user.mostrar_dados()
    welcome = 'Bem vindo %s! Agora é so escrever, se quiser sair digita {quit}.' % name
    msg_tratad=pickle.dumps(welcome)
    client.send(msg_tratad)

    msg = "%s entrou no chat!" % name
    broadcast(msg)
    clients[client] = name # o erro esta aqui guardando o usuario onde o endereço é a chave( a={sokt:nome}  ) o end ganha um usuario
    #name1="%s" %name
    #nomes[name] = client #darei um endereço para o usuário
    #nome.append(name1) #listagem de nomes para ser usado nos parametros
    endereco.append(client) #listagem de nomes para ser usado nos parametros  #NOVO

    #DESCONSIDERA OS PRINTS ABAIXO
    print("esse é o",name)
    print("clientes",clients)
    print(len(clients))
    print("end do cliente",client)
    print("nomes",nomes)
    print(len(nomes))
    print("nome",name)
    print(len(name))


    while True:
        data = client.recv(BUFSIZ)
        msg = pickle.loads(data)
        if msg != "{quit}":
            broadcast(msg, name+": ")
        else:
            client.send("{quit}")
            client.close()
            del clients[client]
            broadcast("%s saiu fora." % name)
            break

def broadcast(msg, prefix=""):  # prefix é para identificação do nome.
    """Transmite uma mensagem para todos os clientes."""

    for i in range(len(endereco)):  # end:nome #NOVO
        msg_tratada=pickle.dumps(prefix+msg)
        endereco[i].send(msg_tratada)  #NOVO prefix,



clients = {}  #dicio
addresses = {}  #dicio
nomes={} #dicio
nome=[] #lista NO MOMENTO N FUNCIONA
endereco=[]#enderecos socket dos usuario

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Esperando alguem chegar...")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
