class StatusDistribuicao:
  def __init__ (self):
    self.__mensagem = None

  def sucesso(self, nova_mensagem: str):
    self.__mensagem = nova_mensagem
    print(f"✅ {self.__mensagem}")

  def erro(self, nova_mensagem: str):
    self.__mensagem = nova_mensagem
    print(f"❌ {self.__mensagem}")

  def get_mensagem(self):
    return self.__mensagem
