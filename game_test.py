import unittest

from node import Node
from llstack import LLStack
from game import Map, InvalidCoordinateError, OutOfBoundaries

class TestLlStack(unittest.TestCase):
    """Unit tests for the LLStack class."""

    def test_init(self):
        """Test that the LLStack initializes with an empty head and size zero."""
        stack = LLStack()
        # Accessed __head using this format due to no property being made for head
        # I was also testing as I developed so I had no push method so I manually set head
        # Until I started working on the push function
        self.assertEqual(stack._LLStack__head, None)
        self.assertEqual(stack.size, 0)

    def test_pop_empty_stack(self):
        """Assert that popping from an empty stack raises IndexError."""
        stack = LLStack()
        with self.assertRaises(IndexError):
            stack.pop()

    def test_pop_none_data(self):
        """Assert that popping a node with None data raises ValueError."""
        stack = LLStack()
        node = Node(None)
        stack._LLStack__size = 1
        stack._LLStack__head = node
        
        with self.assertRaises(ValueError):
            stack.pop()

    def test_pop_small_ll(self):
        """Test popping from a stack with one node."""
        node = Node((1, 1))
        stack = LLStack()
        stack._LLStack__head = node
        stack._LLStack__size = 1
        self.assertEqual(stack.pop(), (1, 1))
        # Verify stack size after popping a value
        self.assertEqual(stack.size, 0)

    def test_pop_large_ll(self):
        """Test popping from a stack with multiple nodes."""
        node = Node((1, 1), Node((2, 2), Node((3, 3))))
        stack = LLStack()
        stack._LLStack__head = node
        stack._LLStack__size = 2
        self.assertEqual(stack.pop(), (1, 1))

    def test_pop_len_of_one_ll(self):
        """Test popping from a stack and checking size is updated correctly."""
        node = Node((1, 1))
        stack = LLStack()
        stack._LLStack__head = node
        stack._LLStack__size = 1
        self.assertEqual(stack.pop(), (1, 1))
        self.assertEqual(0, stack.size)

    def test_push_single(self):
        """Test pushing a single element onto the stack."""
        stack = LLStack()
        data = (0, 0)
        stack.push(data)
        self.assertEqual(stack._LLStack__head.data, (0, 0))

    def test_push_multiple(self):
        """Test pushing multiple elements onto the stack."""
        stack = LLStack()
        push_data = [(0, 0), (0, 1), (0, 2)]

        for data in push_data:
            stack.push(data)
            self.assertEqual(stack._LLStack__head.data, data)

    def test_push_bad_data(self):
        """Assert that pushing invalid data raises appropriate exceptions."""
        stack = LLStack()
        # TypeError Vars
        bad_data_non_tuple = 'Not a tuple'
        bad_data_non_int_tuple_first_val = ('Not an int', 1)
        bad_data_non_int_tuple_second_val = (0, "Not an int")
        bad_data_non_int_both = ("im so tired", 'im so tired')
        with self.assertRaises(TypeError):
            stack.push(bad_data_non_tuple)
        with self.assertRaises(TypeError):
            stack.push(bad_data_non_int_tuple_first_val)
        with self.assertRaises(TypeError):
            stack.push(bad_data_non_int_tuple_second_val)
        with self.assertRaises(TypeError):
            stack.push(bad_data_non_int_both)

        # ValueError Vars
        bad_data_wrong_len = (1, 2, 3, 4, 5, 6)
        bad_data_int_out_range_first_value = (-1, 1)
        bad_data_int_out_range_second_value = (1, -1)
        bad_data_int_out_range_both = (-1, -1)

        with self.assertRaises(ValueError):
            stack.push(bad_data_wrong_len)
        with self.assertRaises(ValueError):
            stack.push(bad_data_int_out_range_first_value)
        with self.assertRaises(ValueError):
            stack.push(bad_data_int_out_range_second_value)
        with self.assertRaises(ValueError):
            stack.push(bad_data_int_out_range_both)

    def test_string_output(self):
        """Test the string representation of the stack."""
        # FIXME: Outputs the string but doesn't pass professor test
        # FIXED
        # FIXME: Passing self as a parameter in test_string_output causes an issue?
        # STOP FORGETTING PARENTHESIS WHEN CREATING AN INSTANCE OF A CLASS
        # FIXED
        stack = LLStack()
        for i in range(0, 2):
            for j in range(0, 2):
                stack.push((i, j))
        # You might want to add assertions here to check the output

