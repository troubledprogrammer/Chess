from random import choice

class Computer:
    def __init__(self, board, colour):
        self.game = board
        self.colour = colour

        self.move_queue = []


class ComputerRandom(Computer):
    def __init__(self, board, colour):
        super().__init__(board, colour)
    
    def update(self):
        if self.game.turn == self.colour:
            self.move_queue.append(choice(self.game.get_legal_moves()))
