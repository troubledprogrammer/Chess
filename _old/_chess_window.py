import pygame as pg
from chess import Square, Move


class HeldPiece:
    def __init__(self, index, display, img):
        self.index = index

        self.display = display
        self.image = img
        self.rect = self.image.get_rect()

    def draw(self):
        self.rect.center = pg.mouse.get_pos()
        self.display.blit(self.image, self.rect)


class Window:
    def __init__(self, board, colour):
        # window
        pg.init()
        pg.display.init()
        self.display = pg.display.set_mode((800, 800))
        pg.display.set_caption("chess")

        # textures
        self.board_image = pg.image.load(".../assets/board/wood/board.png")
        self.board_image = pg.transform.smoothscale(self.board_image, (800, 800))
        self.piece_images = {}
        for c in "pnbrqk":
            w = pg.image.load(f".../assets/pieces/default/w{c}.png")
            w = pg.transform.smoothscale(w, (100, 100))
            b = pg.image.load(f".../assets/pieces/default/b{c}.png")
            b = pg.transform.smoothscale(b, (100, 100))
            self.piece_images[c] = ["", w, b]

        # game
        self.game = board
        self.colour = colour

        # inputs
        self.events = []

        # selected
        self.selected = None

        # move
        self.move_queue = []

    def drawPieces(self):
        for square in self.game.board:
            if square.hasPiece():
                if self.selected == None or square.index != self.selected.index:
                    i = square.index
                    if self.colour == -1: i = 63 - i
                    pos = Square.indexToCoordinate(i)
                    img = self.piece_images[square.piece.type][square.piece.colour]
                    self.display.blit(img, (pos[0] * 100, pos[1] * 100))

    def onLeftMouseDown(self):
        x, y = pg.mouse.get_pos()
        index = Square.coordinateToIndex((x // 100, y // 100))
        if self.colour == -1: index = 63 - index
        s = self.game.board[index]
        if s.hasPiece():
            self.selected = HeldPiece(index, self.display, self.piece_images[s.piece.type][s.piece.colour])

    def onLeftMouseUp(self):
        if self.selected != None and self.game.board[self.selected.index].piece.colour == self.colour:
            x, y = pg.mouse.get_pos()
            index = Square.coordinateToIndex((x // 100, y // 100))
            if self.colour == -1: index = 63 - index
            self.move_queue.append(Move(self.selected.index, index))
        self.selected = None

    def updateInput(self):
        for event in self.events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.onLeftMouseDown()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.onLeftMouseUp()

    def shouldQuit(self):
        for event in self.events:
            if event.type == pg.QUIT:
                pg.quit()
                return True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    return True
        return False

    def update(self):

        # render
        self.display.fill((0, 0, 0))
        self.display.blit(self.board_image, (0, 0))
        self.drawPieces()
        if self.selected != None:
            self.selected.draw()
        pg.display.update()

        # input
        self.events = pg.event.get()
        self.updateInput()

        # window closed
        return self.shouldQuit()


if __name__ == "__main__":
    import chess
    from _ai import ComputerRandom

    b = chess.Board()
    c = pg.time.Clock()
    p1 = Window(b, 1)
    p2 = ComputerRandom(b, -1)

    outcome = False

    while outcome == False:

        if p1.update():
            break
        p2.update()

        pturn = [0, p1, p2][b.turn]
        if pturn.move_queue != []:
            if pturn.move_queue[0].isValid(b):
                b.makeMove(pturn.move_queue.pop(0))
                outcome = b.getWinState()
            else:
                pturn.move_queue = []

        c.tick(60)

    print(outcome)
