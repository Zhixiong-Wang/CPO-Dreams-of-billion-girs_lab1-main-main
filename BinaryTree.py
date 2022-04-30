from typing import TypeVar
from typing import Generic
from typing import List
from typing import Iterator
from typing import Callable
from typing import Generator
from typing import Union
from typing import Any
import collections
from collections.abc import Iterable


class BinaryNode:  # The node of binary balanced tree
    # The construction method, the new nodes are all leaves, and the height is
    # 1
    def __init__(self, k, d):
        self.key = k  # key
        self.data = d  # value
        self.lchild = None  # left pointer
        self.rchild = None  # right pointer
        self.parent = None  # the parent of node
        self.ht = 1  # The height of the subtree of the current node
        self.key_sum = 0
        for i in str(self.key):
            self.key_sum = self.key_sum + ord(i)

    def __next__(self) -> 'BinaryNode':
        return self

    def __iter__(self) -> Iterator:
        return self


class BinaryTree:  # The class of binary balanced tree
    def __init__(self):
        self.r = None  # the root node

    def getht(self, p):  # return the height of subtree
        if p is None:
            return 0  # When the tree is empty the height of tree is 0
        return p.ht

    def insert(self, k, d):  # insert the node (k,d)
        self.r = self._insert(self.r, k, d)

    def _insert(self, p, k, d):  # Called by the insert method
        child = BinaryNode(k, d)
        if isinstance(k, type(None)):
            raise TypeError("NoneType object is not iterable")
            return p
        elif p is None:  # Create root node when the tree is empty
            q = BinaryNode(k, d)
            return q
        elif child.key_sum == p.key_sum:
            p.data = d  # update data
            return p
        elif child.key_sum < p.key_sum:  # The case of k<p.key
            if not p.lchild:
                p.lchild = child
                child.parent = p
            else:
                # insert (k,d) into the left subtree of p
                p.lchild = self._insert(p.lchild, k, d)
        else:  # The case of k>p.key
            if not p.rchild:
                p.rchild = child
                child.parent = p
            else:
                # insert (k,d) into the left subtree of p
                p.rchild = self._insert(p.rchild, k, d)
        p.ht = max(
            self.getht(
                p.lchild), self.getht(
                p.rchild)) + 1  # update the height of node p
        return p

    def search_by_key(self, k):  # Find the node with key k in the AVL tree
        # r is the root node of the AVL tree
        return self._search_by_key(self.r, k)

    def _search_by_key(self, p, k):  # Called by the search method
        if p is None:
            return None  # An empty tree returns None
        if p.key == k:
            return p.data  # Return p.data when found
        if k < p.key:
            # Find recursively in left subtree
            return self._search_by_key(p.lchild, k)
        else:
            # Find recursively in the right subtree
            return self._search_by_key(p.rchild, k)

    def delete(self, k):  # delete node with key k
        self.r = self._delete(self.r, k)

    def _delete(self, p, k):  # Called by delete to delete k nodes
        if p is None:
            return p
        if p.key == k:  # Find the node p with the key k
            if p.lchild is None and p.rchild is None:
                # The case where node p has no subtree
                p = None
                return p  # directly replace the node p with the right child
            elif p.rchild is None:
                # The case where node p has only right subtree
                p.lchild.parent = p.parent
                p.lchild.ht = p.ht
                p = p.lchild
                p.lchild = None
                return p
            elif p.lchild is None:
                # The case where node p has only left subtree
                p.rchild.parent = p.parent
                p = p.rchild
                p.rchild = None
                return p  # directly replace the node p with the left child
            else:  # The case where node p has both left and right subtrees
                p.lchild.parent = p.parent
                p.lchild.rchild = p.rchild
                p = p.lchild
                p.lchild = None
                return p
        # The case of k<p.key
        elif k < p.key:
            # Delete the node with keyword k in the left subtree
            p.lchild = self._delete(p.lchild, k)
        elif k > p.key:  # The case of k>p.key
            # Delete the node with keyword k in the right subtree
            p.rchild = self._delete(p.rchild, k)
        # update the height of node p
        p.ht = max(self.getht(p.lchild), self.getht(p.rchild)) + 1
        return p

    def inorder(self):  # Traverse all nodes in order
        global res
        res = []
        self._inorder(self.r)
        return res

    def _inorder(self, p):  # Called by the inorder method
        global res
        if p is not None:
            self._inorder(p.lchild)
            res.append([p.key, p.data])
            self._inorder(p.rchild)

    def size(self):  # Calculate the size of the tree
        global count
        count = 0
        self._size(self.r)
        return count

    def _size(self, p):  # Called by the size method
        global count
        if p is not None:
            count = count + 1
            self._size(p.lchild)
            self._size(p.rchild)

    def to_list(self):  # Convert binary balanced tree to list
        global res
        res = []
        self._to_list(self.r)
        return res

    def _to_list(self, p):  # Called by the to_list method
        global res
        if p is not None:
            res.append(p.key)
            res.append(p.data)
            if p.lchild:
                self._to_list(p.lchild)
            if p.rchild:
                self._to_list(p.rchild)
