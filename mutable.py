import BinaryTree
from BinaryTree import BTree
from typing import TypeVar
from typing import Generic
from typing import List
from typing import Iterator
from typing import Callable
from typing import Generator
from typing import Union
from typing import Any
from functools import reduce


class AVLNode:
    def __init__(self, k, d):
        self.key = k
        self.data = d
        self.lchild = None
        self.rchild = None
        self.ht = 1


class Dict:
    def __init__(self):
        self.avl = BTree()

    def insert(self, k, d):  # insert a node to tree
        self.avl.insert(k, d)

    def delete(self, k):
        self.avl.delete(k)

    def inorder(self):  # Traverse the tree in inorder
        return self.avl.inorder()

    def find_by_key(self, k):  # find the node by key
        if self.avl.search_by_key(k) is None:
            return False
        else:
            return self.avl.search_by_key(k)

    def __getitem__(self, k):
        return self.avl.search(k)

    def __setitem__(self, k, d):
        self.avl.insert(k, d)

    def size(self) -> int:   # calculate the size of tree
        return self.avl.size()

    def _to_list(self) -> List:
        if self.avl.r is None:
            return []
        else:
            return self.avl.to_list()

    def fromlist(self, lst):  # Convert list to binary balanced tree
        if len(lst) == 0:
            return None
        elif len(lst) % 2 == 1:
            return False
        else:
            for i in range(0, len(lst), 2):
                self.avl.insert(lst[i], lst[i + 1])
            return self

    def filter_func(self, func: Callable):
        list = self._to_list()
        newlist = filter(func, list)
        for i in newlist:
            self.delete(i)

    def map_func(self, func: Callable):
        tolist = self._to_list()
        newlist = list(map(func, tolist))
        dict = Dict()
        for i in range(0, len(newlist), 2):
            dict.avl.insert(newlist[i], newlist[i + 1])
        return dict

    def reduce_func(self, func: Callable):
        list = self._to_list()
        sum = reduce(func, list)
        return sum

    def __iter__(self) -> Iterator:
        return iter(self._to_list())

    def next(self) -> Iterator[Any]:
        if self.avl.r is None:
            raise StopIteration
        else:
            return iter(self._to_list())

    def mempty(self) -> 'Dict':
        self.avl.r = None
        return self

    def mconcat(self, k, d) -> 'Dict':
        a = Dict()
        a.insert(k, d)
        if self.avl.r is None:
            return a
        elif a.avl.r is None:
            return self
        else:
            ls1 = a._to_list()
            for i in range(0, len(ls1), 2):
                self.insert(ls1[i], ls1[i + 1])
            return self
