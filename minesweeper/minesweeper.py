import tkinter as tk
import random

ROWS = 10
COLS = 10
MINES = 12
BTN_SIZE = 2


class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.button = None


class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper (Tkinter)")
        
        self.board = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]
        self.place_mines()
        self.count_neighbors()
        self.create_buttons()

    def place_mines(self):
        positions = set()
        while len(positions) < MINES:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            positions.add((r, c))

        for r, c in positions:
            self.board[r][c].is_mine = True

    def count_neighbors(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c].is_mine:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS:
                            if self.board[nr][nc].is_mine:
                                count += 1
                self.board[r][c].neighbor_mines = count

    def create_buttons(self):
        for r in range(ROWS):
            for c in range(COLS):
                btn = tk.Button(self.root, width=BTN_SIZE, height=1, 
                                command=lambda rr=r, cc=c: self.reveal(rr, cc))
                btn.bind("<Button-3>", lambda e, rr=r, cc=c: self.flag(rr, cc))
                btn.grid(row=r, column=c)
                self.board[r][c].button = btn

    def reveal(self, r, c):
        cell = self.board[r][c]
        if cell.is_flagged or cell.is_revealed:
            return
        
        cell.is_revealed = True
        
        if cell.is_mine:
            cell.button.config(text="💣", bg="red")
            self.game_over(False)
            return

        cell.button.config(text=str(cell.neighbor_mines) if cell.neighbor_mines > 0 else "",
                           relief=tk.SUNKEN, bg="lightgray")

        # auto-reveal empty neighbors
        if cell.neighbor_mines == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if not self.board[nr][nc].is_revealed:
                            self.reveal(nr, nc)

        self.check_win()

    def flag(self, r, c):
        cell = self.board[r][c]
        if cell.is_revealed:
            return
        
        if not cell.is_flagged:
            cell.button.config(text="🚩", fg="red")
            cell.is_flagged = True
        else:
            cell.button.config(text="")
            cell.is_flagged = False

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.game_over(True)

    def game_over(self, win):
        # Reveal all mines
        for row in self.board:
            for cell in row:
                if cell.is_mine:
                    cell.button.config(text="💣", bg="gray")
        
        msg = "🎉 You Win!" if win else "💥 You hit a mine!"
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        tk.Label(popup, text=msg, font=("Arial", 14)).pack(pady=10)
        tk.Button(popup, text="Close", command=self.root.quit).pack(pady=5)


# --- RUN GAME ---
root = tk.Tk()
game = Minesweeper(root)
root.mainloop()
