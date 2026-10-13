"""Módulo para o problema das 8 Rainhas."""
from collections.abc import Iterator
from random import Random
from typing import List, Tuple

Board = List[int]
Move = Tuple[int, int]
N = 8

def initial_board(rng: Random) -> Board:
    return [rng.randrange(N) for _ in range(N)]

def conflicts(board: list[int]) -> int:
    c = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                c += 1
    return c

def moves(board: list[int]) -> Iterator[tuple[int, int]]:
    for col in range(len(board)):
        current_row = board[col]
        for row in range(8):
            if row != current_row:
                yield (col, row)

def apply_move(board: Board, move: Move) -> Board:
    col, row = move
    if not 0 <= col < N or not 0 <= row < N:
        raise ValueError("Movimento fora do tabuleiro.")
    new_board = board.copy()
    new_board[col] = row
    return new_board

def render(board: Board) -> str:
    rows = []
    for r in range(N):
        rows.append(" ".join("Q" if board[c] == r else "." for c in range(N)))
    return "\n".join(rows)
