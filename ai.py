import random


class AI:
    def choose_column(self, board, me="O", opponent="X"):
        legal = [c for c in range(7) if board.grid[0][c] == "."]
        if not legal:
            return None

        # 1. Win if possible
        for c in legal:
            row = board.drop(c, me)
            if row is not None:
                if board.winner(me):
                    board.grid[row][c] = "."   # undo
                    return c
                board.grid[row][c] = "."       # undo

        # 2. Block opponent's immediate win
        for c in legal:
            row = board.drop(c, opponent)
            if row is not None:
                if board.winner(opponent):
                    board.grid[row][c] = "."   # undo
                    return c
                board.grid[row][c] = "."       # undo

        # 3. Random legal column
        return random.choice(legal)
