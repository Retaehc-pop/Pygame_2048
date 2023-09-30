import random
from os import path
import pygame as pg
import copy

pg.init()


class Block:
    COLORS = {
        "0": pg.Color(204, 192, 179),
        "2": pg.Color(238, 228, 218),
        "4": pg.Color(237, 224, 200),
        "8": pg.Color(242, 177, 121),
        "16": pg.Color(245, 149, 99),
        "32": pg.Color(246, 124, 95),
        "64": pg.Color(246, 94, 59),
        "128": pg.Color(237, 207, 114),
        "256": pg.Color(237, 204, 97),
        "512": pg.Color(237, 200, 80),
        "1024": pg.Color(237, 197, 63),
        "2048": pg.Color(237, 194, 46),
        "4096": pg.Color(237, 207, 114),
        "8192": pg.Color(237, 204, 97),
        "16384": pg.Color(237, 200, 80),
        "32768": pg.Color(237, 197, 63),
        "65536": pg.Color(237, 194, 46),
        "131072": pg.Color(237, 191, 29),
    }

    def __init__(self, value, pos):
        self.value = value
        self.pos = pos
        self.color = self.COLORS[str(self.value)]
        self.font = pg.font.SysFont("Clear Sans", 50)
        self.text = self.font.render(str(self.value), True, pg.Color("black"))

    def draw(self, screen: pg.Surface):
        self.border = pg.Rect(self.pos[1]*150, self.pos[0]*150, 150, 150)
        screen.fill(pg.Color(192, 192, 192), self.border)

        self.rect = pg.Rect((self.pos[1]*150)+5, (self.pos[0]*150)+5, 140, 140)
        screen.fill(self.color, self.rect)

        if self.value != 0:
            screen.blit(self.text, (self.pos[1]*150 + 75 - self.text.get_width(
            )//2, self.pos[0]*150 + 75 - self.text.get_height()//2))


class Board:
    def __init__(self, dimension):
        self.DIMENSION = dimension
        # self.grid = [[2, 2, 2, 2],
        #              [4, 4, 4, 4],
        #              [2, 2, 2, 2],
        #              [4, 4, 4, 4]]
        self.move = 0
        self.game_over = False
        self.score = 0
        self.temp_score = 0
        self.grid = [[0 for i in range(self.DIMENSION)] for j in range(self.DIMENSION)]
        self.grid = self.add_block(self.grid)
        self.grid = self.add_block(self.grid)

    def __str__(self):
        string = ""
        for row in self.grid:
            string += str(row) + "\n"
        return string

    def check_game_over(self) -> bool:
        for row in self.grid:
            if 0 in row:
                return False

        directions = ['l', 'r', 'u', 'd']
        grid = copy.deepcopy(self.grid)
        for direction in directions:
            if self.push_helper(direction, grid) != self.grid:
                return False
        return True

    def push_row(self, row):
        zeros = row.count(0)
        row = [i for i in row if i != 0]
        for _ in range(zeros):
            row.append(0)
        return row

    def combine_row(self, row):
        self.temp_score = 0
        for i in range(len(row)-1):
            if row[i] == row[i+1]:
                self.temp_score += row[i]*2
                row[i] *= 2
                row[i+1] = 0
        return row

    def push_grid(self, grid):
        for i, row in enumerate(grid):
            if all([i == 0 for i in row]):
                continue
            else:
                grid[i] = self.push_row(grid[i])
                grid[i] = self.combine_row(grid[i])
                grid[i] = self.push_row(grid[i])
        return grid

    def push_helper(self, direction, grid):
        if direction == "l":
            grid = self.push_grid(grid)

        elif direction == "r":
            grid = [row[::-1] for row in grid]
            grid = self.push_grid(grid)
            grid = [row[::-1] for row in grid]

        elif direction == "u":
            grid = self.rotate_grid(grid)
            grid = self.rotate_grid(grid)
            grid = self.rotate_grid(grid)
            grid = self.push_grid(grid)
            grid = self.rotate_grid(grid)

        elif direction == "d":
            grid = self.rotate_grid(grid)
            grid = self.push_grid(grid)
            grid = self.rotate_grid(grid)
            grid = self.rotate_grid(grid)
            grid = self.rotate_grid(grid)
        
        return grid
      
      
    def push(self, direction, grid):
        move = False
        original_grid = copy.deepcopy(grid)
        grid = self.push_helper(direction, grid)
        self.score += self.temp_score
        if grid != original_grid:
            self.move += 1
            grid = self.add_block(grid)
            move = True

        return grid,move

    def rotate_grid(self, grid):
        grid = list(zip(*grid[::-1]))
        for i, row in enumerate(grid):
            grid[i] = list(row)
        return grid

    def add_block(self, grid):
        free_space = []
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if col == 0:
                    free_space.append((i, j))
        new_block = random.choice(free_space)
        val = random.randint(1, 10)
        grid[new_block[0]][new_block[1]] = 2 if val > 1 else 4
        return grid

    def draw(self, screen):
        screen.fill(pg.Color("white"))
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                block = Block(self.grid[row][col], (row, col))
                block.draw(screen)
        screen_offset = 150*self.DIMENSION + 10
        score_font = pg.font.SysFont("Clear Sans", 30)
        score_text = score_font.render(
            f"Score: {self.score}", True, pg.Color("black"))
        screen.blit(score_text, (screen_offset, 10))
        
        move_text = score_font.render(
            f"Moves: {self.move}", True, pg.Color("black"))
        screen.blit(move_text, (screen_offset, 50))
        if self.game_over:
            game_over_font = pg.font.SysFont("Clear Sans", 50)
            game_over_text = game_over_font.render(
                "Game Over", True, pg.Color("black"))
            screen.blit(game_over_text, (screen_offset, 110))