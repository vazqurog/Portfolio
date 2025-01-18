from node import Node

class LLStack:
    """Linked-list implementation of a stack data structure.

    This class provides methods to push elements onto the stack and pop elements from the stack.

    Attributes:
        size (int): The number of elements in the stack.
    """
    def __init__(self):
        "Intializes an empty stack"
        self.__head = None
        self.__size = 0

    @property
    def size(self):
        """int: Return the number of elements in the stack"""
        return self.__size

    def pop(self) -> tuple:
        """Removes and returns top element of the stack
        
        Returns:
            tuple: The dar from the top of the node of the stack
            
        Raises:
            IndexError: if the stakc is empty
            ValueError: if the node data is None"""
        
        if self.__size == 0:
            raise IndexError("Stack is empty")
        
        if self.__head.data is None:
            raise ValueError("Node does not contain data")
        
        # Create a temp variable to 
        popped_data = self.__head.data 

        # This handles a LL with only one node
        if self.__head.next is None:
            self.__head = None
        else:
            self.__head = self.__head.next
        self.__size -= 1

        return popped_data
    
    def push(self, data:tuple) -> None:
        """Push a tuple onto the top of the stack.

        Args:
            data (tuple): A tuple containing exactly two positive integers.

        Raises:
            TypeError: If data is not a tuple or its elements are not integers.
            ValueError: If the tuple elements are negative or the tuple does not contain exactly two values.
        """
        # Raises TypeError for non tuple passed type
        if not isinstance(data, tuple):
            raise TypeError("Data is not a tuple")
        
        # Raises Type error if tuple value is not an integer
        if not (isinstance(data[0], int) and isinstance(data[1], int)):
            raise TypeError("Node data: both elements must be integers")
        
        # Raises ValueError if objects in tuple are < 0
        if data[0] < 0 or data[1] < 0:
            raise ValueError("Node data: both values must be positive")
        
        # Rasies ValueError if tuple has a len not equal to 2.
        if len(data) != 2:
            raise ValueError("Data tuple must contain exactly two values")
        
        # Wraps the data tuple in a Node type then pushes it inside the stack
        push_node = Node(data)
        push_node.next = self.__head
        self.__head = push_node
        self.__size += 1 

    def __str__(self) -> str:
        """Returns a string represenation of the stack"""
        output = ''
        # tracks the current head
        tracker = self.__head
        while tracker:
            if output:
                output = (f"({tracker.data[0]},{tracker.data[1]}) -> ") + output
            else:
                output = (f"({tracker.data[0]},{tracker.data[1]})")
            tracker = tracker.next

        return output


if __name__ == "__main__":
    """ 
   stack = LLStack()
    stack.push((0,0))
    stack.push((0,1))
    stack.push((1,1))
    stack.push((1,2))
    stack.pop()
    #print(stack.pop())
    print(stack.__str__())
    """
    array = [[1, 2],
             [4, 5, 6],
             [7, 8, 9]]
    print(len(array[0]))