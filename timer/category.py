from __future__ import annotations


class Category:
    """Every category has an unique id and name with assisiated duration."""

    _next_available = 0
    _ids = set()
    _names = set()

    def __init__(self, id_: int, name: str, duration: float):
        """Should be used only to load existing categories."""
        self._name = name
        self._id = id_
        self._duarion = duration

        Category._ids.add(id_)
        Category._names.add(name)
        Category._next_available = Category._find_smallest_available()

    @classmethod
    def _find_smallest_available(cls) -> int:
        maxium = max(cls._ids)
        for i in range(min(cls._ids) + 1, maxium):
            if i not in cls._ids:
                return i
        return maxium + 1

    @classmethod
    def new_unique(cls, name: str) -> Category:
        """Creates a new unique category"""
        if name in cls._names:
            raise ValueError("The name '{name}' is already in use.")
        id_ = cls._next_available

        cls._names.add(name)
        cls._ids.add(id_)
        cls._next_available = cls._find_smallest_available()

        return cls(id_, name, 0.0)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def duration(self) -> float:
        return self._duarion

    @duration.setter
    def duration(self, value):
        self._duarion = value

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return str(self._name) + ", id=" + str(self._id)
