import heapq
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


def bfs(problem: WeightedGrid) -> SearchResult:
    inicio = problem.start
    fila = deque([inicio])
    descobertos = {inicio}
    parent = {}

    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored = 1

    while fila:
        atual = fila.popleft()

        if problem.goal_test(atual):
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
            cost = sum(problem.step_cost(p) for p in path[1:])

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

        peak_frontier = max(peak_frontier, len(fila))
        peak_stored = max(peak_stored, len(descobertos))

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
    """Busca em Profundidade (DFS)."""
    inicio = problem.start
    pilha = [inicio]            # Usa lista como pilha LIFO
    descobertos = {inicio}      # Marcado ao inserir na fronteira
    parent = {}

    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored = 1

    while pilha:
        atual = pilha.pop()

        if problem.goal_test(atual):
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
            cost = sum(problem.step_cost(p) for p in path[1:])

            return SearchResult(
                found=True,
                algorithm="dfs",
                path=path,
                actions=actions,
                cost=cost,
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )

        expanded += 1

        # Reverte a lista de sucessores para que o primeiro sucessor (ex: Norte)
        # fique no topo da pilha e seja removido/expandido primeiro
        for acao, destino, custo in reversed(list(problem.successors(atual))):
            if destino not in descobertos:
                descobertos.add(destino)
                parent[destino] = (atual, acao)
                pilha.append(destino)
                generated += 1

        peak_frontier = max(peak_frontier, len(pilha))
        peak_stored = max(peak_stored, len(descobertos))

    return SearchResult(
        found=False,
        algorithm="dfs",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored,
    )

def uniform_cost(problem: WeightedGrid) -> SearchResult:
    """Busca de Custo Uniforme (UCS / Dijkstra)."""
    inicio = problem.start
    counter = 0

    # Fila de prioridade: (custo, contador_desempate, estado)
    frontier = [(0, counter, inicio)]
    na_fronteira = {inicio}  # Conjunto para rastrear estados distintos na fronteira
    parent = {}
    cost_so_far = {inicio: 0}

    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored = 1

    while frontier:
        current_cost, _, atual = heapq.heappop(frontier)

        # 3. Descarte de entradas obsoletas ANTES do teste de objetivo
        if current_cost > cost_so_far[atual]:
            continue

        # Remove o estado válido da fronteira ao ser retirado para expansão
        na_fronteira.discard(atual)

        if problem.goal_test(atual):
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

            return SearchResult(
                found=True,
                algorithm="ucs",
                path=path,
                actions=actions,
                cost=current_cost,
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )

        expanded += 1

        for acao, destino, custo_passo in problem.successors(atual):
            novo_custo = current_cost + custo_passo
            if destino not in cost_so_far or novo_custo < cost_so_far[destino]:
                cost_so_far[destino] = novo_custo
                parent[destino] = (atual, acao)
                counter += 1
                heapq.heappush(frontier, (novo_custo, counter, destino))

                # 1. Contagem de geração a cada inserção (inclusive reinserções)
                generated += 1

                # 2. Rastreamento do estado na fronteira
                na_fronteira.add(destino)

        # Atualização dos picos usando o conjunto de estados distintos
        peak_frontier = max(peak_frontier, len(na_fronteira))
        peak_stored = max(peak_stored, len(cost_so_far))

    return SearchResult(
        found=False,
        algorithm="ucs",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored,
    )

def greedy(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca Gulosa pelo melhor primeiro (Greedy Best-First Search)."""
    inicio = problem.start
    goal = problem.goal
    counter = 0

    h_init = heuristic(inicio, goal)
    # Fila de prioridade baseada apenas no valor da heurística h(n)
    frontier = [(h_init, counter, inicio)]
    descobertos = {inicio}
    parent = {}

    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored = 1

    while frontier:
        _, _, atual = heapq.heappop(frontier)

        if problem.goal_test(atual):
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
            cost = sum(problem.step_cost(p) for p in path[1:])

            return SearchResult(
                found=True,
                algorithm="greedy",
                path=path,
                actions=actions,
                cost=cost,
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )

        expanded += 1

        for acao, destino, _ in problem.successors(atual):
            if destino not in descobertos:
                descobertos.add(destino)
                parent[destino] = (atual, acao)
                counter += 1
                h_val = heuristic(destino, goal)
                heapq.heappush(frontier, (h_val, counter, destino))
                generated += 1

        peak_frontier = max(peak_frontier, len(frontier))
        peak_stored = max(peak_stored, len(descobertos))

    return SearchResult(
        found=False,
        algorithm="greedy",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored,
    )

def astar(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca A* (A-Star)."""
    inicio = problem.start
    goal = problem.goal
    counter = 0

    g_score = {inicio: 0}
    h_init = heuristic(inicio, goal)
    f_init = h_init

    # Fila de prioridade: (f, h, contador_desempate, g, estado)
    frontier = [(f_init, h_init, counter, 0, inicio)]
    na_fronteira = {inicio}
    parent = {}

    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored = 1

    while frontier:
        _, _, _, current_g, atual = heapq.heappop(frontier)

        # Descarte de entradas obsoletas ANTES do teste de objetivo
        if current_g > g_score[atual]:
            continue

        na_fronteira.discard(atual)

        if problem.goal_test(atual):
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

            return SearchResult(
                found=True,
                algorithm="astar",
                path=path,
                actions=actions,
                cost=g_score[atual],
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )

        expanded += 1

        for acao, destino, custo_passo in problem.successors(atual):
            tentative_g = current_g + custo_passo
            if destino not in g_score or tentative_g < g_score[destino]:
                g_score[destino] = tentative_g
                parent[destino] = (atual, acao)
                counter += 1
                
                h_dest = heuristic(destino, goal)
                f_score = tentative_g + h_dest
                
                # Tupla ajustada com h_dest como segundo critério de desempate
                heapq.heappush(frontier, (f_score, h_dest, counter, tentative_g, destino))

                generated += 1
                na_fronteira.add(destino)

        peak_frontier = max(peak_frontier, len(na_fronteira))
        peak_stored = max(peak_stored, len(g_score))

    return SearchResult(
        found=False,
        algorithm="astar",
        path=[],
        actions=[],
        cost=float("inf"),
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored,
    )