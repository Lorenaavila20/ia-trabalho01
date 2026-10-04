"""Testes mínimos da Parte 1 (seção 2.8 do enunciado).

Rode com:
    python -m unittest discover -s tests -v
"""
import math
import unittest
from pathlib import Path

from src.heuristics import euclidean, manhattan
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost

PUBLIC_MAP = Path(__file__).resolve().parent.parent / "data" / "mapa_teste.txt"

ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "ucs": uniform_cost,
    "greedy-manhattan": lambda p: greedy(p, manhattan),
    "greedy-euclidean": lambda p: greedy(p, euclidean),
    "astar-manhattan": lambda p: astar(p, manhattan),
    "astar-euclidean": lambda p: astar(p, euclidean),
}


def make_grid(text: str) -> WeightedGrid:
    return WeightedGrid([list(line) for line in text.strip().splitlines()])


class SearchTestCase(unittest.TestCase):
    def assert_valid_solution(self, problem: WeightedGrid, result) -> None:
        """Consistência interna: caminho, ações, custo e métricas."""
        self.assertTrue(result.found)
        path = result.path
        self.assertEqual(path[0], problem.start)
        self.assertEqual(path[-1], problem.goal)
        self.assertEqual(len(result.actions), len(path) - 1)
        for a, b in zip(path, path[1:]):
            self.assertEqual(abs(a[0] - b[0]) + abs(a[1] - b[1]), 1)
            self.assertTrue(problem.in_bounds(b) and problem.passable(b))
        self.assertEqual(result.cost, sum(problem.step_cost(p) for p in path[1:]))
        self.assertGreaterEqual(result.generated, 1)
        self.assertLessEqual(result.expanded, result.generated)
        self.assertGreaterEqual(result.peak_frontier, 1)
        self.assertGreaterEqual(result.peak_stored_states, result.peak_frontier)

    def run_all(self, problem: WeightedGrid) -> dict:
        return {name: fn(problem) for name, fn in ALGORITHMS.items()}


class TestHeuristics(unittest.TestCase):
    def test_values(self):
        self.assertEqual(manhattan((0, 0), (3, 4)), 7)
        self.assertEqual(euclidean((0, 0), (3, 4)), 5)
        self.assertEqual(manhattan((2, 2), (2, 2)), 0)
        self.assertEqual(euclidean((2, 2), (2, 2)), 0)

    def test_symmetry(self):
        self.assertEqual(manhattan((1, 5), (4, 2)), manhattan((4, 2), (1, 5)))
        self.assertAlmostEqual(euclidean((1, 5), (4, 2)), euclidean((4, 2), (1, 5)))

    def test_euclidean_never_above_manhattan(self):
        for a, b in [((0, 0), (3, 4)), ((1, 1), (1, 9)), ((5, 2), (0, 0))]:
            self.assertLessEqual(euclidean(a, b), manhattan(a, b) + 1e-9)


class TestInicioAdjacenteAoObjetivo(SearchTestCase):
    def test_adjacent(self):
        problem = make_grid("SG")
        for name, result in self.run_all(problem).items():
            with self.subTest(algorithm=name):
                self.assert_valid_solution(problem, result)
                self.assertEqual(result.steps, 1)
                self.assertEqual(result.cost, 1)


class TestSemSolucao(SearchTestCase):
    def test_no_solution(self):
        problem = make_grid("S#G")
        for name, result in self.run_all(problem).items():
            with self.subTest(algorithm=name):
                self.assertFalse(result.found)
                self.assertEqual(result.path, [])
                self.assertEqual(result.cost, math.inf)

    def test_no_solution_enclosed_goal(self):
        problem = make_grid("S.#..\n..#.G\n..#..")
        for name, result in self.run_all(problem).items():
            with self.subTest(algorithm=name):
                self.assertFalse(result.found)


