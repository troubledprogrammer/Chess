from chess.game import Square, Move


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
