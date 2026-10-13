"""Experimentos do relatório (Parte 1 e Parte 2)."""
import statistics
import time
from random import Random
from pathlib import Path

from src.heuristics import euclidean, manhattan
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost
from src.hill_climbing import hill_climbing, random_restart
from src.eight_queens import initial_board, render

MAP = Path("data/mapa_teste.txt")
REPEATS = 30

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
    tempos = []
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        resultado = fn(problem)
        tempos.append(time.perf_counter() - t0)
    mediana_ms = statistics.median(tempos) * 1000
    return resultado, mediana_ms

def parte1() -> None:
    print("## Parte 1: Problema do Mapa (Buscas)\n")
    problem = WeightedGrid.from_file(MAP)
    print("| Alg. | Heur. | Passos | Custo | Ger. | Exp. | Pico F. | Pico Mem. | Tempo (ms) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for nome, heur, fn in CONFIGS:
        r, mediana_ms = medir(fn, problem)
        print(f"| {nome} | {heur} | {len(r.actions)} | {r.cost} | {r.generated} | {r.expanded} | {r.peak_frontier} | {r.peak_stored_states} | {mediana_ms:.3f} |")
    print("\n")

def parte2() -> None:
    print("## Parte 2: Problema das 8 Rainhas (Hill Climbing & Random Restart)\n")
    seeds = range(100)
    
    hc_successes = 0
    hc_iterations = []
    hc_evaluated = []
    failed_run = None

    rr_successes = 0
    rr_iterations = []
    rr_evaluated = []
    rr_restarts = []

    for seed in seeds:
        rng_hc = Random(seed)
        initial = initial_board(rng_hc)
        res_hc = hill_climbing(initial)
        
        if res_hc.success:
            hc_successes += 1
        else:
            if failed_run is None:
                failed_run = (seed, res_hc.initial, res_hc.final, res_hc.initial_conflicts, res_hc.final_conflicts, res_hc.history)
                
        hc_iterations.append(res_hc.iterations)
        hc_evaluated.append(res_hc.evaluated_states)

        rng_rr = Random(seed)
        res_rr = random_restart(rng_rr, max_restarts=50)
        if res_rr.success:
            rr_successes += 1
        rr_iterations.append(res_rr.iterations)
        rr_evaluated.append(res_rr.evaluated_states)
        rr_restarts.append(res_rr.restarts)

    print(f"**Hill Climbing Puro (100 execuções):**")
    print(f"- Taxa de Sucesso: {hc_successes}%")
    print(f"- Média de Iterações: {statistics.mean(hc_iterations):.2f} (Mediana: {statistics.median(hc_iterations)})")
    print(f"- Média de Estados Avaliados: {statistics.mean(hc_evaluated):.2f}")
    if failed_run:
        print(f"  - Exemplo travado (Seed {failed_run[0]}): h inicial = {failed_run[3]}, h final = {failed_run[4]}, Histórico h = {failed_run[5]}")
        print(f"    Tabuleiro Inicial:\n{render(failed_run[1])}")
        print(f"    Tabuleiro Final:\n{render(failed_run[2])}")
    
    print(f"\n**Random Restart (100 execuções, max_restarts=50):**")
    print(f"- Taxa de Sucesso: {rr_successes}%")
    print(f"- Média de Iterações: {statistics.mean(rr_iterations):.2f} (Mediana: {statistics.median(rr_iterations)})")
    print(f"- Média de Estados Avaliados: {statistics.mean(rr_evaluated):.2f}")
    print(f"- Média de Reinícios: {statistics.mean(rr_restarts):.2f} (Máximo: {max(rr_restarts)})")
    print("\n")

def main() -> None:
    parte1()
    parte2()

if __name__ == "__main__":
    main()
