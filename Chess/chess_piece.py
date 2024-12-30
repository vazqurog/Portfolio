from abc import ABC, abstractmethod
from player import Player
from move import Move
from typing import List


class ChessPiece(ABC):
    def __init__(self, player: Player):
        self.__player = player

    @property
    def player(self):
        return self.__player

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def type(self):
        pass

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        # Verifies indices associated with move are within bounds
        if not (0 <= move.from_row < len(board) and 0 <= move.from_col < len(board[0])
                and 0 <= move.to_row < len(board) and 0 <= move.to_col < len(board[0])):
            return False

        # Verifies starting and ending locations are different
        if move.from_row == move.to_row and move.from_col == move.to_col:
            return False

        # Verifies that selected piece is located at starting location in move
        if board[move.from_row][move.from_col] != self:
            return False

        # Verifies that ending location does not contain a piece belonging to the same color of the piece.
        if board[move.to_row][move.to_col] is None:
            return True
        if board[move.from_row][move.from_col] is not None and board[move.to_row][move.to_col].player == self.player:
            return False

        return True
