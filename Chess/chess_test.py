import unittest
from chess_model import ChessModel, MoveTypes
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from player import Player
from move import Move


class TestPawn(unittest.TestCase):
    # set a board for easy testing
    pawn = Pawn(Player.WHITE)
    white = Pawn(Player.WHITE)
    black = Pawn(Player.BLACK)
    b = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, black, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, white, None, None, None],
        [None, None, None, pawn, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]

    # other methods
    def test_str(self):
        self.assertEqual(str(self.pawn), 'Pawn (WHITE)', 'str not set correctly')

    def test_type(self):
        self.assertEqual(self.pawn.type(), 'Pawn', 'str not set correctly')

    # actual moves
    def test_parent(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 6, 3), self.b),
                         False, 'Super not set correctly')

    def test_up_1(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 5, 3), self.b),
                         True, 'move up 1 not set correctly')

    def test_up_2(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 4, 3), self.b),
                         True, 'move up 2 not set correctly')

    def test_ul_none(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 5, 2), self.b),
                         False, 'move ul_none not set correctly')

    def test_ul_black(self):
        self.b[5][2] = self.black
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 5, 2), self.b),
                         True, 'move ul_black not set correctly')
        self.b[5][2] = None

    def test_ur_white(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 5, 4), self.b),
                         False, 'move ur_white not set correctly')

    def test_back(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 7, 3), self.b),
                         False, 'move back not set correctly')

    def test_up_3(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 3, 3), self.b),
                         False, 'move up_3 not set correctly')

    def test_ul_2(self):
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 4, 1), self.b),
                         False, 'move ul_2 not set correctly')

    def test_black(self):
        self.assertEqual(self.black.is_valid_move(Move(1, 3, 2, 3), self.b),
                         True, 'move black not set correctly')

    def test_block(self):
        self.b[5][3] = self.black
        self.assertEqual(self.pawn.is_valid_move(Move(6, 3, 5, 3), self.b),
                         False, 'move block not set correctly')
        self.b[5][3] = None


class TestRook(unittest.TestCase):
    rook = Rook(Player.WHITE)
    white = Rook(Player.WHITE)
    black = Rook(Player.BLACK)
    b = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, black, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, white, None, None, None],
        [None, None, None, None, None, None, None, None],
        [rook, None, None, None, None, white, None, None],
    ]

    # other methods

    def test_str(self):
        self.assertEqual(str(self.rook), 'Rook (WHITE)', 'str not set correctly')

    def test_type(self):
        self.assertEqual(str(self.rook.type()), 'Rook', 'str not set correctly')

    # actual moves
    def test_parent(self):
        self.assertEqual(self.rook.is_valid_move(Move(7, 0, 7, 0), self.b),
                         False, 'super not set correctly')

    def test_vertical_movement(self):
        self.assertEqual(self.rook.is_valid_move(Move(7, 0, 2, 0), self.b),
                         True, 'vertical movement not set up correctly')

    def test_horizontal_movement(self):
        self.assertEqual(self.rook.is_valid_move(Move(7, 0, 7, 4), self.b),
                         True, 'horizontal movement not set up correctly')

    def test_black_rook_movement(self):
        v_move = Move(1, 3, 4, 3)
        self.assertEqual(self.black.is_valid_move(v_move, self.b),
                         True, 'black vertical movement not set up correctly')

        h_move = Move(1, 3, 1, 5)
        self.assertEqual(self.black.is_valid_move(h_move, self.b),
                         True, 'black horizontal movement not set up correctly')

    def test_move_block(self):
        move = Move(7, 0, 7, 5)
        self.assertEqual(self.rook.is_valid_move(move, self.b),
                         False, 'Rook can capture pieces of the same color - FIX IT.')