class TestCiclos(SearchTestCase):
    def test_open_map_with_cycles_terminates(self):
        problem = make_grid("S..\n.#.\n..G")
        for name, result in self.run_all(problem).items():
            with self.subTest(algorithm=name):
                self.assert_valid_solution(problem, result)

    def test_rectangular_open_map(self):
        problem = make_grid("S....\n.....\n....G")
        for name, result in self.run_all(problem).items():
            with self.subTest(algorithm=name):
                self.assert_valid_solution(problem, result)
        self.assertEqual(bfs(problem).steps, 6)


class TestRotasComMesmoNumeroDeAcoes(SearchTestCase):
    def test_tie_broken_by_successor_order(self):
        # Duas rotas de 2 ações: via (0,1) [Leste] ou via (1,0) [Sul].
        # Ordem N -> L -> S -> O: Leste vem antes de Sul.
        problem = make_grid("S.\n.G")
        for name, result in self.run_all(problem).items():
            with self.subTest(algorithm=name):
                self.assert_valid_solution(problem, result)
                self.assertEqual(result.steps, 2)
                self.assertEqual(result.cost, 2)
        self.assertEqual(bfs(problem).path, [(0, 0), (0, 1), (1, 1)])
        self.assertEqual(uniform_cost(problem).path, [(0, 0), (0, 1), (1, 1)])


class TestCurtaCaraVersusLongaBarata(SearchTestCase):
    MAP = "SMG\n..."

    def test_bfs_shortest_actions_but_not_cheapest(self):
        problem = make_grid(self.MAP)
        result = bfs(problem)
        self.assert_valid_solution(problem, result)
        self.assertEqual(result.steps, 2)
        self.assertEqual(result.cost, 7)

    def test_ucs_cheapest_but_more_actions(self):
        problem = make_grid(self.MAP)
        result = uniform_cost(problem)
        self.assert_valid_solution(problem, result)
        self.assertEqual(result.steps, 4)
        self.assertEqual(result.cost, 4)

    def test_astar_optimal_with_both_heuristics(self):
        problem = make_grid(self.MAP)
        for name in ("astar-manhattan", "astar-euclidean"):
            with self.subTest(algorithm=name):
                result = ALGORITHMS[name](problem)
                self.assert_valid_solution(problem, result)
                self.assertEqual(result.cost, 4)

    def test_greedy_is_not_optimal_here(self):
        problem = make_grid(self.MAP)
        for name in ("greedy-manhattan", "greedy-euclidean"):
            with self.subTest(algorithm=name):
                result = ALGORITHMS[name](problem)
                self.assert_valid_solution(problem, result)
                self.assertEqual(result.cost, 7)


class TestMapaPublico(SearchTestCase):
    def setUp(self):
        self.problem = WeightedGrid.from_file(PUBLIC_MAP)
        self.results = self.run_all(self.problem)

    def test_all_find_valid_solution(self):
        for name, result in self.results.items():
            with self.subTest(algorithm=name):
                self.assert_valid_solution(self.problem, result)

    def test_bfs_minimizes_actions(self):
        best = min(r.steps for r in self.results.values())
        self.assertEqual(self.results["bfs"].steps, best)

    def test_ucs_and_astar_minimize_cost(self):
        best = min(r.cost for r in self.results.values())
        for name in ("ucs", "astar-manhattan", "astar-euclidean"):
            with self.subTest(algorithm=name):
                self.assertEqual(self.results[name].cost, best)

    def test_deterministic(self):
        again = self.run_all(self.problem)
        for name in ALGORITHMS:
            with self.subTest(algorithm=name):
                self.assertEqual(self.results[name].path, again[name].path)
                self.assertEqual(self.results[name].generated, again[name].generated)
                self.assertEqual(self.results[name].expanded, again[name].expanded)

class TestDfsNaoOtima(SearchTestCase):
    def test_dfs_longer_than_bfs(self):
        problem = make_grid("S...\n....\nG...")
        r_bfs, r_dfs = bfs(problem), dfs(problem)
        self.assert_valid_solution(problem, r_bfs)
        self.assert_valid_solution(problem, r_dfs)
        self.assertEqual(r_bfs.steps, 2)
        self.assertEqual(r_dfs.steps, 8)
        
if __name__ == "__main__":
    unittest.main()
