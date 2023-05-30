from chess.chess import Board
from random import randint


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
        # TODO send result to player


if __name__ == "__main__":
    b = Board()