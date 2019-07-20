from dataclasses import dataclass, field
from typing import Tuple
import numpy as np
import pygame
import time

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

class Grid:
    def __init__(self, rows, cols):
        self.width = cols 
        self.height = rows
        self.grid = np.empty((rows,cols), dtype=object)
        for row in range(rows):
            for col in range(cols):
                self.grid[row,col] = Tile(row, col, traversable=True)

    def render(self, screen):
        for row in self.grid:
            for tile in row:
                pygame.draw.rect(screen, tile.color, (tile.row*100,tile.col*100,100,100))

    def legal(self, agent, position):
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
            

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000,1000))

    g = Grid(6,4)
    a = Agent(1,1, color = (100,200,100))
    g.add_agent(a)

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                g.move(a,1,0)
                g.render(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()


#g = Grid(6,5)
#g.render()
#print('----')
#
#a = Agent(1,1, color = (20,20,20))
#g.add_agent(a)
#g.render()
#print('----')
#
#g.move(a,1,2)
#g.render()
