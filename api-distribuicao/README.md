# API de Distribuição de Pokémons

Sistema responsável por escolher 5 pokémons aleatórios da PokéAPI e distribuir para cada jogador cadastrado.

## 📋 Descrição

Esta aplicação faz parte de um sistema distribuído de gerenciamento de cartas Pokémon. Sua responsabilidade é:

1. **Receber requisição** quando um jogador se cadastra
2. **Sortear 5 pokémons aleatórios** da PokéAPI (sem repetições para o mesmo jogador)
3. **Registrar** os pokémons no banco de dados
4. **Fornecer interface de consulta** para outras aplicações verificarem os pokémons de um jogador

> **Nota**: Um mesmo jogador não pode ter pokémons repetidos, mas o mesmo pokémon pode ser distribuído para jogadores diferentes.

## 🚀 Endpoints

### POST `/api/v1/players/{id}/distribution`
Distribui 5 pokémons aleatórios para um jogador (chamado quando o jogador se cadastra).

**Resposta:**
```json
{
  "status": "sucesso",
  "mensagem": "5 pokémons distribuídos com sucesso",
  "codigo": "201",
  "pokemons": [
    {
      "numero_pokedex": 25,
      "nome": "pikachu",
      "is_shiny": false
    }
  ]
}
```

### GET `/api/v1/players/{id}/pokemons`
Consulta os pokémons distribuídos para um jogador (interface para outras aplicações)

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=distribuicao_de_cartas

# API
API_HOST=0.0.0.0
API_PORT=8000

# Game Rules
MAX_POKEMONS_PER_PLAYER=5
SHINY_PROBABILITY=8192
```

### Instalação

1. Criar ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Executar a aplicação:
```bash
cd api-distribuicao
uvicorn app.main:app --reload
```

## 🗄️ Banco de Dados

### Schema

O banco utiliza MySQL com as seguintes tabelas:

- **Pokemon**: Armazena os pokémons únicos
- **Usuario**: Armazena os jogadores
- **UsuarioPokemon**: Tabela de associação (many-to-many)

### Criar o banco

Execute o script SQL disponível em `banco-de-dados.sql`:

```bash
mysql -u root -p < banco-de-dados.sql
```

## 🧪 Testes

Para executar testes:

```bash
pytest api-distribuicao/app/modules/distribuicao/testes.py -v
```

## 📚 Princípios Aplicados

### Clean Architecture
- **Separação de camadas**: Core, Shared, Modules
- **Dependency Injection**: Services recebem dependências via construtor
- **Repository Pattern**: Abstração do acesso a dados

### SOLID
- **Single Responsibility**: Cada classe tem uma única responsabilidade
- **Dependency Inversion**: Dependências apontam para abstrações

### Design Patterns
- **Repository Pattern**: `PokemonRepository`, `UsuarioRepository`
- **Service Layer**: `DistribuicaoService`
- **Dependency Injection**: Via FastAPI `Depends()`

## 📖 Documentação da API

Com a aplicação rodando, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **PyMySQL**: Driver MySQL
- **Pydantic**: Validação de dados
- **Requests**: Cliente HTTP para PokéAPI

## 👥 Autores

Projeto desenvolvido para a disciplina de Sistemas Distribuídos - INATEL
