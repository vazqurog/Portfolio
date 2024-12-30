from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List


class Knight(ChessPiece):
    def __init__(self, player: Player):
        super().__init__(player)

    def __str__(self):
        return f'Knight ({self.player.name})'

    def type(self):
        return 'Knight'

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        if not super().is_valid_move(move, board):
            return False

        # confirms the L-shape movement
        deltaY = abs(move.to_row - move.from_row)
        deltaX = abs(move.to_col - move.from_col)
        if sorted([deltaX, deltaY]) == [1, 2]:
            return True
        return False


if __name__ == '__main__':  # testing
    b = Knight(Player.WHITE)
    c = Knight(Player.WHITE)
    d = Knight(Player.BLACK)
    print(b.is_valid_move(Move(2, 0, 0, 1), [[None, c, d], [None, None], [b, None, None]]))
