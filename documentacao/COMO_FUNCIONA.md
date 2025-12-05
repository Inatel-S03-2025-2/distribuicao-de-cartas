# 📚 Como o Código Funciona

## 🎯 Visão Geral

Este projeto implementa uma API REST em **FastAPI** para distribuição e gerenciamento de cartas Pokémon entre jogadores. A arquitetura segue princípios de **Clean Architecture** com separação clara de responsabilidades.

---

## 🏗️ Arquitetura do Projeto

```
api-distribuicao/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── shared/                 # Infraestrutura compartilhada
│   │   └── database.py         # Configuração do banco de dados
│   └── modules/                # Módulos da aplicação
│       └── distribuicao/       # Módulo de distribuição de cartas
│           ├── router.py       # Endpoints HTTP (Controllers)
│           ├── service.py      # Lógica de negócio (Use Cases)
│           ├── repository.py   # Acesso a dados (Data Access)
│           ├── models.py       # Entidades de domínio e ORM
│           ├── adapters.py     # Conversores Domain ↔ ORM
│           ├── external.py     # Integração com PokéAPI
│           └── schemas.py      # DTOs e validações
```

---

## 🔄 Fluxo de Execução

### **1. Inicialização da Aplicação**

```python
# main.py
app = FastAPI()
app.include_router(distribuicao_router, prefix="/api")
```

- Cria instância do FastAPI
- Registra rotas do módulo de distribuição
- Disponibiliza documentação automática em `/docs`

---

### **2. Recepção de Requisição HTTP**

```
Cliente → Router → Service → Repository → Banco de Dados
   ↓         ↓        ↓          ↓            ↓
 HTTP     FastAPI   Lógica   SQLAlchemy    MySQL
```

**Exemplo: POST /api/players/{id}/distribution**

```python
# router.py
@router.post("/players/{player_id}/distribution")
def distribuicao_inicial(player_id: str):
    resultado = GestorCartas(GestorAPI(), None).gerarPokemonsIniciais(player_id)
    return resultado
```

---

### **3. Lógica de Negócio (Service Layer)**

```python
# service.py
def gerarPokemonsIniciais(self, idJogador: str):
    # 1. Gera 5 IDs aleatórios
    while len(pokemons_id) < 5:
        pokemon_id = random.randint(1, self.__api.getMaxID())
        
    # 2. Busca pokémons na PokéAPI
    pokemon = self.__api.getPokemon(pokemon_id, shiny=isShiny)
    
    # 3. Salva no banco de dados
    UsuarioRepository.adicionaUsuario(idJogador)
    PokemonRepository.adicionaPokemon(pokemon)
    UsuarioPokemonRepository.adicionarPokemonUsuario(idJogador, pokemon)
    
    # 4. Retorna resultado
    return {"status": "sucesso", "pokemons": pokemons}
```

---

### **4. Camada de Dados (Repository Pattern)**

**Padrão Repository** abstrai o acesso ao banco de dados:

```python
# repository.py
class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def adicionaUsuario(self, usuario: Jogador):
        # Converte entidade de domínio para ORM
        novo_usuario_orm = UsuarioToOrmAdapter(usuario)
        
        # Salva no banco
        self.db.add(novo_usuario_orm)
        self.db.commit()
```

---

### **5. Conversão de Dados (Adapters)**

**Adapters** convertem entre entidades de domínio e modelos ORM:

```python
# adapters.py
def pokemonToOrmAdapter(pokemon: Pokemon) -> PokemonORM:
    """Domain → Database"""
    return PokemonORM(
        idPokemon=pokemon.get_numero_pokedex(),
        nomePokemon=pokemon.get_nome(),
        isShiny=pokemon.is_shiny()
    )

def OrmTopokemonAdapter(pokemon_orm: PokemonORM) -> Pokemon:
    """Database → Domain"""
    return Pokemon(
        numero_pokedex=pokemon_orm.idPokemon,
        nome=pokemon_orm.nomePokemon,
        shiny=pokemon_orm.isShiny
    )
```

