from dataclasses import dataclass, field
from typing import Tuple
import numpy as np


def itergrid(grid):
    return ()


@dataclass
class Tile:
    row: int
    col: int
    position: Tuple[int] = field(init=False)
    traversable: bool = True
    color: Tuple[int] = field(default_factory=lambda: (0,0,0))

    def __post_init__(self):
        self.position = (self.row, self.col)

    #build in way to do this?
    def update(self):
        self.__post_init__()

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

    def render(self):
        #print(self.grid)
        for row in self.grid:
            row_render = ''
            for tile in row:
                if tile.color == (0,0,0):
                    row_render += '#'
                else:
                    row_render += ' '
            print(row_render)

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
            


g = Grid(6,5)
g.render()
print('----')

a = Agent(1,1, color = (20,20,20))
g.add_agent(a)
g.render()
print('----')

g.move(a,1,2)
g.render()
