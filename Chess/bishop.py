from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List


class Bishop(ChessPiece):
    def __init__(self, player: Player):
        super().__init__(player)

    def __str__(self):
        return f'Bishop ({self.player.name})'

    def type(self):
        return 'Bishop'

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        # Check if the move is diagonal
        if abs(start_col - end_col) != abs(start_row - end_row):
            return False

        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1

        for i in range(1, abs(end_row - start_row)):
            if board[start_row + i * row_step][start_col + i * col_step] is not None:
                return False

        return True


if __name__ == '__main__':  # testing
    b = Bishop(Player.WHITE)
    c = Bishop(Player.WHITE)
    d = Bishop(Player.BLACK)
    print(b.is_valid_move(Move(2, 0, 0, 2), [[None, None, d], [None, None], [b, None, None]]))
