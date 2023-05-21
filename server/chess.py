from copy import deepcopy
from random import randint

LETTERS = "abcdefgh"
NUMBERS = "12345678"
PIECES = {
    "p": ["", "\u2659", "\u265F"],
    "n": ["", "\u2658", "\u265E"],
    "b": ["", "\u2657", "\u265D"],
    "r": ["", "\u2656", "\u265C"],
    "q": ["", "\u2655", "\u265B"],
    "k": ["", "\u2654", "\u265A"],
}
WHITE = 1
BLACK = -1


class Square:
    def __init__(self, pos=0, piece=None):
        """
        Creates a square object that holds a position and piece
        :param pos: int
        :param piece: Piece
        """
        self.index = pos
        self.piece = piece

    @staticmethod
    def algebraic_to_index(an):
        """
        Converts from algebraic notation to an index
        :param an: str
        :return: int
        """
        c = LETTERS.index(an[0])
        r = NUMBERS[::-1].index(an[1])
        return 8 * r + c

    @staticmethod
    def index_to_algebraic(i):
        """
        Converts from an index to algebraic notation
        :param i: int
        :return: str
        """
        c, r = Square.index_to_coordinate(i)
        return LETTERS[c] + NUMBERS[::-1][r]

    @staticmethod
    def index_to_coordinate(i):
        """
        Converts from an index to a (col, row) coordinate
        :param i: int
        :return: (int, int)
        """
        return i % 8, i // 8

    @staticmethod
    def coordinate_to_index(square):
        """
        Converts from a (col, row) coordinate to an index
        :param square: (int, int)
        :return: int
        """
        c, r = square
        return c + r * 8

    def has_piece(self):
        """
        Checks if square holds a piece
        :return: bool
        """
        return self.piece is not None

    def has_ally_piece(self, colour):
        """
        Checks if square holds a piece of the same colour specified
        :param colour: int
        :return: bool
        """
        if not self.has_piece(): return False
        return self.piece.colour == colour

    def has_enemy_piece(self, colour):
        """
        Checks if square holds a piece of the opposite colour specified
        :param colour: int
        :return: bool
        """
        if not self.has_piece(): return False
        return self.piece.colour != colour

    def __str__(self):
        return Square.index_to_algebraic(self.index)

    def __eq__(self, s):
        if not isinstance(s, Square):
            raise TypeError("Comparing and instace of Square to a differnet object.")
        return s.index == self.index


