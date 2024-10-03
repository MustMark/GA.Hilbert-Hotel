class AVLTree:
    class AVLNode:
        def __init__(self, room_no, guest = None, left = None, right = None):
            self.room_no = room_no
            self.guest = None if guest is None else guest
            self.left = None if left is None else left
            self.right = None if right is None else right
            self.height = self.setHeight()

        def __str__(self):
            return "Room Number: " + str(self.room_no) + "\nGuest: " + str(self.guest)

        def setHeight(self):
                a = self.getHeight(self.left)
                b = self.getHeight(self.right)

                self.height = 1 + max(a,b)

                return self.height     

        def getHeight(self, node):
            return -1 if node == None else node.height

        def balanceValue(self):      
            return self.getHeight(self.right) - self.getHeight(self.left)
        

    def __init__(self, root = None):
        self.root = None if root is None else root

    def add(self, room_no, guest):
        room_no = int(room_no)
        if self.root == None:
            self.root = AVLTree.AVLNode(room_no, guest)
        else:
            self.root = AVLTree._add(self.root, room_no, guest)

    def _add(root, room_no, guest):
        if root is None:
            return AVLTree.AVLNode(room_no, guest)
        elif room_no < root.room_no:
            root.left = AVLTree._add(root.left, room_no, guest)
        else:
            root.right = AVLTree._add(root.right, room_no, guest)

        root.setHeight()
        balance = root.balanceValue()
        
        if balance > 1:
            if room_no < root.right.room_no:
                root.right = AVLTree.rotateRightChild(root.right)
            return AVLTree.rotateLeftChild(root)
        elif balance < -1:
            if room_no >= root.left.room_no:
                root.left = AVLTree.rotateLeftChild(root.left)
            return AVLTree.rotateRightChild(root)
        return root

    def rotateLeftChild(root):
        right = root.right
        if right == None:
            return root
        root.right = right.left
        right.left = root
        root.setHeight()
        right.setHeight()
        return right

    def rotateRightChild(root):
        left = root.left
        if left == None:
            return root
        root.left = left.right
        left.right = root
        root.setHeight()
        left.setHeight()
        return left

    def in_Order(self):
        print("AVLTree post-order : ", end="")
        AVLTree._in_Order(self.root)
        print()

    def _in_Order(root):
        if not root is None:
            AVLTree._in_Order(root.left)
            print(root)
            AVLTree._in_Order(root.right)

    def printTree(self):
        AVLTree._printTree(self.root)
        print()

    def _printTree(node , level=0):
        if not node is None:
            AVLTree._printTree(node.right, level + 1)
            print('     ' * level, node.room_no)
            AVLTree._printTree(node.left, level + 1)


hotel = AVLTree()

for i in range(1,10000):
    hotel.add(i, f"G{i}")

hotel.printTree()
hotel.in_Order()