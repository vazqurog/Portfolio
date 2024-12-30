from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List


class Queen(ChessPiece):
    def __init__(self, player: Player):
        super().__init__(player)

    def __str__(self):
        return f'Queen ({self.player.name})'

    def type(self):
        return 'Queen'

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        # Check if the move is in a straight line (like a rook)
        if start_row == end_row or start_col == end_col:
            # Check if the path is clear
            if start_row == end_row:
                for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                    if board[start_row][col] is not None:
                        return False
            else:
                for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                    if board[row][start_col] is not None:
                        return False

        # Check if the move is diagonal (like a bishop)
        elif abs(start_col - end_col) == abs(start_row - end_row):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1

            for i in range(1, abs(end_row - start_row)):
                if board[start_row + i * row_step][start_col + i * col_step] is not None:
                    return False
        else:
            return False

        return True


if __name__ == '__main__':  # testing
    b = Queen(Player.WHITE)
    c = Queen(Player.WHITE)
    d = Queen(Player.BLACK)
    print(b.is_valid_move(Move(2, 0, 2, 2), [[None, None, d], [None, None], [b, None, None]]))
