from dataclasses import dataclass, field
from typing import Tuple
import numpy as np


def itergrid(grid):
    return ()


@dataclass
class Tile:
    row: int
    column: int
    position: Tuple[int] = field(init=False)
    traversable: bool = True
    color: Tuple[int] = field(default_factory=lambda: (0,0,0))

    def __post_init__(self):
        self.position = (self.row, self.column)

#TODO superclass of character for objects, projectile, agents
@dataclass
class Agent(Tile):
    height: int = 0
    speed: int = 0

class Grid:
    def __init__(self, rows, columns):
        self.width = columns 
        self.height = rows
        self.grid = np.empty((rows,columns), dtype=object)
        for row in range(rows):
            for column in range(columns):
                self.grid[row,column] = Tile(row, column, traversable=True)

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

    #TODO generalize?
    def add_agent(self, agent):
        #print(self.grid[agent.position])
        if self.grid[agent.position].traversable == True:
            self.grid[agent.position] = agent
    
    def move(self, agent, direction):
        pass


g = Grid(6,5)
g.render()
print('\n\n')

a = Agent(1,1, color = (20,20,20))
g.add_agent(a)
g.render()
