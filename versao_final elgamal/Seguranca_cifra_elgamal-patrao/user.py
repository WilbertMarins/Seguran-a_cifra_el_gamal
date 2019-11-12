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