class TestMap(unittest.TestCase):
    """Unit tests for the Map class."""

    def setUp(self):
        """Set up valid and invalid grids and coordinates for testing."""
        self.valid_grid = [
            ['grass', 'ocean'],
            ['grass', 'ocean', 'ocean', 'grass'],
            ['grass', 'ocean', 'ocean', 'grass', 'ocean'],
            ['grass', 'grass', 'grass', 'grass']
        ]

        self.invalid_grid = [
            ['not grass', 'dune buggy', 'not ocean'],
            ['invalid', 'friday morning', 'jojo'],
            [74, 91.2, 'bad data']
        ]

        self.invalid_grid_non_str = [
            [1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2],
            [0],
            [430947390, 1, 1, 1]
        ]
        
        self.start_coords_valid = (0, 0)
        self.end_coords_valid = (3, 3)

        # Initialize a valid map 
        self.valid_map = Map(self.valid_grid, self.start_coords_valid, self.end_coords_valid)

    # -- GRID TESTING ---
    def test_grid_init(self):
        """Test initialization with invalid grids raises appropriate exceptions."""
        # Test for a grid with non 'grass' and 'ocean' strings
        with self.assertRaises(ValueError):
            invalid_map = Map(self.invalid_grid, self.start_coords_valid, self.end_coords_valid)

        with self.assertRaises(TypeError):
            invalid_map_lst_of_non_lst = Map([{"not a list": 5}], self.start_coords_valid, self.end_coords_valid)

        with self.assertRaises(TypeError):
            invalid_map_lst_of_non_str = Map(self.invalid_grid_non_str, self.start_coords_valid, self.end_coords_valid)

    # --- START COORDS TESTING ---
    def test_start_coords_non_tuple(self):
        """Test that non-tuple start coordinates raise TypeError."""
        non_tuple_start = [0, 0]

        with self.assertRaises(TypeError):
            test = Map(self.valid_grid, non_tuple_start, self.end_coords_valid)

    def test_start_coords_non_integer(self):
        """Test that non-integer start coordinates raise TypeError."""
        non_int_start = 'not an integer'

        with self.assertRaises(TypeError):
            test = Map(self.valid_grid, non_int_start, self.end_coords_valid)

    def test_start_coords_negative_x(self):
        """Test that negative X in start coordinates raises ValueError."""
        negative_start_x = (-1, 1)

        with self.assertRaises(ValueError):
            test = Map(self.valid_grid, negative_start_x, self.end_coords_valid)
    
    def test_start_coords_negative_y(self):
        """Test that negative Y in start coordinates raises ValueError."""
        negative_start_y = (1, -1)

        with self.assertRaises(ValueError):
            test = Map(self.valid_grid, negative_start_y, self.end_coords_valid)

    def test_start_coords_length(self):
        """Test that start coordinates of incorrect length raise ValueError."""
        non_two_len_start = (1, 2, 3, 4)
        with self.assertRaises(ValueError):
            test = Map(self.valid_grid, non_two_len_start, self.end_coords_valid)

    def test_start_coords_x_out_of_bounds(self):
        """Test that start X coordinate out of bounds raises OutOfBoundaries."""
        invalid_start_x = (5, 0)

        with self.assertRaises(OutOfBoundaries):
            test = Map(self.valid_grid, invalid_start_x, self.end_coords_valid)

    def test_start_coords_y_out_of_bounds(self):
        """Test that start Y coordinate out of bounds raises OutOfBoundaries."""
        invalid_start_y = (0, 2)
        with self.assertRaises(OutOfBoundaries):
            test = Map(self.valid_grid, invalid_start_y, self.end_coords_valid)

    def test_start_coords_invalid_coord_error(self):
        """Test that start coordinates in 'ocean' raise InvalidCoordinateError."""
        invalid_coord_ocean = (0, 1)
        with self.assertRaises(InvalidCoordinateError):
            test = Map(self.valid_grid, invalid_coord_ocean, self.end_coords_valid)
    
    # --- END COORD TESTING ---
    def test_end_coords_non_tuple(self):
        """Test that non-tuple end coordinates raise TypeError."""
        non_tuple_end = [0, 0]

        with self.assertRaises(TypeError):
            test = Map(self.valid_grid, self.start_coords_valid, non_tuple_end)

    def test_end_coords_non_integer(self):
        """Test that non-integer end coordinates raise TypeError."""
        non_int_end = 'not an integer'

        with self.assertRaises(TypeError):
            test = Map(self.valid_grid, self.start_coords_valid, non_int_end)

    def test_end_coords_negative_x(self):
        """Test that negative X in end coordinates raises ValueError."""
        negative_end_x = (-1, 1)

        with self.assertRaises(ValueError):
            test = Map(self.valid_grid, self.start_coords_valid, negative_end_x)
    
    def test_end_coords_negative_y(self):
        """Test that negative Y in end coordinates raises ValueError."""
        negative_end_y = (1, -1)

        with self.assertRaises(ValueError):
            test = Map(self.valid_grid, self.start_coords_valid, negative_end_y)

    def test_end_coords_length(self):
        """Test that end coordinates of incorrect length raise ValueError."""
        non_two_len_end = (1, 2, 3, 4)
        with self.assertRaises(ValueError):
            test = Map(self.valid_grid, self.start_coords_valid, non_two_len_end)

    def test_end_coords_x_out_of_bounds(self):
        """Test that end X coordinate out of bounds raises OutOfBoundaries."""
        invalid_end_x = (5, 0)

        with self.assertRaises(OutOfBoundaries):
            test = Map(self.valid_grid, self.start_coords_valid, invalid_end_x)

    def test_end_coords_y_out_of_bounds(self):
        """Test that end Y coordinate out of bounds raises OutOfBoundaries."""
        invalid_end_y = (0, 2)
        with self.assertRaises(OutOfBoundaries):
            test = Map(self.valid_grid, self.start_coords_valid, invalid_end_y)

    def test_end_coords_invalid_coord_error(self):
        """Test that end coordinates in 'ocean' raise InvalidCoordinateError."""
        invalid_coord_ocean = (0, 1)
        with self.assertRaises(InvalidCoordinateError):
            test = Map(self.valid_grid, self.start_coords_valid, invalid_coord_ocean)
    
    def test_different_coords(self):
        """Placeholder test for different coordinate scenarios."""
        pass
    
    def test_solve_valid_path(self):
        """Test that a valid path is found in the maze."""
        # FIXME: Moved LLStack variable and it returns a valid path, LLStack doesn't show last coord
        crumb = set()
        valid_grid_v2 = [
            ['grass', 'ocean'],
            ['grass', 'grass', 'ocean', 'grass'],
            ['grass', 'grass', 'ocean', 'grass', 'ocean'],
            ['ocean', 'grass', 'grass', 'grass']
        ]
        start_coords = (0, 0)
        end_coords = (3, 3)
        game = Map(valid_grid_v2, start_coords, end_coords)
        game.find_path()
        # You might want to add assertions to check that the path is correct

    def test_grid_no_solution(self):
        """Test that find_path returns None when no path exists."""
        crumb = set()
        grid = [
            ['grass', 'ocean', 'grass', 'grass'],
            ['ocean', 'grass', 'ocean'],
            ['grass', 'grass', 'grass', 'ocean', 'grass'],
            ['ocean', 'grass'],
            ['grass', 'ocean', 'grass'],
            ['grass']
        ]

        start_coords = (0, 0)
        end_coords = (5, 0)
        game = Map(grid, start_coords, end_coords)
        self.assertIsNone(game.find_path())

if __name__ == "__main__":
    map_tester = TestMap()
    map_tester.test_solve_valid_path()
    #unittest.main()
    #Stack_tester = TestLlStack()
    #Stack_tester.test_string_output()
    #map_tester.test_grid_init()


        