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
        self.left: "Node" = None
        self.right: "Node" = None
        self.parent: "Node" = None

# Implement RB Tree
class RedBlackTree:
    def __init__(self):
        self.EMPTY = Node(None)
        self.EMPTY.color = Color.BLACK
        self.root = self.EMPTY

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

    # Rotate left
    def _left_rotate(self, node):
        # Declare new paretn node
        new_parent = node.right

        # Move new parent's left subtree to location of node's right subtree
        node.right = new_parent.left

        # Update parent after subtree moves
        if new_parent.left != self.EMPTY:
            new_parent.left.parent = node

        # Update the parent of the new parent
        new_parent.parent = node.parent

        if node.parent is None:
            self.root = new_parent
        elif node == node.parent.left:
            node.parent.left = new_parent
        else:
            node.parent.right = new_parent
        # Make node the left child of the new parent
        new_parent.left = node
        node.parent = new_parent

    # Search Tree
    def search(self, value):
        current = self.root
        
        while current != self.EMPTY:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
                
        return None

# rotate right
# fix after insertion
