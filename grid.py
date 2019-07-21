from dataclasses import dataclass, field
from typing import Tuple, List
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
    color: Tuple[int] = field(default_factory=lambda: (200,100,100))
    height: int = 0

    def __post_init__(self):
        self.position = (self.row, self.col)

#TODO superclass of character for objects, projectile, agents
@dataclass
class Agent():
    tiles: List[Tile]
    speed: int = 0

    def __post_init__(self):
        self.positions = (tile.position for tile in self.tiles)

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

    def legal_tile(self, tile, position):
        if any(cord < 0 for cord in position):
            print(tile, 'FIRST')
            return False
        try:
            #make sure grid[position] exists
            self.grid[position]
        except:
            print(tile, 'SECOND')
            print(position)
            print(self.grid.shape)
            return False

        #TODO add different conditial checks based on agent properties  
        legality = self.grid[position].traversable == True 
        return legality

    def legal_agent(self, agent, positions):
        #assert len(agent.tiles) == len(positions)
        return all(self.legal_tile(tile, position) for tile, position in zip(agent.tiles, positions))

    #TODO generalize?
    def add_agent(self, agent):
        if self.legal_agent(agent, agent.positions):
            for tile in agent.tiles:
                self.grid[tile.position] = tile 
    
    #TODO store state of grid better (layers)
    def remove_agent(self, agent):
        for tile in agent.tiles:
            self.grid[tile.position] = Tile(tile.row, tile.col, traversable=True)
    
    def move_agent(self, agent, row_deltas, col_deltas):
        #assert len(agent.tiles) == len(row_deltas) == len(col_deltas)
        if legal_agent(agent, (row_deltas, col_deltas)):
            for tile, row_delta, col_delta in zip(agent.tiles, row_deltas, col_deltas):
                self.remove_tile(tile)
                tile.row = tile.row + row_delta
                tile.col = tile.col + col_delta 
                tile.__post_init__()
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

    board_width = 20
    board_length = 50
    g = Grid(board_width, board_length, 15, 2)
    player = Agent([Tile(1, 1, color = (100, 200, 100))])
    g.add_agent(player)

    mplayer = Agent([
        Tile(10, 10, color = (0,100,0), traversable = False),
        Tile(10, 11, color = (0,100,0), traversable = False),
        Tile(11, 10, color = (0,100,0), traversable = False),
        Tile(11, 11, color = (0,100,0), traversable = False),
        ])

    g.add_agent(mplayer)

#    for i in range(25):
#        agent = Agent([Tile(
#                random.randrange(board_width),
#                random.randrange(board_length),
#                color = (100,100,200),
#                traversable = False)])
#
#        g.add_agent(agent)
   
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                action = actions.get(bytes([event.key]))
                if action:
                    g.move(player,action[0],action[1])
                g.render(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
