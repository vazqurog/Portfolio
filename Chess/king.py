from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List


class King(ChessPiece):
    def __init__(self, player: Player):
        super().__init__(player)

    def __str__(self):
        return f'King ({self.player.name})'

    def type(self):
        return 'King'

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        # Check if the move is one square in any direction
        if max(abs(start_row - end_row), abs(start_col - end_col)) != 1:
            return False

        return True
