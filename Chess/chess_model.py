from enum import Enum
from player import Player
from move import Move
from chess_piece import ChessPiece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from move import Move
from typing import List, Tuple


class MoveTypes(Enum):
    StopCheck = 1
    MakeCheck = 2
    StopThreat = 3
    Advance = 4


class MoveValidity(Enum):
    Valid = 1
    Invalid = 2
    MovingIntoCheck = 3
    StayingInCheck = 4

    def __str__(self):
        if self.value == 2:
            return 'Invalid move.'

        if self.value == 3:
            return 'Invalid -- cannot move into check.'

        if self.value == 4:
            return 'Invalid -- must move out of check.'


class UndoException(Exception):
    pass


class ChessModel:
    def __init__(self):
        self.board = [[Rook(Player.BLACK), Knight(Player.BLACK), Bishop(Player.BLACK), Queen(Player.BLACK),
                       King(Player.BLACK), Bishop(Player.BLACK), Knight(Player.BLACK), Rook(Player.BLACK)],
                      [Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK),
                       Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK)],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE),
                       Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE)],
                      [Rook(Player.WHITE), Knight(Player.WHITE), Bishop(Player.WHITE), Queen(Player.WHITE),
                       King(Player.WHITE), Bishop(Player.WHITE), Knight(Player.WHITE), Rook(Player.WHITE)]]
        self.__player = Player.WHITE
        self.__nrows = 8
        self.__ncols = 8
        self.__message_code = None
        self.move_history = []

    @property
    def nrows(self):
        return self.__nrows

    @nrows.setter
    def nrows(self, new_nrows: int):
        if isinstance(new_nrows, int):
            self.__nrows = new_nrows

    @property
    def ncols(self):
        return self.__nrows

    @ncols.setter
    def ncols(self, new_ncols: int):
        if isinstance(new_ncols, int):
            self.__ncols = new_ncols

    @property
    def current_player(self):
        return self.__player

    @current_player.setter
    def current_player(self, new_current_player: Player):
        if isinstance(new_current_player, Player):
            self.__player = new_current_player

    @property
    def messageCode(self):
        return self.__message_code

    @messageCode.setter
    def messageCode(self, new_messageCode: MoveValidity):
        if isinstance(new_messageCode, MoveValidity):
            self.__message_code = new_messageCode

    def is_complete(self) -> bool:
        white_check = self.in_check(Player.WHITE)
        black_check = self.in_check(Player.BLACK)

        if white_check or black_check:
            # get all of checked players pieces
            player_checked = Player.WHITE if white_check else Player.BLACK
            pieces = []
            for row in range(8):
                for col in range(8):
                    if self.board[row][col] is not None and self.board[row][col].player == player_checked:
                        pieces.append([row, col])
            # for each piece, check all possible moves and if it can stop check, return false
            for piece in pieces:
                start_row = piece[0]
                start_col = piece[1]
                for row in range(8):
                    for col in range(8):
                        if [row, col] in pieces:
                            continue
                        if self.is_valid_move(Move(start_row, start_col, row, col)):
                            return False
            return True
        return False

    def is_valid_move(self, move: Move):
        piece = self.piece_at(move.from_row, move.from_col)
        # use individual piece is_valid_move()
        if not piece.is_valid_move(move, self.board):
            self.messageCode = MoveValidity.Invalid
            return False
        # check if moving into check
        in_check_before = self.in_check(piece.player)
        self.move(move)
        if self.in_check(piece.player):
            self.undo()
            if in_check_before:
                self.messageCode = MoveValidity.StayingInCheck
                return False
            else:
                self.messageCode = MoveValidity.MovingIntoCheck
                return False
        self.undo()
        self.messageCode = MoveValidity.Valid
        return True
        # set __message_code correctly

    def move(self, move: Move):
        # Store the state of the board before the move
        old_board = [row.copy() for row in self.board]

        # Carry out the move
        self.board[move.to_row][move.to_col] = self.board[move.from_row][move.from_col]
        self.board[move.from_row][move.from_col] = None

        # pawn promotion
        piece = self.board[move.to_row][move.to_col]
        if piece.type() == 'Pawn':
            if (piece.player == Player.WHITE and move.to_row == 0) or (piece.player == Player.BLACK and move.to_row == 7):
                self.set_piece(move.to_row, move.to_col, Queen(piece.player))
        self.set_next_player()

        # Store the move and the old state of the board in move_history
        self.move_history.append(old_board)

    def in_check(self, p: Player):
        # get the position of player p's king
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if isinstance(piece, ChessPiece):
                    if piece.type() == 'King' and piece.player == p:
                        king_pos = (i, j)
                        break

        # for each of the opponents pieces, if said piece could take the king, return True
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if isinstance(piece, ChessPiece):
                    if piece.player != p and piece.player is not None:
                        if piece.is_valid_move(Move(i, j, king_pos[0], king_pos[1]), self.board):
                            return True
        return False

    def piece_at(self, row: int, col: int):
        try:
            return self.board[row][col]
        except IndexError:
            return None
        # returns piece at row, col

    def set_next_player(self):
        self.__player = Player.WHITE if self.__player == Player.BLACK else Player.BLACK
        # sets next player

    def set_piece(self, row: int, col: int, piece: ChessPiece):
        if row < 0 or row >= 8:
            raise ValueError
        elif col < 0 or col >= 8:
            raise ValueError
        elif not isinstance(piece, ChessPiece):
            raise TypeError
        else:
            self.board[row][col] = piece
        # puts piece at row, col

    def undo(self):
        # Undoes the most recent not undone move
        if len(self.move_history) == 0:
            raise UndoException

        # Pop the last move and the old state of the board from move_history
        old_board = self.move_history.pop()

        # Restore the board to its old state
        self.board = old_board
        self.set_next_player()

    def ai(self) -> bool:
        # get out of check
        if self.in_check(self.current_player):
            # move out of check
            self.move(self.possible_moves(MoveTypes.StopCheck, self.current_player))
        elif self.possible_moves(MoveTypes.MakeCheck, self.current_player):
            # check king with most expensive piece
            self.move(self.possible_moves(MoveTypes.MakeCheck, self.current_player))
        elif self.possible_moves(MoveTypes.StopThreat, self.current_player):
            # move most expensive piece under threat
            self.move(self.possible_moves(MoveTypes.StopThreat, self.current_player))
        else:
            # move forward
            self.move(self.possible_moves(MoveTypes.Advance, self.current_player))

    def find_piece(self, comp: ChessPiece) -> List[Tuple[int, int]]:
        """
        Finds all pieces that have the same color and class as an inputted ChessPiece.
        :param comp: ChessPiece an example of the specific piece you are looking for with the player set correctly.
        :return: A list of tuples with the row and col of the pieces that have the same color and class as comp.
        """
        r = []
        for i in range(8):
            for j in range(8):
                temp = self.piece_at(i, j)
                if isinstance(temp, ChessPiece):
                    if str(temp) == str(comp):
                        r.append((i, j))
        return r

    # get all poss_moves for type, then order them and return
    def possible_moves(self, type_move: MoveTypes, player: Player):
        """
        Returns the median of all possible moves of a certain MoveType that player can make.
        :param type_move: MoveTypes The type of move you are looking for. could be StopCheck, MakeCheck, StopThreat,
         or Advance.
        :param player: Player The player who is making the move.
        :return: Move The median of all moves that the lowest ranking piece can make.
        """
        piece_order = [King(player), Queen(player), Rook(player), Bishop(player), Knight(player), Pawn(player)]
        poss_moves = []
        for piece_type in piece_order[::-1]:
            for piece in self.find_piece(piece_type):
                for row in range(8):
                    for col in range(8):
                        temp_move = Move(piece[0], piece[1], row, col)
                        if not self.is_valid_move(temp_move):
                            continue
                        # Find checks to make
                        if type_move == MoveTypes.MakeCheck:
                            self.move(temp_move)
                            if self.in_check(Player.BLACK if player == Player.WHITE else player):
                                poss_moves = [temp_move] + poss_moves
                            self.undo()

                        # Stop pieces from being taken
                        elif type_move == MoveTypes.StopThreat:
                            if self.piece_at(row, col) is None:
                                continue
                            elif self.is_valid_move(Move(row, col, piece[0], piece[1])):
                                for new_row in range(8):
                                    for new_col in range(8):
                                        new_move = Move(piece[0], piece[1], new_row, new_col)
                                        if self.is_valid_move(new_move):
                                            poss_moves = [new_move] + poss_moves
                        # if in check or advancing, append all moves
                        else:
                            poss_moves.append(temp_move)
            if len(poss_moves) > 0:
                return poss_moves[len(poss_moves) // 2]
