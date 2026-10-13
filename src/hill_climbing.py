"""Algoritmos de Hill Climbing e Random Restart para as 8 Rainhas."""
from dataclasses import dataclass, field
from random import Random
from typing import List
from .eight_queens import Board, conflicts, initial_board, moves

@dataclass
class HillResult:
    success: bool
    initial: Board
    final: Board
    initial_conflicts: int
    final_conflicts: int
    iterations: int
    evaluated_states: int
    restarts: int = 0
    history: List[int] = field(default_factory=list)

def hill_climbing(initial: Board) -> HillResult:
    current = list(initial)
    current_h = conflicts(current)
    initial_h = current_h
    iterations = 0
    evaluated_states = 1
    history = [current_h]

    while True:
        best_neighbor = None
        best_h = current_h
        for col, row in moves(current):
            evaluated_states += 1
            neighbor = list(current)
            neighbor[col] = row
            h_neighbor = conflicts(neighbor)
            if h_neighbor < best_h:
                best_h = h_neighbor
                best_neighbor = neighbor

        if best_neighbor is None or best_h >= current_h:
            break

        current = best_neighbor
        current_h = best_h
        iterations += 1
        history.append(current_h)

    return HillResult(
        success=(current_h == 0),
        initial=initial,
        final=current,
        initial_conflicts=initial_h,
        final_conflicts=current_h,
        iterations=iterations,
        evaluated_states=evaluated_states,
        history=history,
    )

def random_restart(rng: Random, max_restarts: int = 50) -> HillResult:
    total_iterations = 0
    total_evaluated_states = 0
    restarts = 0
    last_initial = []
    last_res = None

    while restarts <= max_restarts:
        initial = initial_board(rng)
        if restarts == 0:
            last_initial = initial
        
        result = hill_climbing(initial)
        total_iterations += result.iterations
        total_evaluated_states += result.evaluated_states
        
        if result.success:
            return HillResult(
                success=True,
                initial=initial,
                final=result.final,
                initial_conflicts=result.initial_conflicts,
                final_conflicts=0,
                iterations=total_iterations,
                evaluated_states=total_evaluated_states,
                restarts=restarts,
                history=result.history,
            )
            
        last_res = result
        restarts += 1

    return HillResult(
        success=False,
        initial=last_res.initial,
        final=last_res.final,
        initial_conflicts=last_res.initial_conflicts,
        final_conflicts=last_res.final_conflicts,
        iterations=total_iterations,
        evaluated_states=total_evaluated_states,
        restarts=max_restarts,
        history=last_res.history,
    )
