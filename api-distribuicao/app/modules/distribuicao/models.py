from shared.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Jogador:
    def __init__(self, id: str, pokemons: list = None, log: str = ""):
        self.__id = id
        self.__pokemons = pokemons if pokemons is not None else []
        self.__log = log

    def get_id(self):
        return self.__id
    
    def get_pokemons(self):
        return self.__pokemons
    
    def get_log(self):
        return self.__log

class Pokemon:
    def __init__(self, numero_pokedex: int = 0, nome: str = 'missingno', shiny: bool = False):
        self.__numero_pokedex = numero_pokedex
        self.__nome = nome
        self.__shiny = shiny

    def get_numero_pokedex(self):
        return self.__numero_pokedex

    def get_nome(self):
        return self.__nome

    def is_shiny(self):
        return self.__shiny

# classe table pokemon bd
class PokemonORM(Base):
    __tablename__ = 'Pokemon'

    idPokemon = Column(Integer, primary_key=True, index=True)
    nomePokemon = Column(String(25), nullable=False)
    isShiny = Column(Boolean, default=False)

    # Relação com UsuarioPokemon
    usuarios_cartas = relationship("UsuarioPokemonORM", back_populates="pokemon_carta")

# Classe table usuario bd
class UsuarioORM(Base):
    __tablename__ = 'Usuario'

    idUsuario = Column(String(20), primary_key=True, index=True)
    nomeUsuario = Column(String(50), nullable=False)

    # Relação com UsuarioPokemon
    pokemons_colecao = relationship("UsuarioPokemonORM", back_populates="usuario")

# Classe table usuario has pokemon do bd
class UsuarioPokemonORM(Base):
    __tablename__ = 'UsuarioPokemon'

    # As chaves primárias
    idUsuario = Column(String(20), ForeignKey('Usuario.idUsuario', ondelete='CASCADE'), primary_key=True)
    idPokemon = Column(Integer, ForeignKey('Pokemon.idPokemon', ondelete='CASCADE'), primary_key=True)

    # Definição dos relacionamentos
    usuario = relationship("UsuarioORM", back_populates="pokemons_colecao")
    pokemon_carta = relationship("PokemonORM", back_populates="usuarios_cartas")