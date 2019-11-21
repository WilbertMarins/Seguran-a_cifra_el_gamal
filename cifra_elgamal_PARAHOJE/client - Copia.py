"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import pickle
marco_zero=[]#vou marcar o cadastro do usuario
chaves_rec=[]
# PICKLES.DUMPS() FUNÇAO PARA ENVIAR MSG
# PICKLES.LOAD() FUNÇAO PARA CARREGAR MSG
#chaves recebidas do servidor  localhost

############    ELGAMAL        ###################
from elgamal import gen_key, encrypt, power, decrypt
from random import randint

p = randint(pow(10, 20), pow(10, 50))  # numero primo
g = randint(2, p)
k = gen_key(p)  # chave privada
r = power(g, k, p)  # calcula a congruencia pra fazer algo
#print("g used : ", g)
#print("g^a used : ", r)
public_key = (p, r, g)



verdade=True
while(verdade==True):
    def receive():
        """Recebimento de mensagens"""
        while True:
            try:
                data = client_socket.recv(BUFSIZ)
                msg = pickle.loads(data)
                print("Essa é a msg recebida cifrada :" ,msg)
                for i in range(len(chaves_rec)):
                    chaves_rec.pop()
                rec=msg[1]#vetor de chaves publicas recebida
                if len(rec)==0:
                    pass
                else:
                    chaves_rec.append(rec)
                print("Chaves publicas recebidas nessa rodada:",chaves_rec)


                if msg[3]=='servidor':
                    msg_list.insert(tkinter.END, msg[0])
                else:
                    private_key=(msg[2],k,p)
                    print("minha chave privada",private_key)
                    dr_msg = decrypt(msg[0], private_key)
                    dmsg = ''.join(dr_msg)
                    print("Mensagem decifrada :", dmsg)
                    nome=msg[3]
                    msg_exibida=str(nome)+str(dmsg)
                    msg_list.insert(tkinter.END, msg_exibida)



                print("nome socket ", client_socket.getsockname())# minha porta

                #print("recebe esse nº %i de chaves", len(chaves_rec))



            except OSError:  # Possibilidade do cliente deixar o chat.
                break

    def send(event=None):  # evento é passado por binders.
        """Envio de mensagens."""

        msg = my_msg.get()
        my_msg.set("")  # Limpa o campo de entrada.


        #CHAVE PUBLICA DO USUÁRIO
        chave_p=(p, r, g)


        print("Chaves q tenho", chaves_rec)
        if(len(marco_zero)==0):
            print("Cadastro")
            msgs=[msg,chave_p,0]
            marco_zero.append(0)

        else:
            if(msg!="{quit}"):

                print("Cifrar")
                msgs_cif=[]#msgs cifradas
                gammas=[] #gamma de cada msg que incorpora a chave privada
                for i in range(len(chaves_rec[0])):
                    en_msg, gamma = encrypt(msg, chaves_rec[0][i])
                    msgs_cif.append(en_msg)
                    gammas.append(gamma)
                print("vetor de msgs cifrada",msgs_cif)
                print(" vetor de gammas",gammas)
                msgs = [msgs_cif, chave_p, gammas]

                #lista_msg=[]
                #for i in range(len(chaves_rec)):
                    #lista_msg.append(i)
                #msgs=[lista_msg,chave_p,0]
            if (msg == "{quit}"):
                msgs = [msg, chave_p, 7]




        msg_tratada=pickle.dumps(msgs)
        client_socket.send(msg_tratada)
        for i in range(len(chaves_rec)):
            chaves_rec.pop()


        if msg == "{quit}":
            client_socket.close()
            top.quit()

    def on_closing(event=None):
        """Esta função deve ser chamada quando a janela é fechada."""
        my_msg.set("{quit}")
        send()

    top = tkinter.Tk()
    top.title("Chat Toppezzera")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # Para que as mensagens sejam enviadas.
    my_msg.set("Escreva seu nome.")
    # Para navegar pelas mensagens anteriores.
    scrollbar = tkinter.Scrollbar(messages_frame)
    # A seguir conterá as mensagens.
    msg_list = tkinter.Listbox(messages_frame, height=15,
                               width=80, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    # ----Agora vem a parte dos sockets----
    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)


    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()  # Starts GUI execution.
