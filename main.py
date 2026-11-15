"""AI Tic-Tac-Toe: BFS state exploration with backward game-state evaluation."""
from collections import deque
import tkinter as tk
from tkinter import ttk

HUMAN, AI, EMPTY = 'X', 'O', ' '
LINES = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

def winner(board):
    for a,b,c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None

def terminal(board):
    return winner(board) is not None or EMPTY not in board

def moves(board, player):
    for i, cell in enumerate(board):
        if cell == EMPTY:
            next_board = list(board)
            next_board[i] = player
            yield i, tuple(next_board)

def bfs_best_move(board):
    """Build reachable game graph in BFS order; evaluate from leaves backward.

    States are (board, player_to_move). BFS does the exploration, while
    backward minimax-style scoring handles the adversarial opponent.
    """
    start = (tuple(board), AI)
    queue = deque([start])
    seen = {start}
    order = []
    children = {}
    while queue:
        state = queue.popleft()
        order.append(state)
        cells, player = state
        next_states = []
        if not terminal(cells):
            opponent = HUMAN if player == AI else AI
            for index, next_cells in moves(cells, player):
                child = (next_cells, opponent)
                next_states.append((index, child))
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        children[state] = next_states

    values = {}
    for state in reversed(order):
        cells, player = state
        if terminal(cells):
            victor = winner(cells)
            values[state] = 1 if victor == AI else (-1 if victor == HUMAN else 0)
        else:
            scores = [values[child] for _, child in children[state]]
            values[state] = max(scores) if player == AI else min(scores)

    # Center, corners, edges as deterministic tie-breaking preferences.
    preference = [4, 0, 2, 6, 8, 1, 3, 5, 7]
    choices = children[start]
    best_value = max(values[child] for _, child in choices)
    best_index = min((i for i, child in choices if values[child] == best_value),
                     key=preference.index)
    return best_index, len(order), best_value, [sum(1 for s in order if s[0].count(EMPTY) == n)
                                                     for n in range(board.count(EMPTY), -1, -1)]

class Game:
    def __init__(self, root):
        self.root = root
        root.title('AI Tic-Tac-Toe | BFS Search')
        root.geometry('680x710')
        root.configure(bg='#0c1224')
        self.board = [EMPTY] * 9
        self.score = {'human': 0, 'ai': 0, 'draw': 0}
        self.heading = tk.Label(root, text='AI TIC-TAC-TOE', font=('Segoe UI', 25, 'bold'),
                                fg='#eaf0ff', bg='#0c1224')
        self.heading.pack(pady=(22, 4))
        tk.Label(root, text='Breadth-First Search • Game State Exploration',
                 font=('Segoe UI', 11), fg='#94a3b8', bg='#0c1224').pack()
        self.status = tk.StringVar(value='Your turn — choose a square (X)')
        tk.Label(root, textvariable=self.status, font=('Segoe UI', 13, 'bold'),
                 fg='#b9a6ff', bg='#0c1224').pack(pady=16)
        frame = tk.Frame(root, bg='#0c1224')
        frame.pack()
        self.buttons = []
        for i in range(9):
            btn = tk.Button(frame, text=' ', font=('Segoe UI', 34, 'bold'), width=4, height=2,
                            bg='#192541', fg='#5bd5ff', activebackground='#29365b',
                            relief='flat', command=lambda index=i: self.human_move(index))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
        self.info = tk.StringVar(value='Nodes explored: 0 | Chosen move: — | Evaluation: —')
        tk.Label(root, textvariable=self.info, font=('Consolas', 10), fg='#cbd5e1',
                 bg='#0c1224', wraplength=640).pack(pady=(18, 6))
        self.detail = tk.StringVar(value='BFS explores reachable states level by level.')
        tk.Label(root, textvariable=self.detail, font=('Segoe UI', 10), fg='#94a3b8',
                 bg='#0c1224', wraplength=640).pack()
        self.scores = tk.StringVar()
        tk.Label(root, textvariable=self.scores, font=('Segoe UI', 12), fg='#eaf0ff',
                 bg='#0c1224').pack(pady=12)
        tk.Button(root, text='New Game', command=self.reset, font=('Segoe UI', 12, 'bold'),
                  bg='#6856d9', fg='white', relief='flat', padx=30, pady=9).pack()
        self.update_scores()

    def update_scores(self):
        self.scores.set(f"You: {self.score['human']}     AI: {self.score['ai']}     Draws: {self.score['draw']}")

    def human_move(self, index):
        if self.board[index] != EMPTY or terminal(self.board):
            return
        self.place(index, HUMAN)
        if self.finish():
            return
        ai_index, explored, value, levels = bfs_best_move(self.board)
        self.place(ai_index, AI)
        label = {1: 'AI can force a win', 0: 'Draw with best play', -1: 'Human can force a win'}[value]
        self.info.set(f'Nodes explored: {explored} | Chosen move: {ai_index+1} | Evaluation: {value:+d}')
        self.detail.set(f'BFS nodes per depth: {levels} | {label}')
        if not self.finish():
            self.status.set('Your turn — choose a square (X)')

    def place(self, index, player):
        self.board[index] = player
        self.buttons[index].configure(text=player, fg='#5bd5ff' if player == HUMAN else '#bc9cff')

    def finish(self):
        victor = winner(self.board)
        if victor == HUMAN:
            self.score['human'] += 1
            self.status.set('You win!')
        elif victor == AI:
            self.score['ai'] += 1
            self.status.set('AI wins!')
        elif EMPTY not in self.board:
            self.score['draw'] += 1
            self.status.set('Draw!')
        else:
            return False
        self.update_scores()
        return True

    def reset(self):
        self.board = [EMPTY] * 9
        for button in self.buttons:
            button.configure(text=' ')
        self.status.set('Your turn — choose a square (X)')
        self.info.set('Nodes explored: 0 | Chosen move: — | Evaluation: —')
        self.detail.set('BFS explores reachable states level by level.')

if __name__ == '__main__':
    app = tk.Tk()
    Game(app)
    app.mainloop()
