## librarian.py is an abstract class that specifies the Librarian interface that provides a 'Persistence_Manager' for filing to file server, database, etc.

from abc import ABC, abstractmethod

class Librarian(ABC):
    @abstractmethod
    def fn1(self):
        pass