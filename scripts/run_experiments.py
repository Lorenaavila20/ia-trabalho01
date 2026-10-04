"""Experimentos do relatório."""
import statistics
import time
from pathlib import Path

from src.heuristics import euclidean, manhattan
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost

MAP = Path("data/mapa_teste.txt")
REPEATS = 30

# Mesma ordem da tabela do enunciado (seção 2.7)
CONFIGS = [
    ("BFS", "-", bfs),
    ("DFS", "-", dfs),
    ("UCS", "-", uniform_cost),
    ("Gulosa", "Manhattan", lambda p: greedy(p, manhattan)),
    ("A*", "Manhattan", lambda p: astar(p, manhattan)),
    ("Gulosa", "Euclidiana", lambda p: greedy(p, euclidean)),
    ("A*", "Euclidiana", lambda p: astar(p, euclidean)),
]

def medir(fn, problem):
    """Roda fn(problem) REPEATS vezes e devolve (resultado, mediana em ms)."""
    tempos = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        resultado = fn(problem)
        tempos.append(time.perf_counter() - t0)
        
    mediana_ms = statistics.median(tempos) * 1000
    
    return resultado, mediana_ms

def parte1() -> None:
    problem = WeightedGrid.from_file(MAP)   # leitura do arquivo fica fora da medição
    
    print("| Alg. | Heur. | Passos | Custo | Ger. | Exp. | Pico F. | Pico Mem. | Tempo (ms) |")
    print("|---|---|---|---|---|---|---|---|---|")
    
    for nome, heur, fn in CONFIGS:
        r, mediana_ms = medir(fn, problem)
        
        # Obs: Utilizado len(r.actions) para representar os "passos". 
        # Se a sua classe SearchResult possuir uma propriedade específica chamada 'steps',
        # basta substituir len(r.actions) por r.steps
        print(f"| {nome} | {heur} | {len(r.actions)} | {r.cost} | {r.generated} | {r.expanded} | {r.peak_frontier} | {r.peak_stored_states} | {mediana_ms:.3f} |")

def main() -> None:
    parte1()
    # Parte 2 (8 Rainhas, seeds 0..99): fica para depois de implementar o Hill Climbing

if __name__ == "__main__":
    main()