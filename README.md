# AI Tic-Tac-Toe — CF321 Search Algorithms

A Python desktop Tic-Tac-Toe game where a human (`X`) plays against an AI (`O`).

## Run

Install Python 3 with Tkinter support. No third-party packages required.

```bash
python main.py
```

## Problem formulation

- **State:** Nine board cells, each `X`, `O`, or blank, plus the player whose turn is next.
- **Initial state:** Empty board; human (`X`) moves first.
- **Actions:** Place the current player's mark in any empty cell.
- **Transition:** Mark that cell, then switch players.
- **Terminal/goal:** Three matching symbols in a row/column/diagonal, or a full board (draw).
- **Cost:** Each move has unit cost; the game has no weighted path costs.
- **Utility:** AI win = +1; draw = 0; human win = -1.

## Algorithm

`bfs_best_move` explores the reachable state graph **breadth-first** with a `deque` queue and a `seen` set. It records all successor states and the number of explored unique states. Because BFS alone finds shallow paths rather than optimal *adversarial* play, a separate backward dynamic-programming (minimax-style) evaluation assigns each terminal state a utility and propagates scores to parent states. AI maximizes; human minimizes. Equal-score moves are resolved by a deterministic center/corner/edge preference.

This distinction matters in the discussion: **BFS performs the search; backward evaluation chooses the move.**

## Live demonstration

1. Start a new game; click any empty square.
2. Observe the AI move, nodes explored, and evaluation.
3. Try playing in the center or corner first; compare explored node counts.
4. Explain `queue.popleft()`, the `seen` set, successor generation, terminal tests, and reverse evaluation.
5. Change `preference` in `bfs_best_move` to alter tie-breaking, then explain the result.

## Team discussion preparation

- Student 1: state representation, goal test, and game rules.
- Student 2: BFS queue, visited set, and graph expansion.
- Student 3: backward evaluation, choice of move, and trace.
- Student 4: Tkinter interface, testing, README, and GitHub.

All team members should be able to trace one example and make a small live code change.

## GitHub

Create a public or private repository, upload `main.py` and `README.md`, and demonstrate how to run the game.
