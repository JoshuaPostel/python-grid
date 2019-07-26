from dataclasses import dataclass, field
from typing import Tuple, List
import numpy as np
import pygame
import time
import random
import copy

#TODO
def itergrid(grid):
    return ()

@dataclass
class Tile:
    row: int
    col: int
    traversable: bool = True
    color: Tuple[int] = field(default_factory=lambda: (200,100,100))
    height: int = 0
    center: bool = False

    def __post_init__(self):
        self.position = (self.row, self.col)

#TODO superclass of character for objects, projectile, agents
@dataclass
class Agent():
    tiles: List[Tile]
    speed: int = 0

    def __post_init__(self):
        self.positions = [tile.position for tile in self.tiles]
        #TODO assert center uniqueness (and existance?)
        self.center = [tile.position for tile in self.tiles if tile.center == True]

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
            #print(tile, 'FIRST')
            return False
        try:
            #make sure grid[position] exists
            self.grid[position]
        except:
            #print(tile, 'SECOND')
            return False

        #TODO add different conditial checks based on agent properties  
        legality = self.grid[position].traversable == True 
        if not legality:
            #print(tile, 'THIRD')
            pass

        return legality

    def legal_agent(self, agent):
        return all([self.legal_tile(tile, position) for tile, position in zip(agent.tiles, agent.positions)])

    #TODO generalize?
    def add_agent(self, agent):
        if self.legal_agent(agent):
            for tile in agent.tiles:
                self.grid[tile.position] = tile 
    
    #TODO store state of grid better (layers)
    def remove_agent(self, agent):
        for tile in agent.tiles:
            self.grid[tile.position] = Tile(tile.row, tile.col, traversable=True)
   
    def move_agent(self, agent, moved_agent):
        if self.legal_agent(moved_agent):
            self.remove_agent(agent)
            self.add_agent(moved_agent)
            return moved_agent
        else:
            return agent

    def translate(self, agent, direction):
        new_agent = copy.deepcopy(agent)
        for tile in new_agent.tiles:
            tile.row += direction[0]
            tile.col += direction[1] 
            tile.__post_init__()

        new_agent.__post_init__()
        return self.move_agent(agent, new_agent)
        
    def rotate(self, agent, rotation_matrix):
        new_agent = copy.deepcopy(agent)
        center = np.array(agent.center)
        #if want to be fancy/efficent, vectorize this 
        for tile in new_agent.tiles:
            position = np.array(tile.position)
            normalized_position = position - center
            normalized_rotation = normalized_position * rotation_matrix
            rotation = normalized_rotation + center
            tile.row, tile.col = (cordinate for cordinate in rotation.tolist()[0])
            tile.__post_init__()
        
        new_agent.__post_init__()
        return self.move_agent(agent, new_agent)



translate_controls = {
        b'h': (-1,0),
        b'j': (0,1),
        b'k': (0,-1),
        b'l': (1,0)}

rotate_controls = {
        b'd': np.matrix([[0,-1],[1,0]]),
        b'f': np.matrix([[0,1],[-1,0]])}

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000,1000))

    board_width = 20
    board_length = 50
    g = Grid(board_width, board_length, 15, 2)
    player = Agent([Tile(1, 1, color = (100, 200, 100)),
                    Tile(1, 2, color = (100, 200, 100)),
                    Tile(1, 3, color = (100, 200, 100)),
                    Tile(2, 2, color = (100, 200, 100), center = True),
                    ])
    g.add_agent(player)

    for i in range(25):
        agent = Agent([Tile(
                random.randrange(board_width),
                random.randrange(board_length),
                color = (100,100,200),
                traversable = False)])

        g.add_agent(agent)
   
    mplayer = Agent([
        Tile(10, 10, color = (0,100,0), traversable = False),
        Tile(10, 11, color = (0,100,0), traversable = False),
        Tile(11, 10, color = (0,100,0), traversable = False),
        Tile(11, 11, color = (0,100,0), traversable = False),
        ])

    g.add_agent(mplayer)

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                translate_action = translate_controls.get(bytes([event.key]))
                if translate_action:
                    player = g.translate(player, translate_action)
                rotate_action = rotate_controls.get(bytes([event.key]))
                if rotate_action is None:
                    pass
                else:
                    player = g.rotate(player, rotate_action)
                g.render(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
