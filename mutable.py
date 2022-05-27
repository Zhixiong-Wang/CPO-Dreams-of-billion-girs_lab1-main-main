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

T = TypeVar('T')
K = TypeVar('K', bound=Union[str, int, float])
D = TypeVar('D', bound=Union[None, str, int, float])
T12 = Union[K, D]


class BinaryNode:  # The node of binary balanced tree
    # The construction method, the new nodes are all leaves, and the height is
    # 1
    def __init__(self, k: K, d: D):
        self.key = k  # key
        self.data = d  # value
        self.lchild = None  # left pointer
        self.rchild = None  # right pointer
        self.parent = None  # the parent of node
        # self.ht = 1  # The height of the subtree of the current node
        self.key_sum = 0
        for i in str(self.key):
            self.key_sum = self.key_sum + ord(i)

    def __next__(self) -> 'BinaryNode':
        return self

    def __iter__(self) -> Iterator:
        return self


class Dict:
    def __init__(self):
        self.avl = BTree()

    def insert(self, k: K, d: D) -> None:  # insert a node to tree
        self.avl.insert(k, d)

    def delete(self, k) -> None:
        self.avl.delete(k)

    def inorder(self) -> List:  # Traverse the tree in inorder
        return self.avl.inorder()

    def find_by_key(self, k: K) -> Union[None, False]:  # find the node by key
        if self.avl.search_by_key(k) is None:
            return False
        else:
            return self.avl.search_by_key(k)

    def size(self) -> int:  # calculate the size of tree
        return self.avl.size()

    def _to_list(self) -> List:
        if self.avl.r is None:
            return []
        else:
            return self.avl.to_list()

    def fromlist(self, lst) -> 'Dict':  # Convert list to binary balanced tree
        if len(lst) == 0:
            return self
        elif len(lst) % 2 == 1:
            return self
        else:
            for i in range(0, len(lst), 2):
                self.avl.insert(lst[i], lst[i + 1])
            return self

    def filter_func(self, func: Callable) -> None:
        list1 = self._to_list()
        newlist = filter(func, list1)
        for i in newlist:
            self.delete(i)

    def map_func(self, func: Callable) -> 'Dict':
        tolist = self._to_list()
        newlist = list(map(func, tolist))
        dict = Dict()
        for i in range(0, len(newlist), 2):
            dict.avl.insert(newlist[i], newlist[i + 1])
        return dict

    def reduce_func(self, func: Callable) -> 'K':
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

    def mconcat(self, a: 'Dict') -> 'Dict':
        if self.avl.r is None:
            return a
        elif a.avl.r is None:
            return self
        else:
            if self.avl.r.key_sum < a.avl.r.key_sum:
                ls1 = a._to_list()
                for i in range(0, len(ls1), 2):
                    self.insert(ls1[i], ls1[i + 1])
                return self
            elif self.avl.r.key_sum >= a.avl.r.key_sum:
                ls1 = self._to_list()
                for i in range(0, len(ls1), 2):
                    a.insert(ls1[i], ls1[i + 1])
                return a
