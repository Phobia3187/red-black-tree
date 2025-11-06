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
        self.left = None
        self.right = None
        self.parent = None

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

        # Traverse the tree to find the correct insertion point like a BST.
        while current != self.EMPTY:
            parent = current
            if new_node.value < current.value:
                current = current.left
            else:
                current = current.right

        # Set the parent of the new node.
        new_node.parent = parent

        # If the tree was empty, the new node becomes the root.
        if parent is None:
            self.root = new_node
        # Otherwise, place the new node as the left or right child of the parent.
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
        # Declare new parent node.
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
        # The node's left child becomes the new parent of this subtree.
        new_parent = node.left

        # The new parent's right child is moved to become the old parent's left child.
        node.left = new_parent.right

        if new_parent.right != self.EMPTY:
            new_parent.right.parent = node

        # Link the new parent to the original node's parent.
        new_parent.parent = node.parent

        if node.parent is None:
            self.root = new_parent
        elif node == node.parent.right:
            node.parent.right = new_parent
        else:
            node.parent.left = new_parent

        # The old parent becomes the right child of the new parent.
        new_parent.right = node
        node.parent = new_parent
        # I would never copy and paste this from the other rotate function. :) - True

    # Search Tree
    def search(self, value):
        current = self.root

        # Pretty much BST search logic.
        while current != self.EMPTY:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right

        return None

    # Delete a node 
    def delete(self, value):
        node = self.search(value)

        # Remember original node color for fixing the delete
        originalNode = node
        originalColor = originalNode.color

        # Node has no left child or no children, Replace node with right child
        if node.left == self.EMPTY:
            newNode = node.right
            self._replaceSubtree(node, node.right)
        # Node has no right child, Replace with its left child
        elif node.right == self.EMPTY:
            newNode = node.left
            self._replaceSubtree(node, node.left)
        # Node has two children
        else:
            # Find the smallest node in the right subtree to replace node we delete
            originalNode = self._findMinimum(node.right)
            originalColor = originalNode.color
            newNode = originalNode.right
            
            # If smallest node is direct right child of original node
            if originalNode.parent == node:
                newNode.parent = originalNode
            else:
                self._replaceSubtree(originalNode, originalNode.right)
                originalNode.right = node.right
                originalNode.right.parent = originalNode

            # Replace deleted node with it successor
            self._replaceSubtree(node, originalNode)
            originalNode.left = node.left
            originalNode.left.parent = originalNode
            originalNode.color = node.color
            
        if originalColor == Color.BLACK:
            self._fixDelete(newNode)

    # Replace subtree helper for delete
    def _replaceSubtree(self, oldNode, newNode):
        if oldNode.parent is None:
            self.root = newNode
        elif oldNode == oldNode.parent.left:
            oldNode.parent.left = newNode  
        else:
            oldNode.parent.right = newNode
        newNode.parent = oldNode.parent
   
    # Find left most or lowest node of tree or subtree
    def _findMinimum(self, node):
        while node.left != self.EMPTY:
            node = node.left
            
        return node

    # Fix delete (fixes the node that replaced deleted node
    def _fixDelete(self, node):
        while node != self.root and node.color == Color.BLACK:
            # Node is a left child
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right

                # Sibling is black with two black children
                if sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
                    sibling.color = Color.RED
                    node = node.parent
                else:
                    # Sibling right child is black, left is red
                    if sibling.right.color == Color.BLACK:
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right  
                    # Sibling right child is red
                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK
                    self._left_rotate(node.parent)
                    node = self.root 
            else:
                # Node is a right child
                sibling = node.parent.left  # Get the sibling
            
                # Sibling is red
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left
                
                # Sibling is black with two black children
                if sibling.right.color == Color.BLACK and sibling.left.color == Color.BLACK:
                    sibling.color = Color.RED
                    node = node.parent
                else:
                    # Sibling left child is black, right is red
                    if sibling.left.color == Color.BLACK:
                        sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left
                    
                    # Sibling left child is red
                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK
                    self._right_rotate(node.parent)
                    node = self.root

        node.color = Color.BLACK

    
    
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
