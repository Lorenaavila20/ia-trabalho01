# Trabalho 01 - Inteligência Artificial (CEFET-MG, 2026/2)

## Identificação da entrega

- **Aluno(a) 1:** Lorena Avila de Souza Silva
- **Aluno(a) 2:** Não se aplica
- **Repositório Git:** https://github.com/Lorenaavila20/ia-trabalho01
- **Tag:** `entrega-final`

Esta é a **entrega final**: Parte 1 (busca não informada e informada em grade ponderada) e Parte 2 (Hill Climbing e Random-Restart Hill Climbing nas 8 Rainhas). O relatório em PDF acompanha o projeto (`relatorio.pdf`).

## Instalação e execução

Requer Python 3.10 ou superior (testado com Python 3.12.3), sem dependências externas além da biblioteca padrão.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Parte 1: uma busca (algoritmos: bfs, dfs, ucs, greedy, astar; heurísticas: manhattan, euclidean)
python -m src.main busca --map data/mapa_teste.txt --algorithm astar --heuristic manhattan

# Parte 2: 8 Rainhas
python -m src.main rainhas --algorithm hill --seed 42
python -m src.main rainhas --algorithm restart --seed 42 --max-restarts 50

# Reproduz as tabelas do relatório (Parte 1 e Parte 2, sementes 0 a 99)
python -m scripts.run_experiments

# Testes automatizados
python -m unittest discover -s tests -v
```

## Organização

- `src/problem.py`: leitura do mapa, sucessores (N, L, S, O) e custos.
- `src/search.py`: BFS, DFS, UCS, Gulosa e A*.
- `src/heuristics.py`: distâncias Manhattan e Euclidiana.
- `src/eight_queens.py`: representação, função de avaliação (`conflicts`) e vizinhança (`moves`).
- `src/hill_climbing.py`: Hill Climbing e Random-Restart Hill Climbing.
- `src/models.py`: `SearchResult` com as métricas da Parte 1.
- `tests/`: testes do problema, das buscas (início adjacente ao objetivo, mapa sem solução, ciclos, rotas com o mesmo número de ações, rota curta e cara × longa e barata, DFS não ótima) e das 8 Rainhas.
- `scripts/run_experiments.py`: gera as tabelas da Parte 1 e da Parte 2.
- `results/`: saídas dos experimentos.
- `relatorio.pdf`: relatório final.
- `IA_USAGE.md`: registro do uso de IA.

## Decisões de implementação

### Parte 1

- **Descoberto na inserção (BFS e DFS):** o estado é marcado ao entrar na fronteira.
- **Teste de objetivo ao retirar da fronteira**, em todos os algoritmos. O objetivo não conta como expandido.
- **DFS:** os sucessores entram na pilha em ordem inversa, para que o Norte seja expandido primeiro.
- **UCS e A\*:** prioridade `(g, ordem)` e `(f, h, ordem)`. Reinserção por melhora de custo conta como nova geração, e entradas obsoletas do heap são ignoradas, sem contar como expansão.
- **Gulosa:** prioridade `(h, ordem)`; cada estado entra uma única vez.
- **Pico de memória:** máximo de estados distintos em fronteira ∪ explorados.
- **Heurísticas:** o menor custo de passo é 1 e os movimentos são em 4 direções, então Manhattan e Euclidiana nunca superestimam o custo restante.

### Parte 2

- **Estado:** vetor de 8 inteiros (índice = coluna, valor = linha), gerado com `randrange(8)` por coluna a partir de `random.Random(seed)`.
- **Avaliação:** `h(s)` = número de pares de rainhas em conflito (mesma linha ou diagonal).
- **Hill Climbing:** avalia os 56 vizinhos (coluna 0 a 7, linha 0 a 7), escolhe o primeiro entre os de menor `h` e só se move com melhora estrita, sem movimentos laterais.
- **Contagens:** uma iteração é um movimento aceito. Estados avaliados incluem o estado inicial e todos os vizinhos de cada varredura, inclusive a última, sem melhora.
- **Random-Restart:** reutiliza o mesmo gerador, com no máximo 51 tentativas (1 inicial + 50 reinícios). `restarts` é o número de tentativas menos 1. Iterações e estados avaliados são acumulados entre as tentativas.

## Resultados da Parte 1 (`data/mapa_teste.txt`)

| Alg. | Heur. | Passos | Custo | Ger. | Exp. | Pico F. | Pico Mem. | Tempo (ms) |
|---|---|---|---|---|---|---|---|---|
| BFS | - | 15 | 40 | 66 | 59 | 9 | 66 | 0.088 |
| DFS | - | 15 | 40 | 21 | 15 | 6 | 21 | 0.029 |
| UCS | - | 29 | 29 | 77 | 74 | 6 | 77 | 0.151 |
| Gulosa | Manhattan | 15 | 40 | 21 | 15 | 6 | 21 | 0.034 |
| A* | Manhattan | 29 | 29 | 60 | 43 | 15 | 58 | 0.109 |
| Gulosa | Euclidiana | 15 | 40 | 21 | 15 | 6 | 21 | 0.032 |
| A* | Euclidiana | 29 | 29 | 72 | 60 | 12 | 72 | 0.134 |

O tempo é a mediana de 30 execuções, sem contar a leitura do arquivo, e varia entre máquinas e rodadas.

### Caminhos

BFS, DFS e Gulosa (15 passos, custo 40):

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

UCS e A* com Manhattan (29 passos, custo 29):

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

O A* com Euclidiana também tem custo 29, por uma rota que difere nos últimos passos.

## Resultados da Parte 2 (sementes 0 a 99)

| Métrica | Hill Climbing | Random Restart |
|---|---|---|
| Taxa de sucesso | 12% | 100% |
| Média de iterações | 3,28 | 24,72 |
| Mediana de iterações | 3,0 | 17,5 |
| Média de estados avaliados | 240,68 | 1826,64 |
| Reinícios (média / máximo) | - | 6,76 / 42 |

Exemplo de falha do Hill Climbing (seed 0): estado inicial `[6, 6, 0, 4, 7, 6, 4, 7]` (h = 9), trajetória de h `[9, 6, 4, 3, 2]` e estado final `[6, 3, 5, 2, 1, 6, 4, 7]` com h = 2. Dos 56 vizinhos, nenhum melhora, 3 empatam e 53 pioram.

## Uso de IA

Registrado em `IA_USAGE.md`.