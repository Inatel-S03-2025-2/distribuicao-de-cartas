#  Distribuição de cartas

## Descrição do Tema:
Responsável por escolher cinco Pokémons aleatórios, disponibilizados pela [**PokéAPI**](https://pokeapi.co), e reservar para cada jogador cadastrado. Esse processo deve ser feito assim que o jogador realiza seu cadastro. A aplicação deve registrar as informações e fornecer uma interface para consulta de outras aplicações. Um mesmo jogador não deve ter Pokémons repetidos, mas o mesmo Pokémon pode ser distribuído para outros jogadores.

## Grupo
|**Nome**|**Matrícula**|
|--------|-------------|
|Felipe Ferreira|380|
|Felipe Silva Loschi|601|
|Henrique Oliveira Camppelo|367|
|Pedro Henrique Duarte|210|
|Pedro Henrique Ribeiro|529|
|Vitor Algusto|459|

## Documentação
### UML


### Aplicação do Princípio SOLIDD
#### Single Responsability
- A classe **Pokemon** segue o Princípio da Responsabilidade Única, pois sua única função é encapsular os dados de um Pokémon.
- A classe **StatusDistribuicao** segue o Princípio da Responsabilidade Única, assim como a classe anterior pois somente encapsula os dados de um Log de resposta da Feature Distribuição de Cartas.

#### Open/Close
- Seguindo este princípio, a classe **GestorCartas** é fechada porque seu código é estável, mas aberta porque podemos adicionar novas funcionalidades sem reescrever o que já existe.
- A classe **GerenciadorAPI** é fechada porque seu código não precisa de modificações de funcionalidade, porem, se necessário é possível adicionar mais métodos de usos para a PokeAPI.

#### Liskov Substitution
*Como nossa Feature não possui nenhuma relação de herança entre as classe, portanto não há como aplicar este principio.*

#### Interface Segregation
- A classe **GerenciadorAPI** é pequena e específica para a leitura de dados. Isso evita que as classes sejam forçadas a implementar métodos que não utilizam, como de escrita ou deleção.

#### Dependency Inversion
- A classe **GestorCartas** não depende de uma implementação concreta de como buscar um Pokémon. Em vez disso, ela depende da abstração **GerenciadorAPI**.

#### Demeter
No momento que a classe **GestorCartas** possui um objeto da classe **GerenciadorAPI** ele aplica o principio de Demeter ao só utilizar métodos próprios, ou de objetos que foram passados como parâmetro.