class Piece:
    def __init__(self, printable):
        """
        Creates a piece from a char
        :param printable: str
        """
        self.colour = WHITE
        if printable.islower(): self.colour = BLACK
        self.type = printable.lower()

        self.printable = printable

    def __str__(self):
        # return self.printable
        return PIECES[self.type][self.colour]

    def is_attacking(self, board, cur_pos, target_pos):
        """
        Checks if a piece is attacking a square
        :param board: Board
        :param cur_pos: int
        :param target_pos: int
        :return: bool
        """
        if self.type == "p" and self.colour == WHITE:
            if cur_pos - target_pos == 7 or cur_pos - target_pos == 9:
                if board.board[target_pos].has_enemy_piece(self.colour):
                    return True
        if self.type == "p" and self.colour == BLACK:
            if cur_pos - target_pos == -7 or cur_pos - target_pos == -9:
                if board.board[target_pos].has_enemy_piece(self.colour):
                    return True
        if self.type == "n":
            t = Square.index_to_coordinate(target_pos)
            c = Square.index_to_coordinate(cur_pos)
            o = t[0] - c[0], t[1] - c[1]
            if o in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)] and not board.board[
                target_pos].has_ally_piece(self.colour):
                return True
        if self.type == "b":
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                col, row = Square.index_to_coordinate(cur_pos)
                while 0 <= row <= 7 and 0 <= col <= 7:
                    if not Square.coordinate_to_index((col, row)) == cur_pos:
                        if Square.coordinate_to_index((col, row)) == target_pos:
                            if not board.board[Square.coordinate_to_index((col, row))].has_ally_piece(self.colour):
                                return True
                        if board.board[Square.coordinate_to_index((col, row))].has_piece():
                            break
                    row += direction[0]
                    col += direction[1]
        if self.type == "r":
            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                col, row = Square.index_to_coordinate(cur_pos)
                while 0 <= row <= 7 and 0 <= col <= 7:
                    cur_checking = Square.coordinate_to_index((col, row))
                    if not cur_checking == cur_pos:
                        if cur_checking == target_pos:
                            if not board.board[cur_checking].has_ally_piece(self.colour):
                                return True
                        if board.board[cur_checking].has_piece():
                            break
                    row += direction[0]
                    col += direction[1]
        if self.type == "q":
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                col, row = Square.index_to_coordinate(cur_pos)
                while 0 <= row <= 7 and 0 <= col <= 7:
                    if not Square.coordinate_to_index((col, row)) == cur_pos:
                        if Square.coordinate_to_index((col, row)) == target_pos:
                            if not board.board[Square.coordinate_to_index((col, row))].has_ally_piece(self.colour):
                                return True
                        if board.board[Square.coordinate_to_index((col, row))].has_piece():
                            break
                    row += direction[0]
                    col += direction[1]
        if self.type == "k":
            t = Square.index_to_coordinate(target_pos)
            c = Square.index_to_coordinate(cur_pos)
            o = t[0] - c[0], t[1] - c[1]
            if o in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)] and not board.board[
                target_pos].has_ally_piece(self.colour):
                return True
            if self.colour == 1:
                if target_pos == 62 and board.castling[0]:
                    if not board.board[62].has_piece() and not board.board[61].has_piece():
                        return True
                if target_pos == 28 and board.castling[1]:
                    if not board.board[59].has_piece() and not board.board[58].has_piece() and not board.board[
                        57].has_piece():
                        return True
                if target_pos == 6 and board.castling[2]:
                    if not board.board[6].has_piece() and not board.board[5].has_piece():
                        return True
                if target_pos == 2 and board.castling[3]:
                    if not board.board[1].has_piece() and not board.board[2].has_piece() and not board.board[
                        3].has_piece():
                        return True
        # print(f"{self} cannot move to {Square.indexToAlgebraic(target_pos)}")
        return False

    def can_move(self, board, cur_pos, target_pos):
        """
        Checks if making a move is legal
        :param board: Board
        :param cur_pos: int
        :param target_pos: int
        :return: bool
        """
        if board.turn != self.colour:
            # c = ["", "White", "Black"][board.turn]
            # print(f"{self} cannot move because it is {c}s turn")
            return False
        if self.type == "p" and self.colour == WHITE:
            if cur_pos - target_pos == 8:
                if not board.board[target_pos].has_piece():
                    return True
            elif cur_pos - target_pos == 16 and cur_pos > 47:
                if not board.board[target_pos].has_piece() and not board.board[cur_pos - 8].has_piece():
                    return True
            elif cur_pos - target_pos == 7 or cur_pos - target_pos == 9:
                if board.board[target_pos].has_enemy_piece(self.colour):
                    return True
                elif board.en_passant.index == target_pos:
                    return True
        if self.type == "p" and self.colour == BLACK:
            if cur_pos - target_pos == -8:
                if not board.board[target_pos].has_piece():
                    return True
            elif cur_pos - target_pos == -16 and cur_pos < 16:
                if not board.board[target_pos].has_piece() and not board.board[cur_pos + 8].has_piece():
                    return True
            elif cur_pos - target_pos == -7 or cur_pos - target_pos == -9:
                if board.board[target_pos].has_enemy_piece(self.colour):
                    return True
                elif board.en_passant.index == target_pos:
                    return True
        return self.is_attacking(board, cur_pos, target_pos)


class Move:
    def __init__(self, start_pos, target_pos, promotion_piece="q"):
        """
        Creates an instance of a move holding a start and end pos
        :param start_pos: int
        :param target_pos: int
        :param promotion_piece: str
        """
        self.current_pos = start_pos
        self.target_pos = target_pos
        self.promotion_piece = promotion_piece

    def __str__(self):
        return f"{Square.index_to_algebraic(self.current_pos)} > {Square.index_to_algebraic(self.target_pos)}"

    def __eq__(self, move):
        if not isinstance(move, Move):
            raise TypeError("Comparing and instance of Move to a different object.")
        return move.current_pos == self.current_pos and move.target_pos == self.target_pos

    def is_valid(self, board):
        """
        Checks if move is legal
        :param board: Board
        :return: bool
        """
        # print(board.board[self.current_pos].piece)
        try:
            if not board.board[self.current_pos].has_piece:
                return False
            if not board.board[self.current_pos].piece.can_move(board, self.current_pos, self.target_pos):
                return False
        except AttributeError:
            print("Tried to move a piece that didn't exist")
            return False
        c = board.clone()
        c.make_move(self)
        if c.is_check(board.turn):
            del c
            return False
        del c
        return True


