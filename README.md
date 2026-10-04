# Trabalho 01 - Inteligência Artificial (CEFET-MG, 2026/2)

## Identificação da entrega

- **Aluno(a) 1:** Lorena Ávila
- **Aluno(a) 2:** <nome ou não se aplica>
- **Repositório Git:** <link do repositório>
- **Tag:** `entrega-parte1`

Esta entrega contém a **Parte 1** (busca não informada e informada). A Parte 2 (Hill Climbing nas 8 Rainhas) será entregue em 15/10/2026.

## Instalação e execução

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# uma busca (algoritmos: bfs, dfs, ucs, greedy, astar; heurísticas: manhattan, euclidean)
python -m src.main busca --map data/mapa_teste.txt --algorithm astar --heuristic manhattan

# tabela de resultados (mediana de 30 execuções)
python -m scripts.run_experiments

# testes
python -m unittest discover -s tests -v
```

## Organização

- `src/problem.py`: leitura do mapa, sucessores (N, L, S, O) e custos.
- `src/search.py`: BFS, DFS, UCS, Gulosa e A*.
- `src/heuristics.py`: distâncias Manhattan e Euclidiana.
- `src/models.py`: `SearchResult` com as métricas.
- `tests/`: testes do problema e das buscas (início adjacente ao objetivo, mapa sem solução, ciclos, rotas com o mesmo número de ações, rota curta e cara × longa e barata).
- `scripts/run_experiments.py`: gera a tabela da Parte 1.

## Decisões de implementação

- **Descoberto na inserção (BFS e DFS):** o estado é marcado ao entrar na fronteira.
- **Teste de objetivo ao retirar da fronteira**, em todos os algoritmos. O objetivo não conta como expandido.
- **DFS:** os sucessores entram na pilha em ordem inversa, para que o Norte seja expandido primeiro.
- **UCS e A\*:** prioridade `(g, ordem)` e `(f, h, ordem)`. Reinserção por melhora de custo conta como nova geração, e entradas obsoletas do heap são ignoradas, sem contar como expansão.
- **Gulosa:** prioridade `(h, ordem)`; cada estado entra uma única vez.
- **Pico de memória:** máximo de estados distintos em fronteira ∪ explorados.
- **Heurísticas:** o menor custo de passo é 1 e os movimentos são em 4 direções, então Manhattan e Euclidiana nunca superestimam o custo restante.

## Resultados no mapa público (`data/mapa_teste.txt`)

| Alg. | Heur. | Passos | Custo | Ger. | Exp. | Pico F. | Pico Mem. | Tempo (ms) |
|---|---|---|---|---|---|---|---|---|
| BFS | - | 15 | 40 | 66 | 59 | 9 | 66 | 0.088 |
| DFS | - | 15 | 40 | 21 | 15 | 6 | 21 | 0.027 |
| UCS | - | 29 | 29 | 77 | 74 | 6 | 77 | 0.140 |
| Gulosa | Manhattan | 15 | 40 | 21 | 15 | 6 | 21 | 0.030 |
| A* | Manhattan | 29 | 29 | 60 | 43 | 15 | 58 | 0.094 |
| Gulosa | Euclidiana | 15 | 40 | 21 | 15 | 6 | 21 | 0.031 |
| A* | Euclidiana | 29 | 29 | 72 | 60 | 12 | 72 | 0.133 |

O tempo é a mediana de 30 execuções, sem contar a leitura do arquivo, e varia entre máquinas e rodadas.

## Caminhos no mapa público

BFS (15 passos, custo 40; DFS e Gulosa produzem o mesmo caminho):

```
S**************G
.#.#####.####...
.#.....#....#...
.#####.#.##.#...
.....#.#....#...
####.#.######...
.....#...R.R....
................
```

UCS (29 passos, custo 29):

```
S**MMMMM.....**G
.#*#####.####*..
.#*****#....#*..
.#####*#.##.#*..
.....#*#....#*..
####.#*######*..
.....#***R.R**..
........*****...
```

## Uso de IA

Registrado em `IA_USAGE.md`.