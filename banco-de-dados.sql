DROP DATABASE IF EXISTS distribuicao_de_cartas;
CREATE DATABASE IF NOT EXISTS distribuicao_de_cartas;
USE distribuicao_de_cartas;

-- Tabela de Pokémons
CREATE TABLE IF NOT EXISTS Pokemon (
    idPokemon INT AUTO_INCREMENT PRIMARY KEY,
    nomePokemon VARCHAR(25) NOT NULL,
    isShiny BOOLEAN DEFAULT FALSE
);

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS Usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY
);

-- Relação entre Usuario e Pokemon
CREATE TABLE IF NOT EXISTS UsuarioPokemon (
    idUsuario INT NOT NULL,
    idPokemon INT NOT NULL,

    PRIMARY KEY (idUsuario, idPokemon),
    FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (idPokemon) REFERENCES Pokemon(idPokemon)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Teste
SELECT * FROM Pokemon;
SELECT * FROM Usuario;
SELECT * FROM UsuarioPokemon;