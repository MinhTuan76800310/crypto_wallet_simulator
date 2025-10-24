from abc import ABC, abstractmethod

class AbstractUoW(ABC):
    """Abstract Unit of Work defining transactional boundary."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

class InMemoryUoW(AbstractUoW):
    def __init__(self, repo=None):
        self.repo = repo
        self._staged = []

    def commit(self):
        # simple commit: persist staged items to repo
        if self.repo is not None:
            for item in self._staged:
                self.repo.add(item)
        self._staged.clear()

    def rollback(self):
        self._staged.clear()

    def stage(self, item):
        self._staged.append(item)
