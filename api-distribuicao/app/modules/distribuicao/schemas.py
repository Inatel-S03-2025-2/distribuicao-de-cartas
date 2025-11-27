from enum import Enum

class Status(Enum):
  SUCESSO = "sucesso"
  ERRO = "erro"

class StatusDistribuicao:
  def __init__ (self):
    self.__status: Status | None = None
    self.__mensagem: str | None = None
    self.__codigo: str | None = None
  
  def get_status(self):
    if self.__status is None:
      return None
    return self.__status.value
  
  def set_status(self, novo_status: Status):
    self.__status = novo_status

  def get_mensagem(self):
    return self.__mensagem
  
  def set_mensagem(self, nova_mensagem: str):
    self.__mensagem = nova_mensagem

  def get_codigo(self):
    return self.__codigo
  
  def set_codigo(self, novo_codigo: str):
    self.__codigo = novo_codigo
  
  def get_resumo(self):
    return {
      "status:": self.get_status(),
      "mensagem:": self.get_mensagem(),
      "codigo:": self.get_codigo()
    }
