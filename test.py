import unittest
from rb_tree import RedBlackTree, RED, BLACK, NIL
class TestRedBlackTree(unittest.TestCase):
    def setUp(self):
        # Create a new Red-Black Tree for testing
        self.tree = RedBlackTree()
        print("we get here")

    def verify_rb_tree_properties(self, node):
        """
        Verify properties of the Red-Black Tree:
        - No two red nodes are adjacent.
        - All paths from the root to the leaves have the same black height.
        """
        def check_properties(node):
            if node == self.tree.NIL_LEAF:
                return 1  # Black height of NIL leaves

            left_black_height = check_properties(node.left)
            right_black_height = check_properties(node.right)

            # Check black height consistency
            if left_black_height != right_black_height:
                raise AssertionError("Black heights of left and right subtrees differ")

            # Check no two red nodes are adjacent
            if node.color == RED:
                if node.left.color == RED or node.right.color == RED:
                    raise AssertionError("Red node has red children")

            return left_black_height + (1 if node.color == BLACK else 0)

        # Start from root and verify properties
        if self.tree.root is not None:
            check_properties(self.tree.root)

    def test_insert_and_contains(self):
        self.tree.add(10)
        self.tree.add(20)
        self.tree.add(15)

        self.verify_rb_tree_properties(self.tree.root)

        self.assertTrue(self.tree.contains(10))
        self.assertTrue(self.tree.contains(20))
        self.assertTrue(self.tree.contains(15))
        self.assertFalse(self.tree.contains(25))

    def test_remove_leaf_node(self):
        self.tree.add(10)
        self.tree.add(20)
        self.tree.add(15)

        self.tree.remove(15)

        self.verify_rb_tree_properties(self.tree.root)

        self.assertFalse(self.tree.contains(15))
        self.assertTrue(self.tree.contains(10))
        self.assertTrue(self.tree.contains(20))

    def test_remove_node_with_one_child(self):
        self.tree.add(10)
        self.tree.add(20)
        self.tree.add(15)

        self.tree.remove(20)

        self.verify_rb_tree_properties(self.tree.root)

        self.assertFalse(self.tree.contains(20))
        self.assertTrue(self.tree.contains(10))
        self.assertTrue(self.tree.contains(15))

    def test_remove_node_with_two_children(self):
        self.tree.add(10)
        self.tree.add(20)
        self.tree.add(15)
        self.tree.add(25)
        self.tree.add(5)

        self.tree.remove(20)

        self.verify_rb_tree_properties(self.tree.root)

        self.assertFalse(self.tree.contains(20))
        self.assertTrue(self.tree.contains(10))
        self.assertTrue(self.tree.contains(15))
        self.assertTrue(self.tree.contains(25))
        self.assertTrue(self.tree.contains(5))

    def test_insert_duplicate(self):
        self.tree.add(10)
        self.tree.add(10)  # Insert duplicate

        # Verify the properties remain intact
        self.verify_rb_tree_properties(self.tree.root)

        # Check that the tree contains the value
        self.assertTrue(self.tree.contains(10))

    def test_remove_non_existent(self):
        self.tree.add(10)
        self.tree.add(20)

        self.tree.remove(15)  # Attempt to remove a non-existent node
        self.verify_rb_tree_properties(self.tree.root)

        # Check that the tree still contains existing nodes
        self.assertTrue(self.tree.contains(10))
        self.assertTrue(self.tree.contains(20))

    def test_stress_test_inserts(self):
        # Insert a large number of elements
        for i in range(100):
            self.tree.add(i)

        self.verify_rb_tree_properties(self.tree.root)

        # Check if all values are present
        for i in range(100):
            self.assertTrue(self.tree.contains(i))

    def test_stress_test_removals(self):
        for i in range(100):
            self.tree.add(i)

        for i in range(50):
            self.tree.remove(i)

        self.verify_rb_tree_properties(self.tree.root)

        # Ensure the removed values are not present
        for i in range(50):
            self.assertFalse(self.tree.contains(i))

        # Ensure the remaining values are still present
        for i in range(50, 100):
            self.assertTrue(self.tree.contains(i))

if __name__ == '__main__':
    unittest.main()
