from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List


class Rook(ChessPiece):
    def __init__(self, player: Player):
        super().__init__(player)

    def __str__(self):
        return f"Rook ({self.player.name})"

    def type(self):
        return "Rook"
  
    def is_valid_move(self, move: Move, board: List[List[ChessPiece]]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        # Check to not allow diagonal movement
        if start_col != end_col and start_row != end_row:
            return False

        # Check for standard move
        if start_row == end_row:
            for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if board[end_row][col] is not None:
                    return False

        if start_col == end_col:
            for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if board[row][end_col] is not None:
                    return False

        # capture check
        if board[end_row][end_col] is None or board[end_row][end_col].player != self.player:
            return True
            
        return False


if __name__ == '__main__':  # testing
    b = Rook(Player.WHITE)
    d = Rook(Player.BLACK)
    print(d.is_valid_move(Move(0, 0, 1, 0), [
        [d, None, None],
        [None, None, None],
        [None, None, None],
        [None, None, None],
        [None, None, None],
        [None, None, None],
        [None, None, None],
        [b, None, None]
    ]))
