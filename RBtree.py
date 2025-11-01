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
        self.fix_insert(new_node)

    # In-Order Tree Traversal
    def in_order_traversal(self, node=None):
        if node is None:
            node = self.root

        if node != self.EMPTY:
            self.in_order_traversal(node.left)
            print(node.value)
            print(node.color)
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

    # Rotate Right
    def _right_rotate(self, node):
        new_parent = node.left

        node.left = new_parent.right

        if new_parent.right != self.EMPTY:
            new_parent.right.parent = node

        new_parent.parent = node.parent

        if node.parent is None:
            self.root = new_parent
        elif node == node.parent.right:
            node.parent.right = new_parent
        else:
            node.parent.left = new_parent

        new_parent.right = node
        node.parent = new_parent
        # I would never copy and paste this from the other rotate function. :)

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

    # Delete a node   /// IN PROGRESS. ILL WRAP THIS UP BY SATURDAY MORE COMPLICATED THAN I THOUGHT///
    def delete(self, value):
        node = self.search(value)

        # Remember original node color for fixing the delete
        originalNode = node
        originalColor = originalNode.color

    
    # Fix After Insertion
    def fix_insert(self, node):
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right

                # Code is red - recolor required
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    # Node is right child - rotate left
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)

                    # Node is left child - rotate right and change color
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left

                # Uncle is red so recolor
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    # Node is left child so rotate right
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)

                    # Node is right child so rotate left and recolor
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)
        
        self.root.color = Color.BLACK
        # I think I did this right? This is complex and could probably be better.
        
def main():
    tree = RedBlackTree()
    values = []
    choice = 0
    
    while choice != -1:
        try:
            choice = int(input("Enter a value (-1 to quit): "))
        except:
            print("Error! Try again with a value.")
        
        if choice != -1:
            values.append(choice)
    
    for value in values:
        tree.insert(value)
        
    tree.in_order_traversal()
    
    choice = 0
        
    while choice != -1:
        try:
            choice = int(input("Enter a value to search for (-1 to quit): "))
        except:
            print("Error! Try again with a value.")
            
        result = tree.search(choice)
        
        if result:
            print(f"{result.value} was found!")
        else:
            print(f"{choice} not found!")
    
if __name__ == "__main__":
    main()