---

## 🎲 Componentes Principais

### **1. Entidades de Domínio (models.py)**

#### **Pokemon**
```python
class Pokemon:
    def __init__(self, numero_pokedex: int, nome: str, shiny: bool):
        self.__numero_pokedex = numero_pokedex
        self.__nome = nome
        self.__shiny = shiny
```
- Representa um Pokémon no domínio da aplicação
- Encapsula dados e comportamentos
- Independente de banco de dados

#### **Jogador**
```python
class Jogador:
    def __init__(self, id: str, pokemons: list = None):
        self.__id = id
        self.__pokemons = pokemons if pokemons else []
```
- Representa um jogador
- Mantém lista de pokémons (domínio)

---

### **2. Modelos ORM (models.py)**

#### **PokemonORM**
```python
class PokemonORM(Base):
    __tablename__ = 'Pokemon'
    
    idPokemon = Column(Integer, primary_key=True)
    nomePokemon = Column(String(25), nullable=False)
    isShiny = Column(Boolean, default=False)
```
- Mapeia tabela `Pokemon` do MySQL
- Gerenciado pelo SQLAlchemy

#### **UsuarioPokemonORM**
```python
class UsuarioPokemonORM(Base):
    __tablename__ = 'UsuarioPokemon'
    
    idUsuario = Column(String(20), ForeignKey('Usuario.idUsuario'), primary_key=True)
    idPokemon = Column(Integer, ForeignKey('Pokemon.idPokemon'), primary_key=True)
```
- Tabela de relacionamento N:N
- Conecta usuários e pokémons

---

### **3. Integração Externa (external.py)**

