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

# Insert Into Tree (BST)
def insert(self, value):
        new_node = Node(value)
        new_node.left = self.EMPTY
        new_node.right = self.EMPTY
        
        parent = None
        current = self.root
        
        while current != self.EMPTY:
            parent = current
            if new_node.value < current.value:
                current = current.left
            else:
                current = current.right
        
        new_node.parent = parent
        
        if parent is None:
            self.root = new_node
        elif new_node.value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
        
        new_node.color = Color.RED
        # We will need to call fix insert here, most likely.

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
    
