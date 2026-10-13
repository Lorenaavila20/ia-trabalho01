## Parte 1: Problema do Mapa (Buscas)

| Alg. | Heur. | Passos | Custo | Ger. | Exp. | Pico F. | Pico Mem. | Tempo (ms) |
|---|---|---|---|---|---|---|---|---|
| BFS | - | 15 | 40 | 66 | 59 | 9 | 66 | 0.088 |
| DFS | - | 15 | 40 | 21 | 15 | 6 | 21 | 0.029 |
| UCS | - | 29 | 29 | 77 | 74 | 6 | 77 | 0.151 |
| Gulosa | Manhattan | 15 | 40 | 21 | 15 | 6 | 21 | 0.034 |
| A* | Manhattan | 29 | 29 | 60 | 43 | 15 | 58 | 0.109 |
| Gulosa | Euclidiana | 15 | 40 | 21 | 15 | 6 | 21 | 0.032 |
| A* | Euclidiana | 29 | 29 | 72 | 60 | 12 | 72 | 0.134 |


## Parte 2: Problema das 8 Rainhas (Hill Climbing & Random Restart)

**Hill Climbing Puro (100 execuções):**
- Taxa de Sucesso: 12%
- Média de Iterações: 3.28 (Mediana: 3.0)
- Média de Estados Avaliados: 240.68
  - Exemplo travado (Seed 0): h inicial = 9, h final = 2, Histórico h = [9, 6, 4, 3, 2]
    Tabuleiro Inicial:
. . Q . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . Q . . Q .
. . . . . . . .
Q Q . . . Q . .
. . . . Q . . Q
    Tabuleiro Final:
. . . . . . . .
. . . . Q . . .
. . . Q . . . .
. Q . . . . . .
. . . . . . Q .
. . Q . . . . .
Q . . . . Q . .
. . . . . . . Q

**Random Restart (100 execuções, max_restarts=50):**
- Taxa de Sucesso: 100%
- Média de Iterações: 24.72 (Mediana: 17.5)
- Média de Estados Avaliados: 1826.64
- Média de Reinícios: 6.76 (Máximo: 42)


