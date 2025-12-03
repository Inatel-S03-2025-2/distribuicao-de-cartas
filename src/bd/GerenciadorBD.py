class GerenciadorBD:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init_once(*args, **kwargs)
        return cls._instance

    def __init_once(self):
        # Inicialização da conexão com o banco
        pass

    def conexaoBD(self):
        pass
    def createJogador(self, jogador):
        pass
    def readJogador(self, id):
        pass
    def updateJogador(self, jogador):
        pass
    def deleteJogador(self, jogador):
        pass
