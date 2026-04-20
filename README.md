
# Projeto2_Solitaire — Funcionalidades Extra

Este documento descreve as funcionalidades extra implementadas como extensão do jogo Solitaire, justificando a sua inclusão e explicando o seu comportamento em detalhe. 

## Funcionalidade: Ecrã Azul de Erro (Easter Egg)

Motivação e descrição detalhada:

Esta funcionalidade foi adicionada como um Easter egg lúdico e temático (estamos em época de Páscoa). Quando o utilizador carrega três vezes seguidas no elemento que mostra o `score`, o jogo apresenta um ecrã azul de erro simulado. O objectivo não é indicar uma falha real, mas fornecer um momento surpreendente e divertido que recompensa a curiosidade dos jogadores mais aventureiros.

O ecrã reproduz visualmente elementos típicos de um crash (fundo azul, mensagem destacada e uma “stack trace” fictícia), mas com mensagens humorísticas. Esta escolha permite demonstrar controlo sobre a interface e acrescenta valor de design e creatividade.

Impacto na avaliação:

Esta funcionalidade demonstra capacidade de criar interacções não triviais na UI, gestão de eventos de input (detecção de três cliques) e design criativo para o utilizador perceber que os devs se preocupam com os detalhes e com o consumidor final. A implementação exige controlo de estado, sobreposição de ecrã e competências relevantes para o objetivo avaliado.

Instruções de utilização:

- Para activar: clicar três vezes rapidamente no indicador do `score`.


## Funcionalidade: Contador de Movimentos

Motivação e descrição detalhada:

O contador de movimentos contabiliza cada acção válida do jogador durante a partida. Esta métrica é uma medida de eficiência e estratégia, importante para jogadores que queiram optimizar as suas soluções ou comparar desempenhos entre partidas. A inclusão do contador valoriza o aspecto competitivo e analítico do jogo sem alterar as regras base.

O contador incrementa quando o utilizador realiza um movimento válido (por exemplo, mover uma carta entre slots). Está ligado à lógica de jogo para evitar contagens por acções inválidas ou por desfazer/repôr movimentos quando apropriado. O valor é exibido permanentemente na interface, ao lado do `score`, com atualização em tempo real.

Impacto na avaliação:

Esta funcionalidade evidencia compreensão da lógica de jogo, ligações entre UI e estado interno, e atenção à usabilidade da app, (feedback imediato e persistência durante a sessão). Contabilizar movimentos implica manipular dados de eventos, testar condições de validade e garantir consistência após operações como reiniciar o jogo.

Instruções de utilização:

- O número de movimentos aparece ao lado do `score` na interface principal.
- Para reiniciar o contador: O Utilizador deve iniciar uma nova partida (ou utilizar a tecla de reinício, se disponível).

## Como executar

Para correr a aplicação localmente, a partir da raíz do projecto execute:

```bash
python -m Solitaire.main
```

Ou, conforme o ambiente de desenvolvimento, use o comando de execução configurado (por exemplo, `uv run main.py`).
