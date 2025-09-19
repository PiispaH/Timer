class Category:
    """Category with an id, name and assisiated duration."""

    def __init__(self, id_: int, name: str, duration: float):
        self._id = id_
        self._name = name
        self._duration = duration

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def duration(self) -> float:
        return self._duration

    @duration.setter
    def duration(self, value: float):
        self._duration = value

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return str(self.name) + ", id=" + str(self.id)


class CategoryManager:
    """Manages and holds the categories"""

    def __init__(self):
        self._categories = set()
        self._next_available = 0
        self._ids = set()
        self._names = set()

    @property
    def categories(self):
        return self._categories

    def delete(self, cat: Category):
        """Frees up the name and id"""
        self._names.remove(cat.name)
        self._ids.remove(cat.id)
        self._categories.remove(cat)
        self._update_smallest_available()

    def _update_smallest_available(self) -> int:
        """Returns the smallest non-negative integer that is not included in the set of ids"""
        maxium = max(self._ids, default=1)
        for i in range(0, maxium):
            if i not in self._ids:
                self._next_available = i
                return
        self._next_available = maxium + 1

    def recreate_existing(self, id_: int, name: str, duration: float) -> Category:
        cat = Category(id_, name, duration)
        self._categories.add(cat)
        self._names.add(name)
        self._ids.add(id_)
        self._update_smallest_available()

        return cat

    def new_unique(self, name: str) -> Category:
        """Creates a new unique category"""
        if name in self._names:
            raise ValueError(f"The name '{name}' is already in use.", name)
        id_ = self._next_available

        self._names.add(name)
        self._ids.add(id_)
        cat = Category(id_, name, 0.0)
        self._categories.add(cat)

        self._update_smallest_available()

        return cat
