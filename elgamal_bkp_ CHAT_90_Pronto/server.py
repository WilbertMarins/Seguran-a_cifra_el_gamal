"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from user import User
from elgamal import gerar_chaves
import pickle

# PICKLES.DUMPS() FUNÇAO PARA ENVIAR MSG
# PICKLES.LOAD() FUNÇAO PARA CARREGAR MSG localhost
P=0#gamma da msg do servidor para compor a msg
nome_serv="servidor"
def accept_incoming_connections():
    """Configura o manuseio para clientes recebidos"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s ihhhh tem gente." % client_address)
        msg="Qual teu nome ?"
        ############## ENVIA O BEM VINDO E VETOR DE CHAVES ##############
        # a msg é um vetor de 2 posições [ vetor de msg , chave_p]
        conectado=[msg,chaves,P,nome_serv]
        msg_tratada = pickle.dumps(conectado)

        client.send(msg_tratada)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Toma o sockt do cliente como argumento.
    """Lida com uma única conexão de cliente."""

    nome = client.recv(BUFSIZ) #nome recebido
    dados=pickle.loads(nome)
    name= dados[0]
    chaves.append(dados[1])
    print("chaves",chaves)

    welcome = 'Bem vindo %s! Agora é so escrever, se quiser sair digita {quit}.' % name
    boas_vindas=[welcome,chaves,P,nome_serv]
    msg_tratad=pickle.dumps(boas_vindas)
    client.send(msg_tratad)

    novo_usu = "%s entrou no chat!" % name # novo usuário
    broadcast2(novo_usu)

    clients[client] = name # o erro esta aqui guardando o usuario onde o endereço é a chave( a={sokt:nome}  ) o end ganha um usuario
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
        if msg[0] != "{quit}":
            # a msg é um vetor de 2 posições [ vetor de msg , chave_p]
            broadcast(msg, name+": ")
        else:  ############# HORA DA SAIDA DE UM USUARIO ############
            client.send("{quit}")
            client.close()
            del clients[client]
            #saida=str(name)+"saiu"
            desconectado = ("%s saiu fora." % name)
            msg_tratada = pickle.dumps(desconectado)
            broadcast(desconectado)
            break

def broadcast(msg, prefix=""):  # prefix é para identificação do nome.
    """Transmite uma mensagem para todos os clientes."""
    #a msg é um vetor de 2 posições [ vetor de msg , chave_p]
    for i in range(len(endereco)):  # end:nome #NOVO

        print("msg normal",msg)
        remetente=(str(prefix))
        print("msg remetente",msg)
        print("Nome remetente",str(prefix))

        msgs = [msg[0][i],chaves,msg[2][i],remetente]

        #msg_tratada=pickle.dumps(prefix+msg)  ########SEPARAR MSG DA CHAVE PUBLICA Q A ACOMPANHA #########
        #msg_tratada=pickle.dumps(prefix+msg)  ########SEPARAR MSG DA CHAVE PUBLICA Q A ACOMPANHA #########
        msg_tratada=pickle.dumps(msgs)  ########SEPARAR MSG DA CHAVE PUBLICA Q A ACOMPANHA #########
        endereco[i].send(msg_tratada)  #NOVO prefix,

def broadcast2(msg):  # FUNÇÃO PARA MSG BÁSICAS Q NÃO ESTÁ CIFRADA
    """Transmite uma mensagem para todos os clientes."""
    #a msg é um vetor de 2 posições [ vetor de msg , chave_p]
    for i in range(len(endereco)):  # end:nome #NOVO
        msgs = [msg, chaves, P, nome_serv]
        msg_tratada=pickle.dumps(msgs)
        endereco[i].send(msg_tratada)



clients = {}  #dicio
addresses = {}  #dicio
nomes={} #dicio
nome=[] #lista NO MOMENTO N FUNCIONA
endereco=[]#enderecos socket dos usuario
chaves=[]

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
