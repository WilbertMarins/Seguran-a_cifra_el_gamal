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
print("g used : ", g)
print("g^a used : ", r)
public_key = (p, r, g)

#en_msg, gamma = encrypt(msg, public_key)
#private_key = (gamma, k, p)
#dr_msg = decrypt(en_msg, private_key)
#dmsg = ''.join(dr_msg)
#print("Decrypted Message :", dmsg)

verdade=True
while(verdade==True):
    def receive():
        """Recebimento de mensagens"""
        while True:
            try:
                data = client_socket.recv(BUFSIZ)
                msg = pickle.loads(data)
                print("Essa é a msg recebida :" ,msg)
                for i in range(len(chaves_rec)):
                    chaves_rec.pop()
                rec=msg[1]#vetor de chaves publicas recebida
                if len(rec)==0:
                    pass
                else:
                    chaves_rec.append(rec)
                print("Chaves recebidas nessa rodada:",chaves_rec)

                # decifra
                print("mgs possui : ",len(msg))
                print("mgs q chegou :" ,msg)
                if msg[3]=='servidor':
                    msg_list.insert(tkinter.END, msg[0])
                else:
                    private_key=(msg[2],k,p)
                    dr_msg = decrypt(msg[0], private_key)
                    dmsg = ''.join(dr_msg)
                    print("Decrypted Message :", dmsg)
                    nome=msg[3]
                    msg_exibida=str(nome)+str(dmsg)
                    msg_list.insert(tkinter.END, msg_exibida)

                #print(msg[0])
                # a msg é um vetor de 2 posições [ msg , lista de chaves]
                #chaves_rec.append(msg)
                #print(chaves_rec)
                ######## DECIFRA A MSG RECEBIDA ###############
                #original msg = client_socket.recv(BUFSIZ)

                print("nome socket ", client_socket.getsockname())
                # nessa parte acredito que pode ocorrer a decifragem
                ######## DECIFRA A MSG RECEBIDA ###############
                print("recebe esse nº %i de chaves", len(chaves_rec))

                #msg_list.insert(tkinter.END, msg[0])

            except OSError:  # Possibilidade do cliente deixar o chat.
                break

    def send(event=None):  # evento é passado por binders.
        """Envio de mensagens."""

        #MANDA
        #[ [vetor_msg] , chave_p , [vetor_P(gamma)] , nome]  cliente-> servidor

        #[ msg , [chaves_p ], p(nulo) , servidor] servidor-> cliente (msg privadas)

        #[ [vetor_msg][i] , [VETOR_CHAVES]  , [vetor_P(gamma)][i] , NOME]  servidor

        msg = my_msg.get()
        my_msg.set("")  # Limpa o campo de entrada.
    ########## VETOR  DE MSG CIFFRADA N VEZES ###############
        # a msg é um vetor de 2 posições [ vetor de msg , chave_p]

        #CHAVE PUBLICA DO USUÁRIO
        chave_p=(p, r, g)
        print("olha mantem chaves", len(chaves_rec))

        print("chaves q tenho total", chaves_rec)
        if(len(marco_zero)==0):
            print("Cadastro")
            msgs=[msg,chave_p,0]
            marco_zero.append(0)
            print("ZIIIIIIIIIIICaAAAA")
        else:
            print("entrou 1")
            msgs_cif=[]#msgs cifradas
            gammas=[] #gamma de cada msg que incorpora a chave privada
            for i in range(len(chaves_rec[0])):
                en_msg, gamma = encrypt(msg, chaves_rec[0][i])
                msgs_cif.append(en_msg)
                gammas.append(gamma)
            print("msg cifrada",msgs_cif)
            print("gammas",gammas)
            msgs = [msgs_cif, chave_p, gammas]
            #decifra

            # private_key=(gammas[0],k,p)
            #dr_msg = decrypt(msgs_cif[0], private_key)
            #dmsg = ''.join(dr_msg)
            #print("Decrypted Message :", dmsg)


            print("olha mantem chaves", len(chaves_rec[0]))
            print("chaves q tenho", chaves_rec[0])
            lista_msg=[]
            for i in range(len(chaves_rec)):
                lista_msg.append(i)
            #msgs=[lista_msg,chave_p,0]




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