class TestKnight(unittest.TestCase):
    knight = Knight(Player.WHITE)
    white = Knight(Player.WHITE)
    black = Knight(Player.BLACK)
    b = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, black, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, white, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, knight, None, None, None, None, None, None],
    ]

    # other methods

    def test_str(self):
        self.assertEqual(str(self.knight), 'Knight (WHITE)', 'str not set correctly')

    def test_type(self):
        self.assertEqual(str(self.knight.type()), 'Knight', 'str not set correctly')

    # actual moves

    def test_parent(self):
        self.assertEqual(self.knight.is_valid_move(Move(7, 1, 7, 1), self.b),
                         False, 'super not set correctly')

    def test_knight_movement(self):
        move = Move(7, 1, 5, 2)
        self.assertEqual(self.knight.is_valid_move(move, self.b),
                         True, 'White Knight movement not set up correctly')

    def test_wrong_knight_movement(self):
        move = Move(7, 1, 4, 3)
        self.assertEqual(self.knight.is_valid_move(move, self.b),
                         False, 'Knight movement not set up correctly')

    def test_black_knight_movement(self):
        move = Move(2, 2, 4, 3)
        self.assertEqual(self.black.is_valid_move(move, self.b),
                         True, 'Black Knight movement not set up correctly')


class TestBishop(unittest.TestCase):
    bishop = Bishop(Player.WHITE)
    white = Bishop(Player.WHITE)
    black = Bishop(Player.BLACK)
    b = [
        [None, None, black, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, white, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, bishop, None, None, None, None, None],
    ]

    # other methods

    def test_str(self):
        self.assertEqual(str(self.bishop), 'Bishop (WHITE)', 'str not set correctly')

    def test_type(self):
        self.assertEqual(str(self.bishop.type()), 'Bishop', 'type not set correctly')

    # actual moves

    def test_parent(self):
        self.assertEqual(self.bishop.is_valid_move(Move(7, 2, 7, 2), self.b),
                          False, 'super not set correctly')

    def test_bishop_movement(self):
        # Diagonal Movement
        move = Move(7, 2, 6, 3)
        self.assertEqual(self.bishop.is_valid_move(move, self.b),
                         True, 'Bishop movement not set correctly')

        # Horizontal Movement (SHOULD RETURN FALSE)
        h_move = Move(7, 2, 7, 0)
        self.assertEqual(self.bishop.is_valid_move(h_move, self.b),
                         False, 'Bishop movement not set correctly')

        # Vertical Movement (SHOULD RETURN FALSE)
        v_move = Move(7, 2, 1, 2)
        self.assertEqual(self.bishop.is_valid_move(v_move, self.b),
                         False, 'Bishop movement not set correctly')

    def test_black_bishop_movement(self):
        move = Move(0, 2, 2, 4)
        self.assertEqual(self.black.is_valid_move(move, self.b),
                         True, 'Black Bishop movement not set correctly')

    def test_move_block(self):
        move = Move(7, 2, 5, 4)
        self.assertEqual(self.bishop.is_valid_move(move, self.b),
                         False, 'Bishop can capture same color piece - FIX THAT.')


