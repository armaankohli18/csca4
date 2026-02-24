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

class Tests(unittest.TestCase):
  pass
  
if (__name__ == '__main__'):
  unittest.main()
