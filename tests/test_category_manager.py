import unittest
from timer.category import Category, CategoryManager


class TestCategoryManager(unittest.TestCase):
    """Tests for the Category class"""

    def setUp(self):
        self._cat_mngr = CategoryManager()

    def assert_are_unique(self):
        num_of_cats = len(self._cat_mngr.categories)
        ids = set()
        names = set()
        for cat in self._cat_mngr.categories:
            ids.add(cat.id)
            names.add(cat.name)
        self.assertTrue(num_of_cats == len(ids) == len(names))

    def test_creating_unique_categories(self):
        names = ["a", "b", "c", "d"]
        for name in names:
            self._cat_mngr.new_unique(name)
        self.assert_are_unique()

    def test_error_with_same_names(self):
        names = ["a", "c", "a", "d"]
        with self.assertRaises(ValueError) as e:
            for name in names:
                self._cat_mngr.new_unique(name)
        self.assertEqual(e.exception.args[1], "a")

    def test_removing_category(self):
        """Tests that the delete function frees up the name and id"""
        cat_a = self._cat_mngr.new_unique("a")
        self.assertEqual(self._cat_mngr._ids, {0})
        self.assertEqual(self._cat_mngr._names, {"a"})

        self._cat_mngr.delete(cat_a)
        self.assertEqual(self._cat_mngr.categories, set())
        self.assertEqual(self._cat_mngr._ids, set())
        self.assertEqual(self._cat_mngr._names, set())

        cat_a2 = self._cat_mngr.new_unique("a")
        self.assertEqual(self._cat_mngr._ids, {0})
        self.assertEqual(self._cat_mngr._names, {"a"})
        self.assertIsInstance(cat_a2, Category)

        _ = self._cat_mngr.new_unique("b")
        self.assertEqual(self._cat_mngr._ids, {0, 1})
        self.assertEqual(self._cat_mngr._names, {"a", "b"})

        self._cat_mngr.delete(cat_a2)
        cat_c = self._cat_mngr.new_unique("c")
        self.assertEqual(cat_c.id, 0)
        self.assertEqual(cat_c.name, "c")
        self.assertEqual(self._cat_mngr._ids, {0, 1})
        self.assertEqual(self._cat_mngr._names, {"b", "c"})
