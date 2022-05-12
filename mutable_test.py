import unittest
from hypothesis import given
import hypothesis.strategies as st
from mutable import *


class TestMutableList(unittest.TestCase):
    def test_insert(self):
        dict = Dict()
        dict.insert(3, 14)
        self.assertEqual(dict.avl.r.key, 3)
        self.assertEqual(dict.avl.r.data, 14)
        dict.insert("a", 10)
        dict.insert(1, 16)
        self.assertEqual(dict.avl.r.lchild.data, 16)

    def test_size(self):
        dict = Dict()
        dict.insert(1, 14)
        dict.insert(2, 10)
        dict.insert(3, 16)
        dict.insert("b", 20)
        self.assertEqual(dict.size(), 4)

    def test_to_list(self):
        dict = Dict()
        dict.insert(1, 15)
        dict.insert("ab", 20)
        dict.insert(2, 10)
        dict.insert(3, 16)
        self.assertEqual(dict._to_list(), [1, 15, "ab", 20, 2, 10, 3, 16])

    def test_find(self):
        dict = Dict()
        dict.insert(3, 14)
        dict.insert(2, 10)
        dict.insert(1, 16)
        dict.insert(5, 20)
        self.assertEqual(dict.find_by_key(1), 16)
        self.assertEqual(dict.find_by_key(6), False)

    def test_from_list(self):
        lst = [3, 14, 2, 10, 1, 16, 5, 20]
        dict = Dict().fromlist(lst)
        self.assertEqual(dict.avl.r.key, 3)
        self.assertEqual(dict.avl.r.lchild.data, 10)
        self.assertEqual(dict.avl.r.rchild.data, 20)

    def test_delete(self):
        dict = Dict()
        dict.insert("a", 14)
        dict.insert("ab", "dd")
        dict.insert("abc", 16)
        dict.insert("ddd", 20)
        dict.delete("ddd")
        self.assertEqual(dict.find_by_key("ddd"), False)
        self.assertEqual(dict.find_by_key("ab"), "dd")

    def test_filter_func_value(self):
        dict = Dict()
        dict.insert(3, 14)
        dict.insert(2, 10)
        dict.insert(1, 16)
        dict.insert(5, 20)

        def value_is_odd(x):
            return x % 2 == 1
        dict.filter_func(value_is_odd)
        self.assertEqual(dict.avl.r.key, 2)
        self.assertEqual(dict.avl.r.data, 10)

    def test_map_func(self):
        def square(x):
            return x ** 2
        dict = Dict()
        dict.insert(3, 14)
        dict.insert(2, 10)
        dict.insert(1, 16)
        dict.insert(5, 20)
        dict = dict.map_func(square)
        self.assertEqual(dict.avl.r.key, 9)
        self.assertEqual(dict.avl.r.data, 196)
        self.assertEqual(dict.avl.r.lchild.key, 4)
        self.assertEqual(dict.avl.r.lchild.data, 100)

    def test_reduce_func(self):
        def add(x, y):
            return x + y
        dict = Dict()
        dict.insert(3, 14)
        dict.insert(2, 10)
        dict.insert(1, 16)
        dict.insert(5, 20)
        sum = dict.reduce_func(add)
        self.assertEqual(sum, 71)

    def test_iter(self):
        list1 = [3, 14, 2, 10, 1, 16, 5, 20]
        dict = Dict().fromlist(list1)
        tmp = []
        for e in dict:
            tmp.append(e)
        self.assertEqual(list1, tmp)
        # test that the two iterators on one data structure should work in
        # parallel correctly
        i1 = dict.__iter__()
        i2 = dict.__iter__()
        self.assertEqual(next(i1), 3)
        self.assertEqual(next(i1), dict.find_by_key(3))
        self.assertEqual(next(i2), 3)
        self.assertEqual(next(i2), dict.find_by_key(3))
        self.assertEqual(next(i1), 2)

        self.assertEqual(dict._to_list(), tmp)
        dict.__iter__()
        ls = Dict()
        self.assertRaises(StopIteration, lambda: ls.next())

    def test_mempty(self):
        dict = Dict()
        dict.insert(3, None)
        dict.insert("a", 2)
        dict.insert(5, 6)
        self.assertEqual(dict.mempty().avl.r, None)

    def test_mconcat(self):
        dict = Dict()
        dict.insert(3, 14)
        dict.insert("1", 2)
        dict.insert(5, 6)
        dict1 = Dict()
        dict1.insert("abc", 16)
        dict.mconcat(dict1)
        self.assertEqual(dict.avl.r.key, 3)
        self.assertEqual(dict.avl.r.data, 14)
        self.assertEqual(dict.avl.r.rchild.key, 5)
        self.assertEqual(dict.avl.r.rchild.data, 6)
        self.assertEqual(dict.avl.r.lchild.key, "1")
        self.assertEqual(dict.avl.r.lchild.data, 2)
        self.assertEqual(dict.avl.r.rchild.rchild.key, "abc")

    def de_duplication(self, lst):
        for e in lst:
            count = 0
            for i in lst:
                if e[0] == i[0] and count == 0:
                    count = count + 1
                else:
                    lst.remove(i)
        return lst

    def sort_res(self, lst1):
        # lst1=[2,3,0,0,1,0,-1,5]
        if len(lst1) > 3:
            for i in range(0, len(lst1), 2):
                for j in range(2, len(lst1) - i - 2, 2):
                    if lst1[j] > lst1[j + 2]:
                        lst1[j], lst1[j + 2] = lst1[j + 2], lst1[j]
                        lst1[j + 1], lst1[j + 3] = lst1[j + 3], lst1[j + 1]
        return lst1

    def Datainitial(self, set1):  # solve the data of the PBT tests
        seen = set()
        set1 = self.de_duplication(set1)
        set1 = [e for e in set1 if tuple(
            e) not in seen and not seen.add(tuple(e))]
        return set1

    @given(st.lists(st.tuples(st.integers(), st.integers())))
    def test_from_list_to_list_equality(self, a):
        a = self.Datainitial(a)
        lst1 = []
        for i in a:
            if i[0] not in lst1:
                lst1.append(i[0])
                lst1.append(i[1])
        lst1 = self.sort_res(lst1)
        print(lst1)
        dict = Dict().fromlist(lst1)
        b = dict._to_list()
        self.assertEqual(lst1, b)

    @given(st.lists(st.tuples(st.integers(), st.integers())))
    def test_python_len_and_list_size_equlity(self, a):
        a = self.Datainitial(a)
        lst1 = []
        for i in a:
            if i[0] not in lst1:
                lst1.append(i[0])
                lst1.append(i[1])
        dict = Dict().fromlist(lst1)
        b = dict.size()
        self.assertEqual(len(lst1) / 2, b)

    @given(st.lists(st.tuples(st.integers(), st.integers())))
    def test_monoid_identity(self, a):
        a = self.Datainitial(a)
        lst1 = []
        for i in a:
            if i[0] not in lst1:
                lst1.append(i[0])
                lst1.append(i[1])
        dict = Dict().fromlist(lst1)
        dict_empty = dict.mempty()
        self.assertEqual(dict.mconcat(dict_empty), dict)
        self.assertEqual(dict_empty.mconcat(dict), dict)
        self.assertEqual(dict.mconcat(dict_empty), dict_empty.mconcat(dict))

    @given(st.lists(st.tuples(st.integers(), st.integers())),
           st.lists(st.tuples(st.integers(), st.integers())),
           st.lists(st.tuples(st.integers(), st.integers())))
    def test_monoid_associativity(self, a, a1, a2):
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
