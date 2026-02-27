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

# Return the hash code of 's' (see assignment description).
def hash_fn(s: str) -> int:
  h = 0
  for ch in s:
      h = h * 31 + ord(ch)
  return h
# Make a fresh hash table with the given number of bins 'size',
# containing no elements.
def make_hash(size: int) -> HashTable:
  return HashTable([None]*size, 0)

# Return the number of bins in 'ht'.
def hash_size(ht: HashTable) -> int:
  return len(ht.bins)

# Return the number of elements (key-value pairs) in 'ht'.
def hash_count(ht: HashTable) -> int:
  return ht.count

# Return whether 'ht' contains a mapping for the given 'word'.
def has_key(ht: HashTable, word: str) -> bool:
  index = hash_fn(word) % hash_size(ht)
  bin = ht.bins[index]
  return has_key_helper(bin, word)
  
def has_key_helper(n: WordLinesList, word: str) -> bool:
  match n:
    case None:
      return False
    case WLNode(f, r):
      if f.key == word:
        return True
      return has_key_helper(r, word)

# Return the line numbers associated with the key 'word' in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def lookup(ht: HashTable, word: str) -> List[int]:
  index = hash_fn(word) % hash_size(ht)
  bin = ht.bins[index] 
  return lookup_helper(bin, word)

def lookup_helper(n: WordLinesList, word: str) -> list[int]:
  match n:
    case None:
      return []
    case WLNode(f, r):
      if f.key == word:
        return il_to_list(f.linenums)
      else:
        return lookup_helper(r, word)

def il_to_list(Il: IntList) -> list[int]:
  output : list[int] = []
  match Il:
    case None:
      return []
    case IntNode(f, r):
      output.append(f)
      return output + il_to_list(r)
    
# Record in 'ht' that 'word' has an occurrence on line 'line'.
def add(ht: HashTable, word: str, line: int) -> None:
  

# Return the words that have mappings in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
pass
# Given a hash table 'stop_words' containing stop words as keys, plus
# a sequence of strings 'lines' representing the lines of a document,
# return a hash table representing a concordance of that document.
def make_concordance(stop_words: HashTable, lines: List[str]) -> HashTable:
pass
# Given an input file path, a stop-words file path, and an output file path,
# overwrite the indicated output file with a sorted concordance of the input
file.
def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
pass

class Tests(unittest.TestCase):
  pass
  
if (__name__ == '__main__'):
  unittest.main()
