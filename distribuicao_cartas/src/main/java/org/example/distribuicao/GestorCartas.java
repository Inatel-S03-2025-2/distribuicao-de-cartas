package org.example.distribuicao;

public class GestorCartas {
    private String idJogador; //Não deveria ser um int?
    private Pokemon pokemons;
    private GerenciadorAPI api;

    public void setApi(GerenciadorAPI api) {
        this.api = api;
    }

    public void gerarPokemonsIniciais() {

    }

    public StatusDistribuicao removerPokemon(int idPokemon) {
        return null;
    }

    public StatusDistribuicao trocarPokemonADM(int idSaindo, int idEntrando) {
        return null;
    }

    public StatusDistribuicao trocarPokemonPlayer(String nomePlayer, int idSaindo, int idEntrando) {
        return null;
    }

    //public Json listarPokemons(String filtro) {
    //}
}
