import math
from collections import deque
from collections.abc import Callable

from .models import SearchResult
from .problem import WeightedGrid

Heuristic = Callable[[tuple[int, int], tuple[int, int]], float]


def bfs(problem: WeightedGrid) -> SearchResult:
    inicio = problem.start
    fila = deque([inicio])      # estados esperando para serem expandidos
    descobertos = {inicio}      # estados que já entraram na fila alguma vez
    parent = {}                 # destino -> (de onde veio, ação)
    
    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored = 1

    while fila:
        atual = fila.popleft()

        if problem.goal_test(atual):
            # 2. Reconstrução do caminho (posições de inicio até goal) e ações
            no = atual
            path = [no]
            actions = []

            while no != inicio:
                pai, acao = parent[no]
                actions.append(acao)
                path.append(pai)
                no = pai

            path.reverse()
            actions.reverse()

            # 3. Cálculo do custo acumulado a partir de path[1:]
            cost = sum(problem.step_cost(p) for p in path[1:])

            # 1. Retorno nomeado de sucesso com todas as estatísticas
            return SearchResult(
                found=True,
                algorithm="bfs",
                path=path,
                actions=actions,
                cost=cost,
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )

        expanded += 1
        for acao, destino, custo in problem.successors(atual):
            if destino not in descobertos:
                descobertos.add(destino)
                parent[destino] = (atual, acao)
                fila.append(destino)
                generated += 1

        # Atualiza os picos da fronteira e de estados armazenados
        peak_frontier = max(peak_frontier, len(fila))
        peak_stored = max(peak_stored, len(descobertos))

    # 4. Caso a fila esvazie sem encontrar o objetivo (falha)
    return SearchResult(
        found=False,
        algorithm="bfs",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored,
    )

def dfs(problem: WeightedGrid) -> SearchResult:
    """Busca em Profundidade. Implemente conforme a especificação do trabalho."""
    raise NotImplementedError("Implemente DFS.")


def uniform_cost(problem: WeightedGrid) -> SearchResult:
    """Busca de Custo Uniforme. Implemente conforme a especificação do trabalho."""
    raise NotImplementedError("Implemente UCS.")


def greedy(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca Gulosa pelo melhor primeiro."""
    raise NotImplementedError("Implemente Busca Gulosa.")


def astar(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca A*."""
    raise NotImplementedError("Implemente A*.")
