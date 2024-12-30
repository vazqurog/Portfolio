from player import Player
from abc import ABC, abstractmethod
from enum import Enum
from move import Move
from typing import List
from chess_piece import ChessPiece


class Pawn(ChessPiece):
    def __init__(self, player: Player):
        super().__init__(player)

    def __str__(self):
        return f'Pawn ({self.player.name})'
    
    def type(self):
        return f"Pawn"

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        # Pawns can only move forward one square, but they can capture diagonally.
        direction = -1 if self.player == Player.WHITE else 1
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        # Check for standard move
        if start_col == end_col:
            if board[end_row][end_col] is None and end_row == start_row + direction:
                return True
        
        # Check for 2 square initial move
        if (self.player == Player.WHITE and start_row == 6) or (self.player == Player.BLACK and start_row == 1):
            if start_col == end_col and end_row == start_row + (2 * direction):
                if board[start_row + direction][start_col] is None and board[end_row][end_col] is None:
                    return True

        # Check for capture
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if board[end_row][end_col] is not None and board[end_row][end_col].player != self.player:
                return True

        return False


if __name__ == '__main__':  # testing
    b = Pawn(Player.WHITE)
    c = Pawn(Player.WHITE)
    d = Pawn(Player.BLACK)
    print(d.is_valid_move(Move(6, 0, 4, 0), [
        [None, None, None],
        [b, None, None],
        [None, None, None],
        [None, None, None],
        [None, None, None],
        [None, None, None],
        [d, None, None],
        [None, None, None]
    ]))
