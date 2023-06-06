import unittest
import people as pl
from digikamdb import Digikam

class TestPeople(unittest.TestCase):
    def setUp(self):
        self.max_m = pl.Person(3, "Max Mustermann", 42)
        self.sabine_m = pl.Person(5, "Sabine Mustermann", 23)
        self.people = pl.People('dk_placeholder')
        self.people.add_person(self.max_m)
        self.people.add_person(self.sabine_m)

    
    def test_add_get_person(self):
        people = pl.People('dk_placeholder')
        people.add_person(self.max_m)
        people.add_person(self.sabine_m)
        result = [self.people.get_person(3), self.people.get_person(5)]
        self.assertEqual(result, [self.max_m, self.sabine_m])

    def test_iterable(self):
        result = [p for p in self.people]
        self.assertEqual(result, [self.max_m, self.sabine_m])

    def test_people_iter(self):
        result = [p for p in self.people]
        self.assertEqual(result, [self.max_m, self.sabine_m])

    def test_get_by_index(self):
        result = [self.people.get_by_index(0), self.people.get_by_index(1)]
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