#### **GestorAPI (Singleton)**
```python
class GestorAPI:
    def getPokemon(self, numero_pokedex: int, shiny: bool) -> Pokemon:
        # 1. Faz requisição para PokéAPI
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{numero_pokedex}")
        
        # 2. Extrai dados
        data = response.json()
        nome = data['name']
        
        # 3. Retorna entidade de domínio
        return Pokemon(numero_pokedex, nome, shiny)
```
- **Singleton:** Uma única instância
- Busca dados da **PokéAPI** (https://pokeapi.co)
- Converte JSON → Objeto Pokemon

---

### **4. Gerenciamento de Sessão (database.py)**

```python
# Configuração do SQLAlchemy
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
```

- **SessionLocal:** Factory de sessões do banco
- Cada requisição cria uma nova sessão
- Garante isolamento de transações

---

## 🔀 Fluxos de Dados Detalhados

### **Fluxo 1: Distribuir Pokémons Iniciais**

```
1. Cliente faz POST /api/players/123/distribution
   ↓
2. Router recebe player_id="123"
   ↓
3. Service.gerarPokemonsIniciais("123")
   ├── Gera 5 números aleatórios [1-1025]
   ├── Para cada número:
   │   ├── GestorAPI.getPokemon(id, shiny)
   │   │   └── Requisição HTTP → pokeapi.co
   │   └── Adiciona à lista
   ├── UsuarioRepository.adicionaUsuario("123")
   │   └── INSERT INTO Usuario (idUsuario) VALUES ("123")
   ├── PokemonRepository.adicionaPokemon(pokemon)
   │   └── INSERT INTO Pokemon VALUES (id, nome, shiny)
   └── UsuarioPokemonRepository.adicionarPokemonUsuario("123", pokemon)
       └── INSERT INTO UsuarioPokemon VALUES ("123", id)
   ↓
4. Retorna JSON: {"status": "sucesso", "pokemons": [...]}
```

---

### **Fluxo 2: Buscar Time do Jogador**

```
1. Cliente faz GET /api/players/123/team
   ↓
2. Router → Service.obterTimeJogador("123")
   ↓
3. Repository busca no banco
   ├── SELECT * FROM Usuario WHERE idUsuario="123"
   ├── SELECT * FROM UsuarioPokemon WHERE idUsuario="123"
   └── JOIN com Pokemon para pegar dados completos
   ↓
4. Adapters convertem ORM → Domain
   ├── OrmToUsuarioAdapter(usuario_orm)
   └── OrmTopokemonAdapter(pokemon_orm)
   ↓
5. Service formata resposta JSON
   {
     "status": 200,
     "data": {
       "player": "123",
       "team": [
         {"pokemon_name": "pikachu", "is_shiny": false},
         ...
       ]
     }
   }
```

---

## 🔑 Conceitos Importantes

### **1. Dependency Injection**
```python
class UsuarioRepository:
    def __init__(self, db: Session):  # Sessão injetada
        self.db = db
```
- Repository recebe dependências (Session)
- Facilita testes (mock da Session)
- Desacopla componentes

---

### **2. Singleton Pattern**
```python
class GestorCartas:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
- Uma única instância na aplicação
- Economiza recursos (conexões API)

---

### **3. Adapter Pattern**
```python
# Domain → Database
pokemon_orm = pokemonToOrmAdapter(pokemon)

# Database → Domain
pokemon = OrmTopokemonAdapter(pokemon_orm)
```
- Isola camadas (domínio não conhece ORM)
- Facilita mudanças (trocar banco de dados)

---

### **4. Repository Pattern**
```python
# Abstração do banco de dados
class PokemonRepository:
    def adicionaPokemon(self, pokemon: Pokemon):
        # Lógica de persistência encapsulada
        pokemon_orm = pokemonToOrmAdapter(pokemon)
        self.db.add(pokemon_orm)
        self.db.commit()
```
- Centraliza acesso a dados
- Service não precisa saber SQL/ORM
- Facilita testes (mock do repository)

---

## 🗄️ Banco de Dados

### **Estrutura**

```sql
-- Tabela de Pokémons
Pokemon (
    idPokemon INT PRIMARY KEY,
    nomePokemon VARCHAR(25),
    isShiny BOOLEAN
)

-- Tabela de Usuários
Usuario (
    idUsuario VARCHAR(20) PRIMARY KEY
)

-- Relação N:N
UsuarioPokemon (
    idUsuario VARCHAR(20) FK → Usuario,
    idPokemon INT FK → Pokemon,
    PRIMARY KEY (idUsuario, idPokemon)
)
```

### **Relacionamentos**
- Um **usuário** pode ter **vários pokémons** (1:N)
- Um **pokémon** pode pertencer a **vários usuários** (N:M)
- Tabela `UsuarioPokemon` implementa N:M

---

## 🚀 Inicialização

### **1. Configurar Ambiente**
```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### **2. Configurar Banco**
```bash
# Criar .env
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=distribuicao_de_cartas

# Executar SQL
mysql -u root -p < banco-de-dados.sql
```

### **3. Executar Aplicação**
```bash
cd api-distribuicao
python3 -m uvicorn app.main:app --reload --port 8000
```

### **4. Acessar Documentação**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📝 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Health check |
| GET | `/api/players/{id}/team` | Lista pokémons do jogador |
| POST | `/api/players/{id}/distribution` | Distribui 5 pokémons iniciais |
| POST | `/api/players/{id}/team` | Adiciona pokémon ao jogador |
| DELETE | `/api/players/{id}/team` | Remove pokémon do jogador |
| PATCH | `/api/players/{id}/team` | Troca pokémon (não implementado) |
| POST | `/api/trades` | Troca entre jogadores (não implementado) |

---

## 🔍 Dicas de Debug

### **Ver Requisições SQL**
```python
# database.py
engine = create_engine(DB_URL, echo=True)  # Mostra SQL no console
```

### **Testar API Manualmente**
```bash
# Distribuir pokémons
curl -X POST http://localhost:8000/api/players/123/distribution

# Ver time
curl http://localhost:8000/api/players/123/team
```

### **Verificar Logs**
- Erros aparecem no terminal onde `uvicorn` está rodando
- Use `print()` para debug rápido
- FastAPI mostra stack traces completos

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)
- [PokéAPI](https://pokeapi.co/docs/v2)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

**Última atualização:** 04/12/2025
