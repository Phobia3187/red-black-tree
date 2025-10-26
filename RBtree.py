from enum import Enum


# Color Enumeration
class Color(Enum):
    RED = 0
    BLACK = 1

# Single Node In RB Tree
class Node:
    def __init__(self, value):
        self.value = value
        self.color = Color.RED
        self.left: 'Node' = None
        self.right: 'Node' = None
        self.parent: 'Node' = None

# Implement RB Tree    
class RedBlackTree:
    def __init__(self):
        self.EMPTY = Node(None)
        self.EMPTY.color = Color.BLACK
        self.root = self.EMPTY

# Required Methods For RBT

    # Insert into tree

# In-Order Tree Traversal
def in_order_traversal(self, node=None):
        if node is None:
            node = self.root
        
        if node != self.EMPTY:
            self.in_order_traversal(node.left)
            print(node.value)
            self.in_order_traversal(node.right)

    # Search tree for value
    # rotate left
    # rotate right
    # fix after insertion
    
