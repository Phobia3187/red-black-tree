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
        # The nodes right child becomes the new parent of this subtree
        new_parent = node.right

        # The new parents left child is moved to become the old parents right child
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
        # Find the node to delete
        node_to_delete = self.search(value)
        # Check if node is None or sentinel
        if node_to_delete is None or node_to_delete == self.EMPTY:
            return
            
        # Remember removed node color for fixing the delete
        node_removed = node_to_delete
        removed_color = node_removed.color

        # Node has no left child so replace right child
        if node_to_delete.left == self.EMPTY:
            replacement_node = node_to_delete.right
            self.replaceSubtree(node_to_delete, node_to_delete.right)
        # Node has no right child so replace with its left child
        elif node_to_delete.right == self.EMPTY:
            replacement_node = node_to_delete.left
            self.replaceSubtree(node_to_delete, node_to_delete.left)
        
        # Node has two children
        else:
            # Find smallest node in right subtree to replace deleted node
            node_removed = self.findMinimum(node_to_delete.right)
            removed_color = node_removed.color
            replacement_node = node_removed.right
            
            # If smallest node is direct right child of node_to_delete
            if node_removed.parent == node_to_delete:
                replacement_node.parent = node_removed
            # Smallest node is not direct child, but is grandchild or further
            else:
                self.replaceSubtree(node_removed, node_removed.right)
                node_removed.right = node_to_delete.right
                node_removed.right.parent = node_removed

            # Replace deleted node with it successor
            self.replaceSubtree(node_to_delete, node_removed)
            node_removed.left = node_to_delete.left
            node_removed.left.parent = node_removed
            node_removed.color = node_to_delete.color

        # Removed node was balck so fix violations    
        if  removed_color == Color.BLACK:
            self.fix_delete(replacement_node)

    # Replace subtree helper for delete
    def replaceSubtree(self, old_node,  replacement_node):
        if old_node.parent is None:
            self.root = replacement_node
        elif old_node == old_node.parent.left:
            old_node.parent.left =   replacement_node  
        else:
            old_node.parent.right =  replacement_node
        if  replacement_node != self.EMPTY:
            replacement_node.parent = old_node.parent
   
    # Find left most or lowest node of tree or subtree
    def findMinimum(self, node):
        current = node
        while current.left != self.EMPTY:
            current = current.left            
        return current

    # Fix delete, fix the red black properteis after deleteing Black node
    def fix_delete(self, node):
    # Loop until reaching root or node becomes red
        while node != self.root and node.color == Color.BLACK:
            
            # Left side fixing aka node is a left child
            if node == node.parent.left:
                sibling = node.parent.right

                # Sibling is red so rotate and recolor so sibling is black
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self.left_rotate(node.parent)
                    sibling = node.parent.right  
                
                # Sibling is black with two black children so color sibling red and move up  
                if (sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK):
                    sibling.color = Color.RED
                    node = node.parent  
                
                else:
                    
                    # Sibling is black, right child black, left child red
                    # Rotate sibling to make outer child red
                    if sibling.right.color == Color.BLACK:
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self.right_rotate(sibling)
                        sibling = node.parent.right  

                    # Sibling is black with red right child
                    # Rotate and recolor to fix black height property
                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK
                    self.left_rotate(node.parent)
                    node = self.root 
            
            # Right side fixing aka node is right child (opposite of above fixes)
            else:
                sibling = node.parent.left
                
                # Sibling is red so rotate and recolor so sibling is black
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    node.parent.color = Color.RED
                    self.right_rotate(node.parent)
                    sibling = node.parent.left
                
                # Sibling is black with two black children so color sibling red and move up 
                if (sibling.right.color == Color.BLACK and 
                    sibling.left.color == Color.BLACK):
                    sibling.color = Color.RED
                    node = node.parent
                
                else:
                    # Sibling is black with left child black, right child red
                    # Rotate sibling to make outer child red
                    if sibling.left.color == Color.BLACK:
                        sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    
                    # Sibling is black with red left child
                    sibling.color = node.parent.color
                    node.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK
                    self.right_rotate(node.parent)
                    node = self.root
        
        # Make sure node is black
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
    
    print("   RED BLACK Tree Menu   ")
    print("1. Insert a value")
    print("2. Display Tree (in order traversal)")
    print("3. Search for a value")
    print("4. Delete a value")
    print("5. Exit the program")

    while True:
        try:
            choice = int(input("\nEnter a choice (1-5): "))
        except: 
            print("Please enter a valid number.")
            continue
        if choice == 1:
            print("\nType the values you want to insert (-1 to quit):")
            while True:
                try:
                    value = int(input("Enter a value: "))
                    if value == -1:
                        break
                    tree.insert(value)
                    print(f"{value} was inserted")
                except:
                    print("Please enter a valid integer.")
        elif choice == 2:
            print("\nIn order traversal of RB Tree: ")
            tree.in_order_traversal()
        elif choice == 3:
            try:
                value = int(input("\nType a value to search for: "))
                result = tree.search(value)
                if result:
                    print(f"{value} has been found. Color: {result.color}")
                else:
                    print(f"{value} was not found in tree")
            except:
                print("Please enter a valid integer.")
        elif choice == 4:
            try:
                value = int(input("\nType a value to delete: "))
                result = tree.search(value)
                if result:
                    tree.delete(value)
                    print(f"{value} has been deleted")
                else:
                    print(f"{value} was not found in tree")
            except:
                print("Please enter a valid integer.")
        elif choice == 5:
            print("Exiting Red Black Tree")
            break
        else:
            print("Please enter a numbmer between 1 and 5.")

if __name__ == "__main__":
    main()
