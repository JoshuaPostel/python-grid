from dataclasses import dataclass, field
from typing import Tuple
import numpy as np
import pygame
import time
import random

#TODO
def itergrid(grid):
    return ()

@dataclass
class Tile:
    row: int
    col: int
    position: Tuple[int] = field(init=False)
    traversable: bool = True
    color: Tuple[int] = field(default_factory=lambda: (200,0,0))

    def __post_init__(self):
        self.position = (self.row, self.col)

#TODO superclass of character for objects, projectile, agents
@dataclass
class Agent(Tile):
    height: int = 0
    speed: int = 0

#multi tile agent?



class Grid:
    def __init__(self, rows, cols, tile_size, boarder_size):
        self.width = cols 
        self.height = rows
        self.grid = np.empty((rows,cols), dtype=object)
        self.tile_size = tile_size
        self.boarder_size = boarder_size
        for row in range(rows):
            for col in range(cols):
                self.grid[row,col] = Tile(row, col, traversable=True)

    def render(self, screen):
        for row in self.grid:
            for tile in row:
                pygame.draw.rect(screen, tile.color,
                        ((1 + tile.row) * self.tile_size + self.boarder_size, 
                         (1 + tile.col) * self.tile_size + self.boarder_size,
                         self.tile_size - self.boarder_size,
                         self.tile_size - self.boarder_size))

    def legal(self, agent, position):
        if any(cord < 0 for cord in position):
            return False
        try:
            #make sure grid[position] exists
            self.grid[position]
        except:
            return False

        #TODO add different conditial checks based on agent properties  
        legality = self.grid[position].traversable == True 
        return legality

    #TODO generalize?
    def add_agent(self, agent):
        if self.legal(agent, agent.position):
            self.grid[agent.position] = agent
    
    #TODO store state of grid better (layers)
    def remove_agent(self, agent):
        self.grid[agent.position] = Tile(agent.row, agent.col, traversable=True)
        
    
    def move(self, agent, delta_row, delta_col):
        new_row = agent.row + delta_row
        new_col = agent.col + delta_col
        if self.legal(agent, (new_row, new_col)):
            self.remove_agent(agent)
            agent.row = new_row
            agent.col = new_col
            agent.__post_init__()
            self.add_agent(agent)

    def rotate(self):
        pass
            

actions = {
        b'h': (-1,0),
        b'j': (0,1),
        b'k': (0,-1),
        b'l': (1,0),}

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000,1000))

    board_width = 10
    board_length = 50
    g = Grid(board_width, board_length, 15, 2)
    player = Agent(1, 1, color = (100, 200, 100))
    g.add_agent(player)

    for i in range(25):
        agent = Agent(
                random.randrange(board_width),
                random.randrange(board_length),
                color = (100,100,200),
                traversable = False)

        g.add_agent(agent)
   
    rock = Agent(2, 3, color = (100,100,200), traversable = False)
    g.add_agent(rock)

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                action = actions.get(bytes([event.key]))
                g.move(player,action[0],action[1])
                g.render(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