class TestQueen(unittest.TestCase):
    queen = Queen(Player.WHITE)
    white = Queen(Player.WHITE)
    black = Queen(Player.BLACK)
    b = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, black, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, white, None, None, None, None, None],
        [None, None, None, queen, None, None, None, None],
    ]

    # other methods

    def test_str(self):
        self.assertEqual(str(self.queen), 'Queen (WHITE)', 'str not set correctly')

    def test_type(self):
        self.assertEqual(str(self.queen.type()), 'Queen', 'type not set correctly')

    # actual moves

    def test_parent(self):
        self.assertEqual(self.queen.is_valid_move(Move(7, 3, 7, 3), self.b),
                         False, 'super not set correctly')

    def test_queen_movement(self):
        # Vertical Movement
        v_move = Move(7, 3, 1, 3)
        self.assertEqual(self.queen.is_valid_move(v_move, self.b),
                         True, 'Queen vertical movement not set correctly')

        # Horizontal Movement
        h_move = Move(7, 3, 7, 1)
        self.assertEqual(self.queen.is_valid_move(h_move, self.b),
                         True, 'Queen horizontal movement not set correctly')

        # Diagonal Movement
        d_move = Move(7, 3, 5, 5)
        self.assertEqual(self.queen.is_valid_move(d_move, self.b),
                         True, 'Queen diagonal movement not set correctly')

    def test_queen_impossible_move(self):
        move = Move(7, 3, 5, 2)
        self.assertEqual(self.queen.is_valid_move(move, self.b),
                         False, 'queen movement not set correctly (it moves like a Knight)')

    def test_black_queen_movement(self):
        # Vertical Movement
        v_move = Move(2, 2, 1, 2)
        self.assertEqual(self.black.is_valid_move(v_move, self.b),
                         True, 'Black Queen vertical movement not set correctly')

        # Horizontal Movement
        h_move = Move(2, 2, 2, 1)
        self.assertEqual(self.black.is_valid_move(h_move, self.b),
                         True, 'Black Queen horizontal movement not set correctly')

        # Diagonal Movement
        d_move = Move(2, 2, 5, 5)
        self.assertEqual(self.black.is_valid_move(d_move, self.b),
                         True, 'Black Queen diagonal movement not set correctly')

    def test_move_block(self):
        move = Move(7, 3, 6, 2)
        self.assertEqual(self.queen.is_valid_move(move, self.b),
                         False, 'queen movement not set correctly')


class TestKing(unittest.TestCase):
    king = King(Player.WHITE)
    white = King(Player.WHITE)
    black = King(Player.BLACK)
    b = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, black, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, white, None, None, None, None, None],
        [None, None, None, king, None, None, None, None],
    ]

    # other methods

    def test_str(self):
        self.assertEqual(str(self.king), 'King (WHITE)', 'str not set correctly')

    def test_type(self):
        self.assertEqual(str(self.king.type()), 'King', 'type not set correctly')

    # actual moves

    def test_parent(self):
        self.assertEqual(self.king.is_valid_move(Move(7, 3, 7, 3), self.b),
                         False, 'super not set correctly')

    def test_king_movement(self):
        # Vertical Movement
        v_move = Move(7, 3, 6, 3)
        self.assertEqual(self.king.is_valid_move(v_move, self.b),
                         True, 'King movement not set correctly - Vertical')

        # Horizontal Movement
        h_move = Move(7, 3, 7, 4)
        self.assertEqual(self.king.is_valid_move(h_move, self.b),
                         True, 'King movement not set correctly - Horizontal')

        # Diagonal Movement
        d_move = Move(7, 3, 6, 4)
        self.assertEqual(self.king.is_valid_move(d_move, self.b),
                         True, 'King movement not set correctly - Diagonal')

    def test_black_king_movement(self):
        # Vertical Movement
        v_move = Move(2, 2, 2, 1)
        self.assertEqual(self.black.is_valid_move(v_move, self.b),
                         True, 'Black King movement not set correctly - Vertical')

        # Horizontal Movement
        h_move = Move(2, 2, 2, 3)
        self.assertEqual(self.black.is_valid_move(h_move, self.b),
                         True, 'Black King movement not set correctly - Horizontal')

        # Diagonal Movement
        d_move = Move(2, 2, 3, 3)
        self.assertEqual(self.black.is_valid_move(d_move, self.b),
                         True, 'Black King movement not set correctly - Diagonal')

    def test_king_more_than_one_space_move(self):
        # Vertical Movement
        v_move = Move(7, 3, 5, 3)
        self.assertEqual(self.king.is_valid_move(v_move, self.b),
                         False, 'King movement not set correctly - Vertical')

        # Horizontal Movement
        h_move = Move(7, 3, 7, 5)
        self.assertEqual(self.king.is_valid_move(h_move, self.b),
                         False, 'King movement not set correctly - Horizontal')

        # Diagonal Movement
        d_move = Move(7, 3, 5, 5)
        self.assertEqual(self.king.is_valid_move(d_move, self.b),
                         False, 'King movement not set correctly - Diagonal')

    def test_move_block(self):
        move = Move(7, 3, 6, 2)
        self.assertEqual(self.king.is_valid_move(move, self.b),
                         False, 'King can capture pieces of the same color - FIX IT.')