class Board:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        """
        Creates an instance of the game
        """
        self.board = [Square()] * 64  # empty board
        self.turn = WHITE  # 1: white, -1: black
        self.castling = [False] * 4
        self.en_passant = Square(-1)  # no en passant square
        self.fifty_move_timer = 0  # counts to 100 halfmoves
        self.moves = 0

        self.load_fen(fen)

    def load_fen(self, fen_to_load):
        """
        Loads a FEN notation onto the board
        :param fen_to_load: str
        :return: None
        """
        fen_string = fen_to_load.split(" ")
        # pieces
        pieces = []
        index = 0
        for char in fen_string[0]:
            if char.isnumeric():
                for _ in range(int(char)):
                    pieces.append(Square(index))
                    index += 1
            else:
                if not char == "/":
                    p = Piece(char)
                    pieces.append(Square(index, p))
                    index += 1
        self.board = pieces
        # turn
        turn = 1
        if fen_string[1] == "b": turn = -1
        self.turn = turn
        # castling
        self.castling = [False] * 4
        for char in fen_string[2]:
            if char == "K": self.castling[0] = True
            if char == "Q": self.castling[1] = True
            if char == "k": self.castling[2] = True
            if char == "q": self.castling[3] = True
        # en passant
        if fen_string[3] == "-":
            self.en_passant = Square(-1)
        else:
            self.en_passant = Square(Square.algebraic_to_index(fen_string[3]))
        # 50 move timer
        self.fifty_move_timer = int(fen_string[4])
        # moves
        self.moves = int(fen_string[5]) * 2 - 2
        if not self.turn: self.moves += 1

    def __str__(self):
        t = "\n    a   b   c   d   e   f   g   h  \n  +---+---+---+---+---+---+---+---+\n8 | # | # | # | # | # | # | " \
            "# | # |\n  +---+---+---+---+---+---+---+---+\n7 | # | # | # | # | # | # | # | # |\n  " \
            "+---+---+---+---+---+---+---+---+\n6 | # | # | # | # | # | # | # | # |\n  " \
            "+---+---+---+---+---+---+---+---+\n5 | # | # | # | # | # | # | # | # |\n  " \
            "+---+---+---+---+---+---+---+---+\n4 | # | # | # | # | # | # | # | # |\n  " \
            "+---+---+---+---+---+---+---+---+\n3 | # | # | # | # | # | # | # | # |\n  " \
            "+---+---+---+---+---+---+---+---+\n2 | # | # | # | # | # | # | # | # |\n  " \
            "+---+---+---+---+---+---+---+---+\n1 | # | # | # | # | # | # | # | # |\n  " \
            "+---+---+---+---+---+---+---+---+\n "
        for square in self.board:
            if not square.has_piece():
                t = t.replace("#", " ", 1)
            else:
                t = t.replace("#", square.piece.printable, 1)
        return t

    def make_move(self, move):
        """
        Makes a move on the board
        :param move: Move
        :return: None
        """

        p = self.board[move.current_pos].piece

        # print(p,self.board[move.target_pos], sep="")

        # en passant
        if self.en_passant.index == move.target_pos:
            self.board[move.target_pos + 8 * p.colour].piece = None
        if p.type == "p" and abs(move.current_pos - move.target_pos) == 16:
            self.en_passant = Square(move.target_pos + 8 * p.colour)
        else:
            self.en_passant = Square(-1)

        # castling
        if p.type == "k":
            if p.colour == WHITE:
                self.castling[0] = False
                self.castling[1] = False
            if p.colour == BLACK:
                self.castling[2] = False
                self.castling[3] = False
        if p.type == "r":
            if p.colour == WHITE:
                if move.current_pos == 63: self.castling[0] = False
                if move.current_pos == 56: self.castling[1] = False
            if p.colour == BLACK:
                if move.current_pos == 7: self.castling[2] = False
                if move.current_pos == 0: self.castling[3] = False
        if p.type == "k" and abs(move.current_pos - move.target_pos) == 2:
            if move.target_pos == 62:  # White KS
                self.board[61].piece = self.board[63].piece
                self.board[63].piece = None
            if move.target_pos == 58:  # White QS
                self.board[59].piece = self.board[56].piece
                self.board[56].piece = None
            if move.target_pos == 6:  # Black KS
                self.board[5].piece = self.board[5].piece
                self.board[7].piece = None
            if move.target_pos == 2:  # Black QS
                self.board[3].piece = self.board[0].piece
                self.board[0].piece = None

        self.board[move.target_pos].piece = self.board[move.current_pos].piece
        self.board[move.current_pos].piece = None

        self.turn *= -1
        self.moves += 1
        self.fifty_move_timer += 1

        if p.type == "p": self.fifty_move_timer = 0
        if self.is_check(self.turn): self.fifty_move_timer = 0

        if p.type == "p":
            if p.colour == WHITE and Square.index_to_coordinate(move.target_pos)[1] == 0:
                self.board[move.target_pos].piece = Piece(
                    move.promotion_piece.upper() if move.promotion_piece.lower() != "k" else "Q")
            if p.colour == BLACK and Square.index_to_coordinate(move.target_pos)[1] == 7:
                self.board[move.target_pos].piece = Piece(
                    move.promotion_piece.lower() if move.promotion_piece.lower() != "k" else "1")

    def get_win_state(self):
        """
        Checks if game has ended (2 for not ended else result)
        :return: Int
        """
        if len(self.get_legal_moves()) == 0:
            if self.is_check(self.turn):
                return self.turn
            else:
                return 0
        return 2

    def get_legal_moves(self):
        """
        Gets an array of all legal moves
        :return: Moves[]
        """
        moves = []
        for square in self.board:
            if square.has_piece():
                for square_target in self.board:
                    move = Move(square.index, square_target.index)
                    if move.is_valid(self):
                        moves.append(move)
        return moves

    def is_check(self, colour):
        """
        Checks if specified colour's king is in check
        :param colour: int
        :return: bool
        """
        king_pos = None
        for square in self.board:
            if square.has_piece():
                if square.piece.type == "k" and square.piece.colour == colour:
                    king_pos = square.index
                    break
        for square in self.board:
            if square.has_piece() and square.piece.colour == -colour:
                if square.piece.is_attacking(self, square.index, king_pos):
                    return True
        return False

    def clone(self):
        return deepcopy(self)


