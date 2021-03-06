"""
Implementation of an auto-balanced binary tree!
For doctests run following command:
python3 -m doctest -v avl_tree.py
For testing run:
python avl_tree.py
"""

import math
import random
import unittest
from typing import Any


class my_queue:
    def __init__(self) -> None:
        self.data = []
        self.head = 0
        self.tail = 0

    def is_empty(self) -> bool:
        return self.head == self.tail

    def push(self, data: Any) -> None:
        self.data.append(data)
        self.tail = self.tail + 1

    def pop(self) -> Any:
        ret = self.data[self.head]
        self.head = self.head + 1
        return ret

    def count(self) -> int:
        return self.tail - self.head

    def print(self) -> None:
        print(self.data)
        print("**************")
        print(self.data[self.head : self.tail])


class my_node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

    def get_data(self) -> Any:
        return self.data

    def get_left(self) -> "my_node":
        return self.left

    def get_right(self) -> "my_node":
        return self.right

    def get_height(self) -> int:
        return self.height

    def set_data(self, data: Any) -> None:
        self.data = data
        return

    def set_left(self, node: "my_node") -> None:
        self.left = node
        return

    def set_right(self, node: "my_node") -> None:
        self.right = node
        return

    def set_height(self, height: int) -> None:
        self.height = height
        return


def get_height(node: "my_node") -> int:
    if node is None:
        return 0
    return node.get_height()


def my_max(a: Any, b: Any) -> Any:
    if a > b:
        return a
    return b


def right_rotation(node: "my_node") -> "my_node":
    r"""
            A                      B
           / \                    / \
          B   C                  Bl  A
         / \       -->          /   / \
        Bl  Br                 UB Br  C
       /
     UB
    UB = unbalanced node
    """
    print("left rotation node:", node.get_data())
    ret = node.get_left()
    node.set_left(ret.get_right())
    ret.set_right(node)
    h1 = my_max(get_height(node.get_right()), get_height(node.get_left())) + 1
    node.set_height(h1)
    h2 = my_max(get_height(ret.get_right()), get_height(ret.get_left())) + 1
    ret.set_height(h2)
    return ret


def left_rotation(node: "my_node") -> "my_node":
    """
    a mirror symmetry rotation of the left_rotation
    """
    print("right rotation node:", node.get_data())
    ret = node.get_right()
    node.set_right(ret.get_left())
    ret.set_left(node)
    h1 = my_max(get_height(node.get_right()), get_height(node.get_left())) + 1
    node.set_height(h1)
    h2 = my_max(get_height(ret.get_right()), get_height(ret.get_left())) + 1
    ret.set_height(h2)
    return ret


def lr_rotation(node: "my_node") -> "my_node":
    r"""
            A              A                    Br
           / \            / \                  /  \
          B   C    LR    Br  C       RR       B    A
         / \       -->  /  \         -->    /     / \
        Bl  Br         B   UB              Bl    UB  C
             \        /
             UB     Bl
    RR = right_rotation   LR = left_rotation
    """
    node.set_left(left_rotation(node.get_left()))
    return right_rotation(node)


def rl_rotation(node: "my_node") -> "my_node":
    node.set_right(right_rotation(node.get_right()))
    return left_rotation(node)


def insert_node(node: "my_node", data: Any) -> "my_node":
    if node is None:
        return my_node(data)
    if data < node.get_data():
        node.set_left(insert_node(node.get_left(), data))
        if (
            get_height(node.get_left()) - get_height(node.get_right()) == 2
        ):  # an unbalance detected
            if (
                data < node.get_left().get_data()
            ):  # new node is the left child of the left child
                node = right_rotation(node)
            else:
                node = lr_rotation(node)
    else:
        node.set_right(insert_node(node.get_right(), data))
        if get_height(node.get_right()) - get_height(node.get_left()) == 2:
            if data < node.get_right().get_data():
                node = rl_rotation(node)
            else:
                node = left_rotation(node)
    h1 = my_max(get_height(node.get_right()), get_height(node.get_left())) + 1
    node.set_height(h1)
    return node


def get_rightMost(root: "my_node") -> "my_node":
    while root.get_right() is not None:
        root = root.get_right()
    return root.get_data()


def get_leftMost(root: "my_node") -> "my_node":
    while root.get_left() is not None:
        root = root.get_left()
    return root.get_data()