class TestUndo(unittest.TestCase):
    # Setting up the Game Board
    def setUp(self):
        self.game = ChessModel()

    def test_undo(self):
        # Create a Pawn at (1, 1)
        pawn = Pawn(Player.BLACK)
        self.game.set_piece(1, 1, pawn)

        # Make a Move
        move = Move(1, 1, 2, 1)
        self.game.move(move)

        # Undo the move
        self.game.undo()

        # Check that the pawn is back at its original position
        self.assertEqual(self.game.piece_at(1, 1), pawn)
        self.assertEqual(self.game.piece_at(2, 1), None)


class TestInCheck(unittest.TestCase):
    def setUp(self):
        self.game = ChessModel()
        self.queen = Queen(Player.WHITE)
        self.king = King(Player.BLACK)
        self.game.set_piece(4, 4, self.queen)
        self.game.set_piece(2, 2, self.king)

    def test_in_check(self):
        # The black king should be in check from the white queen
        self.assertTrue(self.game.in_check(Player.BLACK))


class TestIsValidMove(unittest.TestCase):
    # Setting up the game board
    def setUp(self):
        self.game = ChessModel()

    def test_is_valid_move(self):
        # Create a Pawn at position (1,1)
        pawn = Pawn(Player.BLACK)
        self.game.set_piece(1, 1, pawn)

        # Testing a Valid Move
        move = Move(1, 1, 2, 1)
        self.assertTrue(self.game.is_valid_move(move))

        # Testing an Invalid Move
        move = Move(1, 1, 4, 1)
        self.assertFalse(self.game.is_valid_move(move))


class TestIsComplete(unittest.TestCase):
    def setUp(self):
        self.game = ChessModel()

    def test_is_complete_fail(self):
        # The game should be incomplete as no moves have been made.
        self.assertFalse(self.game.is_complete())

    def test_is_complete(self):
        self.w_king = King(Player.WHITE)
        self.w_rook = Rook(Player.WHITE)
        self.b_king = King(Player.BLACK)
        self.game.board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, self.w_king, None, self.b_king],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, self.w_rook],
        ]

        self.assertTrue(self.game.is_complete())


class TestMove(unittest.TestCase):
    def setUp(self):
        self.game = ChessModel()

    def test_move(self):
        # Set a Black Pawn at (1, 1)
        pawn = Pawn(Player.BLACK)
        self.game.set_piece(1, 1, pawn)

        # Make a move
        move = Move(1, 1, 2, 1)
        self.game.move(move)

        # Check that the pawn has moved to the new position
        self.assertEqual(self.game.piece_at(2, 1), pawn)
        self.assertIsNone(self.game.piece_at(1, 1))

# ChessModel.find_piece() (Brody)


class TestFind(unittest.TestCase):
    # set board
    def setUp(self):
        self.game = ChessModel()

    def test_find_king(self):
        self.assertEqual(self.game.find_piece(King(Player.WHITE)), [(7, 4)], "find_king not set correctly!")

    def test_find_rook(self):
        self.assertEqual(self.game.find_piece(Rook(Player.BLACK)), [(0, 0), (0, 7)], "find_rook not set correctly!")

    # looks for a piece that doesn't exist
    def test_find_nothing(self):
        self.game.board[7][4] = None
        self.assertEqual(self.game.find_piece(King(Player.WHITE)), [], "find_nothing not set correctly!")


# ChessModel.possible_moves() (Brody)
class TestPossibleMoves(unittest.TestCase):
    def setUp(self):
        self.game = ChessModel()

    def test_possible_moves(self):
        self.assertEqual(str(self.game.possible_moves(MoveTypes.Advance, self.game.current_player)),
                         'Move [from_row=6, from_col=4, to_row=4, to_col=4]', 'poss_moves not set correctly!')

    def test_no_moves(self):
        self.assertIsNone(self.game.possible_moves(MoveTypes.StopThreat, self.game.current_player),
                          'no_moves not set correctly!')
