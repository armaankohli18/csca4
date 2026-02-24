from typing import *
from dataclasses import dataclass
import unittest
import sys
import string
sys.setrecursionlimit(10**6)

IntList: TypeAlias = Union[None, "IntNode"]

@dataclass(frozen=True)
class IntNode:
  first: int
  rest: IntList

@dataclass
class WordLines:
  key : str
  linenums: IntList

WordLinesList: TypeAlias = Union[None, "WLNode"]

@dataclass(frozen=True)
class WLNode:
  first: WordLines
  rest: WordLinesList

@dataclass
class HashTable:
  bins: list[WordLinesList]
  count: int


class Tests(unittest.TestCase):
  pass
  
if (__name__ == '__main__'):
  unittest.main()
