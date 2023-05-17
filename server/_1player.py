import chess
from _chess_window import Window
from _ai import ComputerRandom

import pygame as pg


def run(colour):

    b = chess.Board()
    c = pg.time.Clock()
    p1 = Window(b, colour)
    p2 = ComputerRandom(b, -colour)

    outcome = False

    while outcome == False:
            
        if p1.update():
            break
        p2.update()

        pturn = p1
        if p1.colour != b.turn: pturn = p2
        if pturn.move_queue != []:
            if pturn.move_queue[0].isValid(b):
                b.makeMove(pturn.move_queue.pop(0))
                outcome = b.isGameOver()
            else:
                pturn.move_queue = []

        c.tick(60)

    pg.quit()
    if outcome == False: outcome = "Game quit"
    return outcome


if __name__ == "__main__":
    colour = int(input("Enter colour: "))

    print(run(colour))
