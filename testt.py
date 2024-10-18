class AVLTree:
    class AVLNode:
        def __init__(self, room_no, guest=None):
            self.room_no = room_no
            self.guest = guest
            self.left = None
            self.right = None
            self.height = 1

        def __str__(self):
            return f"{self.room_no} : {self.guest}"

        def setHeight(self):
            self.height = 1 + max(self.getHeight(self.left), self.getHeight(self.right))

        def getHeight(self, node):
            return 0 if node is None else node.height

        def balanceValue(self):
            return self.getHeight(self.right) - self.getHeight(self.left)

    def __init__(self):
        self.root = None

    def add(self, room_no, guest):
        self.root = self._add(self.root, room_no, guest)

    def _add(self, node, room_no, guest):
        if node is None:
            return self.AVLNode(room_no, guest)
        if room_no < node.room_no:
            node.left = self._add(node.left, room_no, guest)
        else:
            node.right = self._add(node.right, room_no, guest)

        node.setHeight()
        return self._rebalance(node, room_no)

    def _rebalance(self, node, room_no):
        balance = node.balanceValue()

        if balance > 1:
            if room_no < node.right.room_no:
                node.right = self.rotateRightChild(node.right)
            return self.rotateLeftChild(node)

        if balance < -1:
            if room_no >= node.left.room_no:
                node.left = self.rotateLeftChild(node.left)
            return self.rotateRightChild(node)

        return node

    def rotateLeftChild(self, root):
        right = root.right
        root.right = right.left
        right.left = root

        root.setHeight()
        right.setHeight()

        return right

    def rotateRightChild(self, root):
        left = root.left
        root.left = left.right
        left.right = root

        root.setHeight()
        left.setHeight()

        return left

    def delete(self, room_no):
        self.root, deleted = self._delete(self.root, room_no)
        return deleted

    def _delete(self, node, room_no):
        if node is None:
            return node, False

        if room_no < node.room_no:
            node.left, deleted = self._delete(node.left, room_no)
        elif room_no > node.room_no:
            node.right, deleted = self._delete(node.right, room_no)
        else:
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            temp = self._get_min_value_node(node.right)
            node.room_no, node.guest = temp.room_no, temp.guest
            node.right, _ = self._delete(node.right, temp.room_no)
            deleted = True

        node.setHeight()
        return self._rebalance(node, room_no), deleted

    def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, room_no):
        return self._search(self.root, room_no)

    def _search(self, node, room_no):
        if node is None or node.room_no == room_no:
            return node
        if room_no < node.room_no:
            return self._search(node.left, room_no)
        return self._search(node.right, room_no)

    def in_order(self):
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node is not None:
            self._in_order(node.left, result)
            result.append(node.guest)
            self._in_order(node.right, result)

    def inorder_traversal(self, root):
        if root is None:
            return []
        return (
            self.inorder_traversal(root.left)
            + [root.guest]
            + self.inorder_traversal(root.right)
        )
    
    def printTree(self):
        self._printTree(self.root, 0)

    def _printTree(self, node, level=0):
        if node is not None:
            self._printTree(node.right, level + 1)
            print('     ' * level + str(node.room_no))
            self._printTree(node.left, level + 1)


import time

avl = AVLTree()

for i in range(100000):
    avl.add(i, "A")


# Measure time for in_order
start_time = time.time()
avl.in_order()  # This prints the result during traversal
in_order_time = time.time() - start_time
print(f"in_order runtime: {in_order_time} seconds")

# Measure time for inorder_traversal
start_time = time.time()
result = avl.inorder_traversal(avl.root)  # This returns the result
inorder_traversal_time = time.time() - start_time
print(f"inorder_traversal runtime: {inorder_traversal_time} seconds")