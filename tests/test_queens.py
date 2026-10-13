import unittest
from random import Random
from src.eight_queens import conflicts, moves, initial_board
from src.hill_climbing import hill_climbing, random_restart

class TestQueens(unittest.TestCase):
    def test_conflicts_cases(self):
        self.assertEqual(conflicts([3, 6, 2, 7, 1, 4, 0, 5]), 0)
        self.assertEqual(conflicts([0] * 8), 28)
        self.assertEqual(conflicts(list(range(8))), 28)

    def test_moves_generation(self):
        board = [0] * 8
        generated_moves = list(moves(board))
        self.assertEqual(len(generated_moves), 56)
        for col, row in generated_moves:
            self.assertNotEqual(row, board[col])

    def test_goal_initial_state(self):
        goal_board = [3, 6, 2, 7, 1, 4, 0, 5]
        res = hill_climbing(goal_board)
        self.assertTrue(res.success)
        self.assertEqual(res.iterations, 0)
        self.assertEqual(res.final_conflicts, 0)

    def test_hill_climbing_h_never_increases(self):
        initial = [0, 0, 0, 0, 0, 0, 0, 0]
        res = hill_climbing(initial)
        history = res.history
        for i in range(1, len(history)):
            self.assertLessEqual(history[i], history[i-1])

    def test_random_restart_reproducibility(self):
        rng1 = Random(42)
        res1 = random_restart(rng1, max_restarts=10)
        rng2 = Random(42)
        res2 = random_restart(rng2, max_restarts=10)
        self.assertEqual(res1.success, res2.success)
        self.assertEqual(res1.final_conflicts, res2.final_conflicts)
        self.assertEqual(res1.iterations, res2.iterations)
        self.assertEqual(res1.restarts, res2.restarts)

if __name__ == "__main__":
    unittest.main()
