#!/usr/bin/env python3
import curses
import random

TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
}

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.board = [[0]*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0

    def new_piece(self):
        shape = random.choice(list(TETROMINOS.values()))
        return Piece([row[:] for row in shape])

    def valid(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def lock_piece(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell and piece.y + y >= 0:
                    self.board[piece.y + y][piece.x + x] = 1
        self.clear_lines()
        self.current = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid(self.current):
            raise SystemExit

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared = BOARD_HEIGHT - len(new_board)
        self.score += cleared
        for _ in range(cleared):
            new_board.insert(0, [0]*BOARD_WIDTH)
        self.board = new_board

    def draw(self):
        self.stdscr.clear()
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    self.stdscr.addstr(y, x*2, '[]')
                else:
                    self.stdscr.addstr(y, x*2, '  ')
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell and y + self.current.y >= 0:
                    self.stdscr.addstr(self.current.y + y, (self.current.x + x)*2, '[]')
        self.stdscr.addstr(0, BOARD_WIDTH*2 + 2, f'Score: {self.score}')
        self.stdscr.refresh()

    def step(self):
        if self.valid(self.current, offset_y=1):
            self.current.y += 1
        else:
            self.lock_piece(self.current)

    def move(self, dx):
        if self.valid(self.current, offset_x=dx):
            self.current.x += dx

    def rotate(self):
        old_shape = [row[:] for row in self.current.shape]
        self.current.rotate()
        if not self.valid(self.current):
            self.current.shape = old_shape

    def run(self):
        self.stdscr.nodelay(True)
        while True:
            self.draw()
            try:
                key = self.stdscr.getch()
            except curses.error:
                key = -1
            if key == curses.KEY_LEFT:
                self.move(-1)
            elif key == curses.KEY_RIGHT:
                self.move(1)
            elif key == curses.KEY_UP:
                self.rotate()
            elif key == curses.KEY_DOWN:
                self.step()
            self.step()
            curses.napms(300)


def main(stdscr):
    curses.curs_set(0)
    game = Game(stdscr)
    game.run()

if __name__ == '__main__':
    curses.wrapper(main)
