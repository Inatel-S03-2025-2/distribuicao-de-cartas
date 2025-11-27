from ...shared.database import Base
from ...core.pokemon import Pokemon
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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

    idUsuario = Column(Integer, primary_key=True, index=True)
    nomeUsuario = Column(String(50), nullable=False)

    # Relação com UsuarioPokemon
    pokemons_colecao = relationship("UsuarioPokemonORM", back_populates="usuario")

# Classe table usuario has pokemon do bd
class UsuarioPokemonORM(Base):
    __tablename__ = 'UsuarioPokemon'

    # As chaves primárias
    idUsuario = Column(Integer, ForeignKey('Usuario.idUsuario', ondelete='CASCADE'), primary_key=True)
    idPokemon = Column(Integer, ForeignKey('Pokemon.idPokemon', ondelete='CASCADE'), primary_key=True)

    # Definição dos relacionamentos
    usuario = relationship("UsuarioORM", back_populates="pokemons_colecao")
    pokemon_carta = relationship("PokemonORM", back_populates="usuarios_cartas")