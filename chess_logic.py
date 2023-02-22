from copy import deepcopy

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


class Square:
    def __init__(self, pos=0, piece=None):
        self.index = pos
        self.piece = piece

    @staticmethod
    def algebraicToIndex(an):
        c = LETTERS.index(an[0])
        r = NUMBERS[::-1].index(an[1])
        return 8*r + c

    @staticmethod
    def indexToAlgebraic(i):
        c, r = Square.indexToCoordinate(i)
        return LETTERS[c]+NUMBERS[::-1][r]

    @staticmethod
    def indexToCoordinate(i):
        return i%8, i // 8

    @staticmethod
    def coordinateToIndex(square):
        c, r = square
        return c + r*8

    def hasPiece(self):
        return self.piece != None

    def hasAllyPiece(self, colour):
        if not self.hasPiece(): return False
        return self.piece.colour == colour

    def hasEnemyPiece(self, colour):
        if not self.hasPiece(): return False
        return self.piece.colour != colour

    def __str__(self):
        return Square.indexToAlgebraic(self.index)

    def __eq__(self, s):
        if not isinstance(s, Square):
            raise TypeError("Comparing and instace of Square to a differnet object.")
        return s.index == self.index


class Piece:
    def __init__(self, printable):
        self.colour = 1
        if printable.islower(): self.colour = -1
        self.type = printable.lower()

        self.printable = printable

    def __str__(self):
        #return self.printable
        return PIECES[self.type][self.colour]

    def isAttacking(self, board, cur_pos, target_pos):
        if self.type == "p" and self.colour == 1:
            if cur_pos - target_pos == 7 or cur_pos - target_pos == 9:
                if board.board[target_pos].hasEnemyPiece(self.colour):
                    return True
        if self.type == "p" and self.colour == -1:
            if cur_pos - target_pos == -7 or cur_pos - target_pos == -9:
                if board.board[target_pos].hasEnemyPiece(self.colour):
                    return True
        if self.type == "n":
            t = Square.indexToCoordinate(target_pos)
            c = Square.indexToCoordinate(cur_pos)
            o = t[0] - c[0], t[1] - c[1]
            if o in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)] and not board.board[target_pos].hasAllyPiece(self.colour):
                return True
        if self.type == "b":
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                col, row = Square.indexToCoordinate(cur_pos)
                while row >= 0 and col >= 0 and row <= 7 and col <= 7:
                    if not Square.coordinateToIndex((col, row)) == cur_pos:
                        if Square.coordinateToIndex((col, row)) == target_pos:
                            if not board.board[Square.coordinateToIndex((col, row))].hasAllyPiece(self.colour):
                                return True
                        if board.board[Square.coordinateToIndex((col, row))].hasPiece():
                            break
                    row += direction[0]; col += direction[1]
        if self.type == "r":
            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                col, row = Square.indexToCoordinate(cur_pos)
                while row >= 0 and col >= 0 and row <= 7 and col <= 7:
                    cur_checking = Square.coordinateToIndex((col, row))
                    if not cur_checking == cur_pos:
                        if cur_checking == target_pos:
                            if not board.board[cur_checking].hasAllyPiece(self.colour):
                                return True
                        if board.board[cur_checking].hasPiece():
                            break
                    row += direction[0]; col += direction[1]
        if self.type == "q":
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                col, row = Square.indexToCoordinate(cur_pos)
                while row >= 0 and col >= 0 and row <= 7 and col <= 7:
                    if not Square.coordinateToIndex((col, row)) == cur_pos:
                        if Square.coordinateToIndex((col, row)) == target_pos:
                            if not board.board[Square.coordinateToIndex((col, row))].hasAllyPiece(self.colour):
                                return True
                        if board.board[Square.coordinateToIndex((col, row))].hasPiece():
                            break
                    row += direction[0]; col += direction[1]
        if self.type == "k":
            t = Square.indexToCoordinate(target_pos)
            c = Square.indexToCoordinate(cur_pos)
            o = t[0] - c[0], t[1] - c[1]
            if o in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)] and not board.board[target_pos].hasAllyPiece(self.colour):
                return True
            if self.colour == 1:
                if target_pos == 62 and board.castling[0]:
                    if not board.board[62].hasPiece() and not board.board[61].hasPiece():
                        return True
                if target_pos == 28 and board.castling[1]:
                    if not board.board[59].hasPiece() and not board.board[58].hasPiece() and not board.board[57].hasPiece():
                        return True
                if target_pos == 6 and board.castling[2]:
                    if not board.board[6].hasPiece() and not board.board[5].hasPiece():
                        return True
                if target_pos == 2 and board.castling[3]:
                    if not board.board[1].hasPiece() and not board.board[2].hasPiece() and not board.board[3].hasPiece():
                        return True
        #print(f"{self} cannot move to {Square.indexToAlgebraic(target_pos)}")
        return False

    def canMove(self, board, cur_pos, target_pos):
        if board.turn != self.colour:
            #c = ["", "White", "Black"][board.turn]
            #print(f"{self} cannot move because it is {c}s turn")
            return False
        if self.type == "p" and self.colour == 1:
            if cur_pos - target_pos == 8:
                if not board.board[target_pos].hasPiece():
                    return True
            elif cur_pos - target_pos == 16 and cur_pos > 47:
                if not board.board[target_pos].hasPiece() and not board.board[cur_pos - 8].hasPiece():
                    return True
            elif cur_pos - target_pos == 7 or cur_pos - target_pos == 9:
                if board.board[target_pos].hasEnemyPiece(self.colour):
                    return True
                elif board.en_passant.index == target_pos:
                    return True
        if self.type == "p" and self.colour == -1:
            if cur_pos - target_pos == -8:
                if not board.board[target_pos].hasPiece():
                    return True
            elif cur_pos - target_pos == -16 and cur_pos < 16:
                if not board.board[target_pos].hasPiece() and not board.board[cur_pos + 8].hasPiece():
                    return True
            elif cur_pos - target_pos == -7 or cur_pos - target_pos == -9:
                if board.board[target_pos].hasEnemyPiece(self.colour):
                    return True
                elif board.en_passant.index == target_pos:
                    return True
        return self.isAttacking(board, cur_pos, target_pos)


