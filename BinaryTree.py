from typing import TypeVar, List, Any, Type
from typing import Generic
from typing import List
from typing import Iterator
from typing import Callable
from typing import Generator
from typing import Union
from typing import Any
import collections
from collections.abc import Iterable

global res
res = []  # type: List
global count
T = TypeVar('T')
K = TypeVar('K', bound=Union[str, int, float])
D = TypeVar('D', bound=Union[None, str, int, float])
T12 = Union[K, D]


class BinaryNode(Generic[K]):  # The node of binary balanced tree
    # The construction method, the new nodes are all leaves, and the height is
    # 1
    obj_class: Type[K]

    def __init__(self, k: K, d: D):
        self.key = k  # key
        self.data = d  # value
        self.lchild = None  # left pointer
        self.rchild = None  # right pointer
        self.parent = None  # the parent of node
        self.key_sum = 0
        for i in str(self.key):
            self.key_sum = self.key_sum + ord(i)

    def __next__(self) -> 'BinaryNode':
        return self

    def __iter__(self) -> Iterator:
        return self


class BTree:  # The class of binary balanced tree
    def __init__(self):
        self.r = None  # the root node

    def insert(self, k: K, d: D):  # insert the node (k,d)
        self.r = self._insert(self.r, k, d)

    def _insert(self, p: Union[BinaryNode, None], k: K, d: D) -> \
            Union[BinaryNode, None]:
        # Called by the insert method
        child = BinaryNode(k, d)
        if isinstance(k, type(None)):
            raise TypeError("NoneType object is not iterable")
        elif p is None:  # Create root node when the tree is empty
            q = BinaryNode(k, d)
            return q
        elif isinstance(k, int) and isinstance(p.key, int):
            if child.key == p.key:
                p.data = d  # update data
                return p
            elif child.key < p.key:
                if not p.lchild:
                    p.lchild = child
                    child.parent = p
                else:
                    # insert (k,d) into the left subtree of p
                    p.lchild = self._insert(p.lchild, k, d)
            else:
                if not p.rchild:
                    p.rchild = child
                    child.parent = p
                else:
                    # insert (k,d) into the left subtree of p
                    p.rchild = self._insert(p.rchild, k, d)
        if isinstance(k, type("a")) or isinstance(p.key, str):
            if child.key_sum == p.key_sum:
                p.data = d  # update data
                return p
            elif child.key_sum < p.key_sum:
                if not p.lchild:
                    p.lchild = child
                    child.parent = p
                else:
                    # insert (k,d) into the left subtree of p
                    p.lchild = self._insert(p.lchild, k, d)
            else:
                if not p.rchild:
                    p.rchild = child
                    child.parent = p
                else:
                    # insert (k,d) into the left subtree of p
                    p.rchild = self._insert(p.rchild, k, d)
        return p

    def search_by_key(self, k: K):  # Find the node with key k in the AVL tree
        # r is the root node of the AVL tree
        return self._search_by_key(self.r, k)

    def _search_by_key(self, p: Union[BinaryNode, None], k: K) -> \
            Union[BinaryNode, None]:
        # Called by the search method
        k_key_sum = 0
        for i in str(k):
            k_key_sum = k_key_sum + ord(i)
        if p is None:
            return None  # An empty tree returns None
        elif p.key_sum == k_key_sum:
            return p.data  # Return p.data when found
        elif k_key_sum < p.key_sum:
            # Find recursively in left subtree
            return self._search_by_key(p.lchild, k)
        else:
            # Find recursively in the right subtree
            return self._search_by_key(p.rchild, k)

    def delete(self, k: K):  # delete node with key k
        self.r = self._delete(self.r, k)

    def _delete(self, p: Union[BinaryNode, None], k: K) -> \
            Union[BinaryNode, None]:
        # Called by delete to delete k nodes
        if p is None:
            return p
        if p.key == k:  # Find the node p with the key k
            # The case where node p has no subtree
            if p.lchild is None and p.rchild is None:
                p = None
                return p  # directly replace the node p with the right child
            # The case where node p has only right subtree
            elif p.rchild is None:
                p.lchild.parent = p.parent
                # p.lchild.ht=p.ht
                p = p.lchild
                p.lchild = None
                return p
            # The case where node p has only left subtree
            elif p.lchild is None:
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
        # p.ht = max(self.getht(p.lchild), self.getht(p.rchild)) + 1
        return p

    def inorder(self) -> List:  # Traverse all nodes in order
        global res
        res = []
        self._inorder(self.r)
        return res

    def _inorder(self, p: Union[BinaryNode, None]):
        # Called by the inorder method
        global res
        if p is not None:
            self._inorder(p.lchild)
            res.append([p.key, p.data])
            self._inorder(p.rchild)

    def size(self) -> int:  # Calculate the size of the tree
        global count
        count = 0
        self._size(self.r)
        return count

    def _size(self, p: Union[BinaryNode, None]):  # Called by the size method
        global count
        if p is not None:
            count = count + 1
            self._size(p.lchild)
            self._size(p.rchild)

    def to_list(self) -> List:  # Convert binary balanced tree to list
        global res
        res = []
        if self.r is not None:
            # res.append(self.r.key)
            # res.append(self.r.data)
            self._to_list(self.r)
        return res

    def _to_list(self, p: Union[BinaryNode, None]):
        # Called by the to_list method
        global res
        if p is not None:
            res.append(p.key)
            res.append(p.data)
            # res.append(BinaryNode(p.key,p.data))
            if p.lchild:
                self._to_list(p.lchild)
            if p.rchild:
                self._to_list(p.rchild)
