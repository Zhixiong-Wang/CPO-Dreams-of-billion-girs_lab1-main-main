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
        self.assertEqual(dict._to_list(), [1, 15, 'ab', 20, 2, 10, 3, 16])

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
        dict.insert(3, 14)
        dict.insert(2, 10)
        dict.insert(1, 16)
        dict.insert(5, 20)
        dict.delete(5)
        self.assertEqual(dict.find_by_key(5), False)
        # self.assertEqual(dict.find(3), 16)

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
        def add(x,y):
            return x+y
        dict = Dict()
        dict.insert(3, 14)
        dict.insert(2, 10)
        dict.insert(1, 16)
        dict.insert(5, 20)
        sum=dict.reduce_func(add)
        self.assertEqual(sum, 71)

    def test_iter(self):
        list = [3,14,2,10,1,16,5,20]
        dict = Dict().fromlist(list)
        tmp = []
        for e in dict:
            tmp.append(e)
        self.assertEqual(list, tmp)
        # test that the two iterators on one data structure should work in parallel correctly
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
        dict=Dict()
        dict.insert(3, None)
        dict.insert("a", 2)
        dict.insert(5, 6)
        self.assertEqual(dict.mempty().avl.r, None)

    def test_mconcat(self):
        dict = Dict()
        dict.insert(3, 14)
        dict.insert("1", 2)
        dict.insert(5, 6)
        dict = dict.mconcat("abc", 6)
        self.assertEqual(dict.avl.r.key, 3)
        self.assertEqual(dict.avl.r.data, 14)
        self.assertEqual(dict.avl.r.rchild.key, 5)
        self.assertEqual(dict.avl.r.rchild.data, 6)
        self.assertEqual(dict.avl.r.lchild.key, "1")
        self.assertEqual(dict.avl.r.lchild.data, 2)
        self.assertEqual(dict.avl.r.rchild.rchild.key, "abc")



if __name__ == '__main__':
    unittest.main()
