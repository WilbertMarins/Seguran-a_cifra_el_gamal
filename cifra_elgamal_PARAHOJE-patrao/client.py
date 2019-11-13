"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from elgamal import encrypt
import pickle

# PICKLES.DUMPS() FUNÇAO PARA ENVIAR MSG
# PICKLES.LOAD() FUNÇAO PARA CARREGAR MSG

def receive():
    """Recebimento de mensagens"""
    while True:
        try:
            #msg = tcp.recv(1024)
            #data = pickle.loads(msg)
            data = client_socket.recv(BUFSIZ)
            msg = pickle.loads(data)

            #original msg = client_socket.recv(BUFSIZ)
            print("nome socket ", client_socket.getsockname())
            # nessa parte acredito que pode ocorrer a decifragem
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibilidade do cliente deixar o chat.
            break
#localhost

def send(event=None):  # evento é passado por binders.
    """Envio de mensagens."""
    msg = my_msg.get()
    my_msg.set("")  # Limpa o campo de entrada.

    msg_tratada=pickle.dumps(msg)
    client_socket.send(msg_tratada)

    if msg_tratada == "{quit}":
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
my_msg.set("Escreve pô.")
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
