import pygame as pg
from Board import Board
pg.init()

WIDTH = 800
HEIGHT = 600
DIMENSION = 4
SQUARE_SIZE = HEIGHT // DIMENSION


def main():
    RUNNING = True
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pg.Color("white"))
    clock = pg.time.Clock()
    board = Board(DIMENSION)

    

    while RUNNING:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                RUNNING = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    RUNNING = False
                elif event.key == pg.K_r:
                    board = Board(DIMENSION)
                elif event.key == pg.K_w or event.key == pg.K_UP:
                    board.grid,_ = board.push("u", board.grid)
                elif event.key == pg.K_a or event.key == pg.K_LEFT:
                    board.grid,_ = board.push("l", board.grid)
                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    board.grid,_ = board.push("d", board.grid)
                elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                    board.grid,_ = board.push("r", board.grid)
                
                elif event.key == pg.K_SPACE:
                    board.grid = board.rotate_grid(board.grid)
                    
                if board.check_game_over():
                    board.game_over = True

        board.draw(screen)
        pg.display.update()


if __name__ == "__main__":
    main()


