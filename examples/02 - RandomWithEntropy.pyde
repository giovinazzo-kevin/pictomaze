from __future__ import division
import random as pyrand

class Cell:
    def __init__(self, x, y):
        # Cells only 'need' two walls because a minimum of two walls is always shared with another cell
        self.walls = {
            'right': True,
            'bottom': True
        }
        self.position   = (x, y)
        self.explored   = False
    
    def draw(self, w, h):
        x, y = self.position
        translate(x * w, y * h)
        if self.walls['right']:
            line(w, 0, w, h)
        if self.walls['bottom']:
            line(0, h, w, h)
        translate(-x * w, -y * h)
        

class Maze:
    def __init__(self):
        self.cells = []
        self.width = 0
        self.height = 0
    
    def draw(self):
        # Draw the boundaries (we're not going to bother with entrances and exits)
        line(0, 0, width, 0)
        line(0, 0, 0, height)
        line(width, 0, width, height)
        line(0, height, width, height)
        # Draw each cell
        cellWidth = width / self.width
        cellHeight = height / self.height
        for _ in self.cells:
            for cell in _:
                cell.draw(cellWidth, cellHeight)
                
    @staticmethod
    def _getNeighbours(cells, x, y):
        neighbours = []
        if x - 1 >= 0:
            neighbours.append( cells[x - 1][y] )
        if x + 1 < len(cells[0]):
            neighbours.append( cells[x + 1][y] )
        if y - 1 >= 0:
            neighbours.append( cells[x][y - 1] )
        if y + 1 < len(cells):
            neighbours.append( cells[x][y + 1] )
        return neighbours
        
    
    @staticmethod
    def _removeWallsBetween(a, b):
        # If a is to b's right, remove b's right wall
        if a.position[0] > b.position[0]:
            b.walls['right'] = False
        # Do the opposite for the opposite case
        elif a.position[0] < b.position[0]:
            a.walls['right'] = False
        # Same happens on the Y axis
        if a.position[1] > b.position[1]:
            b.walls['bottom'] = False
        elif a.position[1] < b.position[1]:
            a.walls['bottom'] = False
    
    @staticmethod
    def _randomWithEntropy(entropyBits):
        # Generate a number from 0x0000 to 0xFFFF. We can no longer use processing's random() because we want an integer.
        n = pyrand.randint(0, 0xF)
        # Make sure that 'entropyBits' is in the 0-4 range and cast it to int to be sure.
        entropy = int(min(4, max(0, entropyBits)))
        # Create a bitmask with as many 1s as our entropy value
        bitmask = 0xF << (4 - entropy)
        # And return the random number with the bitmask applied
        return n & bitmask
        
    
    @staticmethod
    def generate(w, h):
        maze = Maze()
        maze.width, maze.height = (w, h)
        # The array of cells from which we're going to remove walls and eventually return
        maze.cells = [[Cell(x, y) for y in range(h)] for x in range(w)]
        maze.cells[0][0].explored = True
        # A stack that works as the backbone of the algorithm and which offers a way to backtrack when a dead end is reached
        stack = [maze.cells[0][0]]
        # The starting cell is already explored, ergo "- 1"
        unexploredCellsLeft = w * h - 1
        # Get the position of the initial cell (which sits at the top of the stack)
        x, y = stack[-1].position
        while unexploredCellsLeft > 0:
            # Find any unexplored neighbours
            unexploredNeighbours = [n for n in Maze._getNeighbours(maze.cells, x, y) if not n.explored]
            if len(unexploredNeighbours) > 0:
                # Sort the neighbour list against the y-value of each element plus a random number that _sometimes_ makes the result higher than it should.
                chosenCell = sorted(unexploredNeighbours, key=lambda c: Maze._randomWithEntropy(4))[0]
                # Push the current cell to the stack
                stack.append(maze.cells[x][y])
                # Remove the wall between the current cell and the chosen cell
                Maze._removeWallsBetween(chosenCell, stack[-1])
                # Update the current coordinates
                x, y = chosenCell.position
                # Mark the chosen cell as explored
                chosenCell.explored = True
                # Reduce by one the number of unexplored cells left
                unexploredCellsLeft -= 1
            else:
                # Otherwise just update the current cell's position and pop the topmost element from the stack
                x, y = stack.pop().position
        return maze
        
maze = None
scalingFactor = 8

def setup():
    size(512, 512)
    strokeWeight(1)
    
    global maze
    maze = Maze.generate(width // scalingFactor, height // scalingFactor)
    
def draw():
    background(230)
    stroke(0)
    
    maze.draw()