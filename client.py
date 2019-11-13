"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from elgamal import gerar_chaves, encrypt, decrypt
from user import User
import pickle


class User:
    def __init__(self, name, keys=()):  # metodo construtor
        self.name = name
        self.__private_key = keys[1]
        self.my_public_key = keys[0]
        self.public_keys = {}

    def add_public_key(self, name, key):
        self.public_keys[name] = key

    def get_my_public_key(self):
        return self.my_public_key

    def get_private_key(self):
        return self.__private_key

    def get_public_keys(self):
        return self.public_keys

    def mostrar_dados(self):
        print("name: ", self.name)
        print("privado: ", self.get_private_key())
        print("Publica: ", self.get_my_public_key())
        print("Chaves publicas: ", self.get_public_keys())


def receive():
    """Recebimento de mensagens"""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msgg = list(msg)
            # msg = decrypt(msgg, ())
            # nessa parte acredito que pode ocorrer a decifragem
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibilidade do cliente deixar o chat.
            break


def send(event=None):  # evento é passado por binders.
    """Envio de mensagens."""
    msg = my_msg.get()
    my_msg.set("")  # Limpa o campo de entrada.
    pub, priv = gerar_chaves()
    msgc, gamma = encrypt(msg, pub)
    # s = pickle.dumps(msgc)
    client_socket.send(bytes(str(msgc), "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def send_key(event=None):
    public, private = gerar_chaves()
    client_socket.send(str.encode(bytes(public, "utf8")))


def on_closing(event=None):
    """Esta função deve ser chamada quando a janela é fechada."""
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chat Toppezzera")


# gerando chaves do usuario
my_public, private = gerar_chaves()

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
# entry_field.bind("<Return>", send_key)
entry_field.pack()
# a cifragem ocorrerá no evento de click
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