def del_node(root: "my_node", data: Any) -> "my_node":
    if root.get_data() == data:
        if root.get_left() is not None and root.get_right() is not None:
            temp_data = get_leftMost(root.get_right())
            root.set_data(temp_data)
            root.set_right(del_node(root.get_right(), temp_data))
        elif root.get_left() is not None:
            root = root.get_left()
        else:
            root = root.get_right()
    elif root.get_data() > data:
        if root.get_left() is None:
            print("No such data")
            return root
        else:
            root.set_left(del_node(root.get_left(), data))
    elif root.get_data() < data:
        if root.get_right() is None:
            return root
        else:
            root.set_right(del_node(root.get_right(), data))
    if root is None:
        return root
    if get_height(root.get_right()) - get_height(root.get_left()) == 2:
        if get_height(root.get_right().get_right()) >= get_height(
            root.get_right().get_left()
        ):
            root = left_rotation(root)
        else:
            root = rl_rotation(root)
    elif get_height(root.get_right()) - get_height(root.get_left()) == -2:
        if get_height(root.get_left().get_left()) >= get_height(
            root.get_left().get_right()
        ):
            root = right_rotation(root)
        else:
            root = lr_rotation(root)
    height = my_max(get_height(root.get_right()), get_height(root.get_left())) + 1
    root.set_height(height)
    return root


class AVLtree:
    """
    An AVL tree doctest
    Examples:
    >>> t = AVLtree()
    >>> t.insert(4)
    insert:4
    >>> print(str(t).replace(" \\n","\\n"))
     4
    *************************************
    >>> t.insert(2)
    insert:2
    >>> print(str(t).replace(" \\n","\\n").replace(" \\n","\\n"))
      4
     2  *
    *************************************
    >>> t.insert(3)
    insert:3
    right rotation node: 2
    left rotation node: 4
    >>> print(str(t).replace(" \\n","\\n").replace(" \\n","\\n"))
      3
     2  4
    *************************************
    >>> t.get_height()
    2
    >>> t.del_node(3)
    delete:3
    >>> print(str(t).replace(" \\n","\\n").replace(" \\n","\\n"))
      4
     2  *
    *************************************
    """

    def __init__(self) -> None:
        self.root = None

    def get_height(self) -> int:
        return get_height(self.root)

    def insert(self, data: Any) -> None:
        print("insert:" + str(data))
        self.root = insert_node(self.root, data)

    def del_node(self, data: Any) -> None:
        print("delete:" + str(data))
        if self.root is None:
            print("Tree is empty!")
            return
        self.root = del_node(self.root, data)

    def __str__(self) -> str:
        """
        A level traversale, gives a more intuitive look on the tree
        """
        output = ""
        q = my_queue()
        q.push(self.root)
        layer = self.get_height()
        if layer == 0:
            return output
        cnt = 0
        while not q.is_empty():
            node = q.pop()
            space = " " * int(math.pow(2, layer - 1))
            output += space
            if node is None:
                output += "*"
                q.push(None)
                q.push(None)
            else:
                output += str(node.get_data())
                q.push(node.get_left())
                q.push(node.get_right())
            output += space
            cnt = cnt + 1
            for i in range(100):
                if cnt == math.pow(2, i) - 1:
                    layer = layer - 1
                    if layer == 0:
                        output += "\n*************************************"
                        return output
                    output += "\n"
                    break
        output += "\n*************************************"
        return output


class Test(unittest.TestCase):
    def _is_balance(self, avl: AVLtree):
        if avl.root is None:
            return True
        dfs = [avl.root]
        while dfs:
            now = dfs.pop()
            if now.left:
                left_height = now.left.height
                dfs.append(now.left)
            else:
                left_height = 0
            if now.right:
                right_height = now.right.height
                dfs.append(now.right)
            else:
                right_height = 0
            if abs(left_height - right_height) > 1:
                return False
        return True

    def test_delete(self):
        avl = AVLtree()
        for i in [8, 7, 4, 3, 9, 10, 11, 13, 6, 0, 2, 12, 1, 14, 5]:
            avl.insert(i)
            self.assertTrue(self._is_balance(avl))

        for v in [8, 7, 4, 3, 9, 10, 11, 13, 6, 0, 2, 12, 1, 14, 5]:
            avl.del_node(v)
            print(avl)
            self.assertTrue(self._is_balance(avl))

    def test_delete_random(self):
        avl = AVLtree()
        random.seed(0)
        values = list(range(1000))
        random.shuffle(values)
        for i in values:
            avl.insert(i)
            self.assertTrue(self._is_balance(avl))
        random.shuffle(values)
        for i in values:
            avl.del_node(i)
            self.assertTrue(self._is_balance(avl))


if __name__ == "__main__":
    unittest.main()
