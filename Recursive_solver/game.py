from typing import Optional, List
from llstack import LLStack
from node import Node

class InvalidCoordinateError(Exception):
    "Exception raised when the coordinate is equal to ocean"
    pass

class OutOfBoundaries(Exception):
    """Exception raised when coordinates that are out bounds are passed"""
    pass


class Map:
    """A class representing a map grid with start and end coordinates.

    The Map class holds the grid, start and end coordinates, and provides methods to set these coordinates with validation.

    Attributes:
        grid (List[List[str]]): The grid representing the map.
        start_coords (tuple): The starting coordinates on the grid.
        end_coords (tuple): The ending coordinates on the grid.
        ll_path (LLStack): A stack to store the path found on the map.
    """
    def __init__(self, grid: List[List[str]], start_loc: tuple, end_loc: tuple):
        """Initialize the Map with a grid and start/end locations.

        Args:
            grid (List[List[str]]): A list of lists representing the map grid. Each cell should be 'grass' or 'ocean'.
            start_loc (tuple): A tuple (row, col) representing the starting location.
            end_loc (tuple): A tuple (row, col) representing the ending location.

        Raises:
            TypeError: If grid is not a list of lists, or if cell values are not strings.
            ValueError: If cell values are not 'grass' or 'ocean'.
            TypeError: If start_loc or end_loc is not a tuple.
            InvalidCoordinateError: If the start or end location is in the ocean.
            OutOfBoundaries: If the start or end coordinates are out of the grid boundaries.
        """
        for row in range(len(grid)):
            if not isinstance(grid[row], list):
                raise TypeError("Grid must contain a list of lists")
            
            for col in range(len(grid[row])): 
                if not isinstance(grid[row][col], str):
                    raise TypeError("Cell values must be of type: str")
                
                if grid[row][col] != 'grass' and grid[row][col] != 'ocean':
                    raise ValueError("Cell value must be 'ocean' or 'grass'")
                
        self.__grid = grid
        self.__start = None
        self.__end = None
        self.start_coords = start_loc
        self.end_coords = end_loc
        self.ll_path = LLStack()
    @property
    def grid(self):
        """List[List[str]]: The grid representing the map."""
        return self.__grid
    
    @property
    def start_coords(self): 
        """tuple: The starting coordinates on the grid.""" 
        return self.__start
    
    @property
    def end_coords(self):
        """tuple: The ending coordinates on the grid."""
        return self.__end
    
    @start_coords.setter
    def start_coords(self, new_start: tuple):
        """Set the starting coordinates with validation.

        Args:
            new_start (tuple): A tuple (row, col) representing the new starting location.

        Raises:
            ValueError: If new_start is the same as the current start_coords or has invalid values.
            TypeError: If new_start is not a tuple or its elements are not integers.
            OutOfBoundaries: If the coordinates are out of grid boundaries.
            InvalidCoordinateError: If the new_start is in the ocean.
        """

        if self.start_coords == new_start:
            raise ValueError
        # Chcecks that new_start is a tuple
        if not isinstance(new_start, tuple):
            raise TypeError
        
        # Checks that both values in the tuple are integers
        if not isinstance(new_start[0], int) or not (isinstance(new_start[1], int)):
            raise TypeError
        
        # Checks that both ints in new_start are non-negative
        if new_start[0] < 0 or new_start[1] < 0:
            raise ValueError
        
        # Checks that len of tuple is 2
        if len(new_start) != 2:
            raise ValueError

        #check for the current row 
        if new_start[0] >= len(self.__grid):
            raise OutOfBoundaries("Start row is out of grid boundaries")
        
        #check for the current column 
        if new_start[1] >= len(self.__grid[new_start[0]]):
            print(len(self.__grid))

            raise OutOfBoundaries("Start column is out of grid boundaries")
        
        # Check that the new_start coordis are not an ocean
        if self.__grid[new_start[0]][new_start[1]] == 'ocean':
            raise InvalidCoordinateError("Start location cannot be in the ocean")
        
        # Sets the new start is all the other checks pass 
        self.__start = new_start
    
    @end_coords.setter
    def end_coords(self, new_end: tuple):
        """Set the ending coordinates with validation.

        Args:
            new_end (tuple): A tuple (row, col) representing the new ending location.

        Raises:
            ValueError: If new_end is the same as start_coords or has invalid values.
            TypeError: If new_end is not a tuple or its elements are not integers.
            OutOfBoundaries: If the coordinates are out of grid boundaries.
            InvalidCoordinateError: If the new_end is in the ocean.
        """
        # Checks that new_end is not equal to start_coords
        if new_end == self.start_coords:
            raise ValueError
        
        # Checks the new_end type is a tuple
        if not isinstance(new_end, tuple):
            raise TypeError
        
        #Checks both values inside the tuple is an Int
        if not isinstance(new_end[0], int) or not isinstance(new_end[1], int):
            raise TypeError
        
        #Checks that both new end values are positive
        if new_end[0] < 0 or new_end[1] < 0:
            raise ValueError
        
        # Raises ValueError if new_end tuple is not equal to 2
        if len(new_end) != 2:
            raise ValueError
        
        if new_end[0] >= len(self.grid):
            raise OutOfBoundaries("End row is out of boudns")
        
        if new_end[1] >= len(self.grid[new_end[0]]):
            raise OutOfBoundaries("end column is out of bounds")
        
        if self.grid[new_end[0]][new_end[1]] == 'ocean':
            raise InvalidCoordinateError
        
        self.__end = new_end
        
    def find_path(self): 
        """
        Find a path from the start to the end point in the maze.

        This is the top-level method to solve the maze 

        Returns:
            LLStack: A stack representing the valid path through the map
            None: If the map is not solvable and no path exists.
        """
        crumb = set()             
        if self.solve(self.grid, self.start_coords, self.end_coords, crumb):
            return self.ll_path
        else:
            return None  

    
    def solve(self, grid, start: tuple, end: tuple, crumb):
        """Recursively search for a path from the start to the end position in the grid.

    This method attempts to find a valid path from the start coordinate to the end coordinate
    in the grid by exploring neighboring cells recursively. I used the Manhattan distance
    heuristic to prioritize .

    Args:
        grid (List[List[str]]): The grid representing the maze, containing 'grass' (traversable)
            and 'ocean' (blocked) cells.
        start (tuple): The current position as a tuple (row, column).
        end (tuple): The end position to reach as a tuple (row, column).
        crumb (set): A set of positions that have been visited to prevent revisiting (like leaving a bread crumb).

    Returns:
        bool: True if a path to the end is found, False otherwise.
    """
        sx, sy = start
        ex, ey = end

        # Check if the end coords have been reached
        if sx == ex and sy == ey:
            self.ll_path.push((sx, sy))
            return True
        # Leave a crumb at the current cell
        crumb.add((sx, sy))

        # Define neighboring positions
        north = (sx - 1, sy)
        west = (sx, sy - 1)
        south = (sx + 1, sy)
        east = (sx, sy + 1)

        # A boolean for the recursive call cases
        n_bool = False
        w_bool = False
        e_bool = False
        s_bool = False
        
        # Defaulted to larger number due to a NoneType Error eith comparison
        ndis = 5000
        edis = 5000
        wdis = 5000
        sdis = 5000

        # calculate the distance between each enighbor and the end coord
        if self.solve_helper(grid, north[0], north[1], end, crumb):
            ndis = (abs(north[0] - end[0]) + (abs(north[1] - end[1])))
            n_bool = True

        if self.solve_helper(grid, west[0], west[1], end, crumb):
            wdis =(abs(west[0] - end[0]) + (abs(west[1] - end[1])))
            w_bool = True

        if self.solve_helper(grid, south[0], south[1], end, crumb):
            sdis = (abs(south[0] - end[0]) + (abs(south[1] - end[1])))
            s_bool = True
        
        if self.solve_helper(grid, east[0], east[1], end, crumb):
            edis = (abs(east[0] - end[0]) + (abs(east[1] - end[1])))
            e_bool = True

        min_dis = min(ndis, edis, wdis, sdis)
        if min_dis == 5000:
            print("No path found: min_dis return")
            return False
        
        # North check
        if n_bool and ndis == min_dis:
            if self.solve(grid, north, end, crumb):
                self.ll_path.push((sx, sy))
                print('North')
                return True
            
        # West Check
        elif w_bool and wdis == min_dis:
            if self.solve(grid, west, end, crumb):
                self.ll_path.push((sx, sy))
                print("west")
                return True
        
        # South Check
        elif s_bool and sdis == min_dis:
            if self.solve(grid, south, end, crumb):
                self.ll_path.push((sx, sy))
                print("South")
                return True

        # East Check 
        elif e_bool and edis == min_dis:
            if self.solve(grid,east, end, crumb):
                self.ll_path.push((sx, sy))
                print("east")
                return True
    
        else:
            print('No path found')
            return None
    
    def solve_helper(self, grid, sx, sy, end, crumb):
        """
        Check if a given cell is valid for exploration in the maze.

        This helper method verifies whether the cell at coordinates (sx, sy) is a valid position
        to move to in the maze. It ensures that the cell is within the grid boundaries, has not
        been visited before.

        Args:
            grid (List[List[str]]): The grid representing the maze.
            sx (int): The row index (x-coordinate) of the cell to check.
            sy (int): The column index (y-coordinate) of the cell to check.
            end (tuple): The end position in the maze (unused in this method but included for consistency).
            crumb (set): A set of positions that have been visited to prevent revisiting.

        Returns:
            bool: True if the cell is valid for exploration, False otherwise.
        """
        # Verify ranges of the new coordinates
        if sx < 0 or sx >= len(grid):
            return False
        if sy < 0 or sy >= len(grid[sx]):
            return False

        # Check if the cell has already been visited
        if (sx, sy) in crumb:
            return False

        # check if the cell is grass
        if grid[sx][sy] != 'grass':
            return False

        return True



    def find_shortest_path(self, grid, start, end, llstack):
        pass

if __name__ == "__main__":
    invalid_grid_bad_str = [
            ['not grass', 'dune buggy', 'not ocean'],
            ['invalid', 'friday morning', 'jojo'],
            [74, 91.2, 'bad data']
        ]
    valid_grid = [
            ['grass', 'ocean'],
            ['grass', 'ocean', 'ocean', 'grass'],
            ['grass', 'ocean', 'ocean', 'grass', 'ocean'],
            ['grass', 'grass', 'grass', 'grass']
    ]
    
    m1 = Map(valid_grid, (0,0), (1,0))

"""

"""