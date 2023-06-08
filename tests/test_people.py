import unittest
import people as pl
from digikamdb import Digikam
import os

class TestPeople(unittest.TestCase):
    def setUp(self):
        self.dk = Digikam('sqlite:///' + 'tests\\testdata\\testdata.db')
        self.max_m = pl.Person(3, "Max Mustermann", 42)
        self.sabine_m = pl.Person(5, "Sabine Mustermann", 23)
        self.musterpeople = pl.People('dk_muster')
        self.musterpeople.add_person(self.max_m)
        self.musterpeople.add_person(self.sabine_m)

    def test_add_get_person(self):
        musterpeople = pl.People(self.dk)
        musterpeople.add_person(self.max_m)
        musterpeople.add_person(self.sabine_m)
        result = [self.musterpeople.get_person(3), self.musterpeople.get_person(5)]
        self.assertEqual(result, [self.max_m, self.sabine_m])

    def test_iterable(self):
        result = [p for p in self.musterpeople]
        self.assertEqual(result, [self.max_m, self.sabine_m])

    def test_len(self):
        result = len(self.musterpeople)
        self.assertEqual(result, 2)

    def test_getitem(self):
        result = [self.musterpeople[3], self.musterpeople[5]]
        self.assertEqual(result, [self.max_m, self.sabine_m])

    def test_get_by_index(self):
        result = [self.musterpeople.get_by_index(0), self.musterpeople.get_by_index(1)]
        self.assertEqual(result, [self.max_m, self.sabine_m])


class TestPerson(unittest.TestCase):
    def test_connections(self):
        mustermann = pl.Person(1, "Max Mustermann", 42)
        mustermann.add_connection(2, 10)
        mustermann.add_connection(3, 5)
        result = mustermann.get_connections()
        self.assertEqual(result, {2: 10, 3: 5})


if __name__ == '__main__':
    unittest.main()