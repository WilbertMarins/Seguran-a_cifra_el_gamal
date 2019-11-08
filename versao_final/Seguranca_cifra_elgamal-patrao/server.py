"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from user import User
from elgamal import gerar_chaves


def accept_incoming_connections():
    """Configura o manuseio para clientes recebidos"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s ihhhh tem gente." % client_address)
        client.send(
            bytes("Qual teu nome ?", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Toma o sockt do cliente como argumento.
    """Lida com uma única conexão de cliente."""

    name = client.recv(BUFSIZ).decode("utf8")
    user = User(name, gerar_chaves())
    user.add_public_key(user.name, user.get_my_public_key())
    user.mostrar_dados()
    welcome = 'Bem vindo %s! Agora é so escrever, se quiser sair digita {quit}.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s o cara entrou!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name # o erro esta aqui guardando o usuario onde o endereço é a chave( a={sokt:nome}  ) o end ganha um usuario
    nomes[name] = client #darei um endereço para o usuário
    nome.append(name) #listagem de nomes para ser usado nos parametros
    teste.append(client) #listagem de nomes para ser usado nos parametros  #NOVO
    print("esse é o",name)
    print("clientes",clients)
    print(len(clients))
    print("end do cliente",client)
    print("nomes",nomes)
    print(len(nomes))
    print("nome",nome)
    print(len(nome))


    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s saiu fora." % name, "utf8"))
            break

def broadcast(msg, prefix=""):  # prefix é para identificação do nome.
    """Transmite uma mensagem para todos os clientes."""
    #for sock in clients:#end:nome
     #   sock.send(bytes(prefix, "utf8")+msg)
    for i in range(len(teste)):  # end:nome #NOVO
        teste[i].send(bytes(str(i), "utf8") + msg)  #NOVO



clients = {}  #dicio
addresses = {}  #dicio
nomes={} #dicio
nome=[] #lista
teste=[]#NOVO

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