class Player:
    def __init__(self, name):
        self.name = name
        self.board = None
        self.move_queue = []

    def set_board(self, board):
        self.board = board

    def get_name(self):
        return self.name

    def add_move(self, move):
        """
        Adds a move to the move queue
        :param move: str
        :return: None
        """
        start, end = move.split(",")
        start, end = Square.algebraic_to_index(start), Square.algebraic_to_index(end)
        self.move_queue.append(Move(start, end))

    def get_move(self):
        """
        Gets the first move in the queue if it is legal otherwise it clears the move queue
        :return: Move or None
        """
        if len(self.move_queue) == 0:
            return None
        else:
            move = self.move_queue.pop(0)
            if move.is_valid(self.board):
                return move
            else:
                self.move_queue = []
                return None


class Game:
    def __init__(self, players):
        """
        Starts a game with given players
        :param players: Player[]
        """
        self.board = Board()
        self.w = players.pop(randint(0, 1))
        self.b = players.pop()
        self.w.set_board(self.board)
        self.b.set_board(self.board)

    def update_move(self):
        """
        Called every time a player adds a move to their queue or a move is played
        :return: None
        """
        moved = False
        if self.board.turn == 1:
            move = self.w.get_move()
        else:
            move = self.b.get_move()
        if move is not None:
            self.make_move(move)
            moved = True
            result = self.board.get_win_state()
            if result != 2:
                self.end_game(result)
        if moved:
            self.update_move()

    def make_move(self, move):
        """
        Makes move on the board and sends back the board state to each player
        :param move: Move
        :return: None
        """
        self.board.make_move(move)
        print(f"[MOVED] Made move {move}")
        # TODO send move to each player

    def end_game(self, result):
        """
        Ends the game and sends results to players
        :param result:
        :return:
        """
        print("Game ended with result:", result)
        print(self.board)


if __name__ == '__main__':
    b = Board(fen="8/6P1/8/8/8/k7/8/7K w - - 0 1")
    r = 2

    while r == 2:
        print(b)
        print(b.turn)

        m = input("--> ").split(" ")
        if len(m) == 2: m.append("q")
        mv = Move(Square.algebraic_to_index(m[0]), Square.algebraic_to_index(m[1]), m[2])

        if mv.is_valid(b):
            print(b.make_move(mv))
            r = b.get_win_state()

        else:
            print(f"{mv} is not valid")

    print(r)

if __name__ == "__main__":
    p1 = Player("t1")
    p2 = Player("t2")
    game = Game([p1, p2])