class Move:
    def __init__(self, start_pos, target_pos):
        self.current_pos = start_pos
        self.target_pos = target_pos

    def __str__(self):
        return f"{Square.indexToAlgebraic(self.current_pos)} > {Square.indexToAlgebraic(self.target_pos)}"

    def __eq__(self, m):
        if not isinstance(m, Move):
            raise TypeError("Comparing and instace of Move to a differnet object.")
        return m.current_pos == self.current_pos and m.target_pos == self.target_pos

    def isValid(self, board):
        #print(board.board[self.current_pos].piece)
        if not board.board[self.current_pos].hasPiece:
            return False
        if not board.board[self.current_pos].piece.canMove(board, self.current_pos, self.target_pos):
            return False
        c = board.clone()
        c.makeMove(self)
        if c.isCheck(board.turn):
            del c
            return False
        del c
        return True


class Board:
    def __init__(self):
        self.board = [Square()] * 64 # empty board
        self.turn = 1 # 1: white, -1: black
        self.castling = [False] * 4
        self.en_passant = Square(-1) # no en passant square
        self.fifty_move_timer = 0 # counts to 100 halfmoves
        self.moves = 0

        self.loadFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def loadFEN(self, fen_to_load):
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
            self.en_passant = Square(Square.algebraicToIndex(fen_string[3]))
        # 50 move timer
        self.fifty_move_timer = int(fen_string[4])
        #moves
        self.moves = int(fen_string[5])*2 - 2
        if not self.turn: self.moves += 1

    def __str__(self):
        t = "\n    a   b   c   d   e   f   g   h  \n  +---+---+---+---+---+---+---+---+\n8 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n7 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n6 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n5 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n4 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n3 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n2 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n1 | # | # | # | # | # | # | # | # |\n  +---+---+---+---+---+---+---+---+\n"
        for square in self.board:
            if not square.hasPiece():
                t = t.replace("#", " ", 1)
            else:
                t = t.replace("#", square.piece.printable, 1)
        return t

    def makeMove(self, move):

        p = self.board[move.current_pos].piece

        #print(p,self.board[move.target_pos], sep="")

        # en passant
        if self.en_passant.index == move.target_pos:
            self.board[move.target_pos + 8*p.colour].piece = None
        if p.type == "p" and abs(move.current_pos - move.target_pos) == 16:
            self.en_passant = Square(move.target_pos + 8*p.colour)
        else:
            self.en_passant = Square(-1)

        # casling
        if p.type == "k":
            if p.colour == 1:
                self.castling[0] = False
                self.castling[1] = False
            if p.colour == -1:
                self.castling[2] = False
                self.castling[3] = False
        if p.type == "r":
            if p.colour == 1:
                if move.current_pos == 63: self.castling[0] = False
                if move.current_pos == 56: self.castling[1] = False
            if p.colour == -1:
                if move.current_pos == 7: self.castling[2] = False
                if move.current_pos == 0: self.castling[3] = False
        if p.type == "k" and abs(move.current_pos - move.target_pos) == 2:
            if move.target_pos == 62: # White KS
                self.board[61].piece = self.board[63].piece
                self.board[63].piece = None
            if move.target_pos == 58: # White QS
                self.board[59].piece = self.board[56].piece
                self.board[56].piece = None
            if move.target_pos == 6: # Black KS
                self.board[5].piece = self.board[5].piece
                self.board[7].piece = None
            if move.target_pos == 2: # Black QS
                self.board[3].piece = self.board[0].piece
                self.board[0].piece = None

        self.board[move.target_pos].piece = self.board[move.current_pos].piece
        self.board[move.current_pos].piece = None

        self.turn *= -1
        self.moves += 1
        self.fifty_move_timer += 1

        if p.type == "p": self.fifty_move_timer = 0
        if self.isCheck(self.turn): self.fifty_move_timer = 0

        #TODO promotion
        if p.type == "p":
            if p.colour == 1 and Square.indexToCoordinate(move.target_pos)[1] == 0:
                self.board[move.target_pos].piece = Piece("Q")
            if p.colour == -1 and Square.indexToCoordinate(move.target_pos)[1] == 7:
                self.board[move.target_pos].piece = Piece("q")

    def isGameOver(self):
        if len(self.getLegalMoves()) == 0:
            if self.isCheck(self.turn):
                return self.turn
            else:
                return 0
        return False

    def getLegalMoves(self):
        moves = []
        for square in self.board:
            if square.hasPiece():
                for sqaure_target in self.board:
                    move = Move(square.index, sqaure_target.index)
                    if move.isValid(self):
                        moves.append(move)
        return moves

    def isCheck(self, colour):
        king_pos = None
        for square in self.board:
            if square.hasPiece():
                if square.piece.type == "k" and square.piece.colour == colour:
                    king_pos = square.index
                    break
        for square in self.board:
            if square.hasPiece() and square.piece.colour == -colour:
                if square.piece.isAttacking(self, square.index, king_pos):
                    return True
        return False

    def clone(self):
        return deepcopy(self)


if __name__ == '__main__':
    board = Board()
    result = False

    while result == False:
        print(board)
        print(board.turn)

        m = input("--> ").split(" ")
        move = Move(Square.algebraicToIndex(m[0]), Square.algebraicToIndex(m[1]))

        if move.isValid(board):
            print(board.makeMove(move))
            result = board.isGameOver()

        else:
            print(f"{move} is not valid")

    print(result)