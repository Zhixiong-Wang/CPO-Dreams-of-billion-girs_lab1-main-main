import unittest
from hypothesis import given
import hypothesis.strategies as st
from mutable import *
from typing import TypeVar, List, Any, Type
from typing import Generic
from typing import List
from typing import Iterator
from typing import Callable
from typing import Generator
from typing import Union
from typing import Optional
from typing import TypeGuard
from typing import Any
import collections
from collections.abc import Iterable


class TestMutableList(unittest.TestCase):
    def test_insert(self: 'TestMutableList') -> None:
        dict1 = Dict()
        dict1.insert(3, 14)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.avl.r.key, 3)
            self.assertEqual(dict1.avl.r.data, 14)
        dict1.insert("a", 10)
        dict1.insert(1, 16)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.avl.r.lchild.data, 16)

    def test_size(self: 'TestMutableList') -> None:
        dict1 = Dict()
        dict1.insert(1, 14)
        dict1.insert(2, 10)
        dict1.insert(3, 16)
        dict1.insert("b", 20)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.size(), 4)

    def test_to_list(self) -> None:
        dict1 = Dict()
        dict1.insert(1, 15)
        dict1.insert("ab", 20)
        dict1.insert(2, 10)
        dict1.insert(3, 16)
        if dict1.avl.r is not None:
            self.assertEqual(dict1._to_list(), [1, 15, "ab", 20, 2, 10, 3, 16])

    def test_find(self) -> None:
        dict1 = Dict()
        dict1.insert(3, 14)
        dict1.insert(2, 10)
        dict1.insert(1, 16)
        dict1.insert(5, 20)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.find_by_key(1), 16)
            self.assertEqual(dict1.find_by_key(6), False)

    def test_from_list(self) -> None:
        lst = [3, 14, 2, 10, 1, 16, 5, 20]
        dict1 = Dict().fromlist(lst)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.avl.r.key, 3)
            self.assertEqual(dict1.avl.r.lchild.data, 10)
            self.assertEqual(dict1.avl.r.rchild.data, 20)

    def test_delete(self) -> None:
        dict1 = Dict()
        dict1.insert("a", 14)
        dict1.insert("ab", "dd")
        dict1.insert("abc", 16)
        dict1.insert("ddd", 20)
        dict1.delete("ddd")
        if dict1.avl.r is not None:
            self.assertEqual(dict1.find_by_key("ddd"), False)
            self.assertEqual(dict1.find_by_key("ab"), "dd")

    def test_filter_func_value(self) -> None:
        dict1 = Dict()
        dict1.insert(3, 14)
        dict1.insert(2, 10)
        dict1.insert(1, 16)
        dict1.insert(5, 20)

        def value_is_odd(x: Any) -> TypeGuard[Any]:
            if type(x) is not bool:
                return x % 2 == 1

        dict1.filter_func(value_is_odd)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.avl.r.key, 2)
            self.assertEqual(dict1.avl.r.data, 10)

    def test_map_func(self) -> None:
        def square(x: Any) -> TypeGuard[Any]:
            return x ** 2

        dict1 = Dict()
        dict1.insert(3, 14)
        dict1.insert(2, 10)
        dict1.insert(1, 16)
        dict1.insert(5, 20)
        dict1 = dict1.map_func(square)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.avl.r.key, 9)
            self.assertEqual(dict1.avl.r.data, 196)
            self.assertEqual(dict1.avl.r.lchild.key, 4)
            self.assertEqual(dict1.avl.r.lchild.data, 100)

    def test_reduce_func(self) -> None:
        def add(x, y) -> Any:
            return x + y

        dict1 = Dict()
        dict1.insert(3, 14)
        dict1.insert(2, 10)
        dict1.insert(1, 16)
        dict1.insert(5, 20)
        sum = dict1.reduce_func(add)
        if dict1.avl.r is not None:
            self.assertEqual(sum, 71)

    def test_iter(self) -> None:
        list1 = [3, 14, 2, 10, 1, 16, 5, 20]
        dict1 = Dict().fromlist(list1)
        tmp = []
        for e in dict1:
            tmp.append(e)
        if dict1.avl.r is not None:
            self.assertEqual(list1, tmp)
        # test that the two iterators on one data structure should work in
        # parallel correctly
        i1 = dict1.__iter__()
        i2 = dict1.__iter__()
        if dict1.avl.r is not None:
            self.assertEqual(next(i1), 3)
            self.assertEqual(next(i1), dict1.find_by_key(3))
            self.assertEqual(next(i2), 3)
            self.assertEqual(next(i2), dict1.find_by_key(3))
            self.assertEqual(next(i1), 2)

            self.assertEqual(dict1._to_list(), tmp)
        dict1.__iter__()
        ls = Dict()
        if dict1.avl.r is not None:
            self.assertRaises(StopIteration, lambda: ls.next())

    def test_mempty(self) -> None:
        dict1 = Dict()
        dict1.insert(3, None)
        dict1.insert("a", 2)
        dict1.insert(5, 6)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.mempty().avl.r, None)

    def test_mconcat(self) -> None:
        dict1 = Dict()
        dict1.insert(3, 14)
        dict1.insert("1", 2)
        dict1.insert(5, 6)
        dict2 = Dict()
        dict2.insert("abc", 16)
        dict1.mconcat(dict2)
        if dict1.avl.r is not None:
            self.assertEqual(dict1.avl.r.key, 3)
            self.assertEqual(dict1.avl.r.data, 14)
            self.assertEqual(dict1.avl.r.rchild.key, 5)
            self.assertEqual(dict1.avl.r.rchild.data, 6)
            self.assertEqual(dict1.avl.r.lchild.key, "1")
            self.assertEqual(dict1.avl.r.lchild.data, 2)
            self.assertEqual(dict1.avl.r.rchild.rchild.key, "abc")

    def de_duplication(self, lst) -> Any:
        for e in lst:
            count = 0
            for i in lst:
                if e[0] == i[0] and count == 0:
                    count = count + 1
                else:
                    lst.remove(i)
        return lst

    @staticmethod
    def sort_res(lst1) -> Any:
        # lst1=[2,3,0,0,1,0,-1,5]
        if len(lst1) > 3:
            for i in range(0, len(lst1), 2):
                for j in range(2, len(lst1) - i - 2, 2):
                    if lst1[j] > lst1[j + 2]:
                        lst1[j], lst1[j + 2] = lst1[j + 2], lst1[j]
                        lst1[j + 1], lst1[j + 3] = lst1[j + 3], lst1[j + 1]
        return lst1

    def Datainitial(self, set1) -> List[Any]:
        # solve the data of the PBT tests
        seen = set()
        set1 = self.de_duplication(set1)
        set1 = [e for e in set1 if tuple(
            e) not in seen and not seen.add(tuple(e))]
        return set1

    @given(st.lists(st.tuples(st.integers(), st.integers())))
    def test_from_list_to_list_equality(self, a: List[Any]) -> None:
        a = self.Datainitial(a)
        lst1 = []
        for i in a:
            if i[0] not in lst1:
                lst1.append(i[0])
                lst1.append(i[1])
        lst1 = self.sort_res(lst1)
        print(lst1)
        dict1 = Dict().fromlist(lst1)
        b = dict1._to_list()
        self.assertEqual(lst1, b)

    @given(st.lists(st.tuples(st.integers(), st.integers())))
    def test_python_len_and_list_size_equlity(self, a: List[Any]) -> None:
        a = self.Datainitial(a)
        lst1 = []
        for i in a:
            if i[0] not in lst1:
                lst1.append(i[0])
                lst1.append(i[1])
        dict1 = Dict().fromlist(lst1)
        b = dict1.size()
        self.assertEqual(len(lst1) / 2, b)

    @given(st.lists(st.tuples(st.integers(), st.integers())))
    def test_monoid_identity(self, a: List[Any]) -> None:
        a = self.Datainitial(a)
        lst1 = []
        for i in a:
            if i[0] not in lst1:
                lst1.append(i[0])
                lst1.append(i[1])
        dict1 = Dict().fromlist(lst1)
        dict_empty = dict1.mempty()
        self.assertEqual(dict1.mconcat(dict_empty), dict1)
        self.assertEqual(dict_empty.mconcat(dict1), dict1)
        self.assertEqual(dict1.mconcat(dict_empty), dict_empty.mconcat(dict1))

    @given(st.lists(st.tuples(st.integers(), st.integers())),
           st.lists(st.tuples(st.integers(), st.integers())),
           st.lists(st.tuples(st.integers(), st.integers())))
    def test_monoid_associativity(self, a: List[Any], a1: List[Any],
                                  a2: List[Any]) -> None:
        a = self.Datainitial(a)
        a1 = self.Datainitial(a1)
        a2 = self.Datainitial(a2)
        lst1 = []
        lst2 = []
        lst3 = []
        for i in a:
            if i[0] not in lst1:
                lst1.append(i[0])
                lst1.append(i[1])
        for i in a1:
            if i[0] not in lst1:
                lst2.append(i[0])
                lst2.append(i[1])
        for i in a2:
            if i[0] not in lst1:
                lst3.append(i[0])
                lst3.append(i[1])
        dict1 = Dict().fromlist(lst1)
        dict2 = Dict().fromlist(lst2)
        dict3 = Dict().fromlist(lst3)
        self.assertEqual(
            dict1.mconcat(dict2).mconcat(dict3),
            dict1.mconcat(
                dict2.mconcat(dict3)))


if __name__ == '__main__':
    unittest.main()
