## query.py is an abstract base class that specifies the Query to be used by librarian.py

@dataclass
class Query:
    location: str # the database if dbquery or the root folder if fsquery
