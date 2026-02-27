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
  index = hash_fn(word) % hash_size(ht)
  node = ht.bins[index]
  while node is not None:
    if node.first.key == word:
      linesword = node.first.linenums
      while linesword is not None:
        if linesword.first == line:
          return None
        linesword = linesword.rest
      node.first.linenums = IntNode(line, node.first.linenums)
      return
    node = node.rest
  ht.bins[index] = WLNode(WordLines(word, IntNode(line, None)), ht.bins[index])
  ht.count += 1
  if hash_count(ht) >= hash_size(ht):
    resize(ht)

def resize(ht : HashTable) -> None:
  size = hash_size(ht) * 2
  bins : list[WordLinesList] = [None] * size
  for bin in ht.bins:
    rehash(bin, bins, size)
  ht.bins = bins

def rehash(n: WordLinesList, bins: list[WordLinesList], size: int) -> None:
  match n:
    case None:
      return None
    case WLNode(f, r):
      index = hash_fn(f.key) % size
      bins[index] = WLNode(f, bins[index])
      rehash(r, bins, size)

# Return the words that have mappings in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
  output : list[str] = []
  for bin in ht.bins:
    node = bin
    while node is not None:
      output.append(node.first.key)
      node = node.rest
  return output

# Given a hash table 'stop_words' containing stop words as keys, plus
# a sequence of strings 'lines' representing the lines of a document,
# return a hash table representing a concordance of that document.
def make_concordance(stop_words: HashTable, lines: List[str]) -> HashTable:
  concordance = make_hash(128)
  linenumber = 1
  for line in lines:
    line = line.replace("'", "")
    for p in string.punctuation:
      line = line.replace(p, " ")
    line = line.lower()
    words = line.split()
    for word in words:
      if word.isalpha() and not has_key(stop_words, word):
        add(concordance, word, linenumber)
    linenumber += 1
  return concordance

# Given an input file path, a stop-words file path, and an output file path,
# overwrite the indicated output file with a sorted concordance of the input
#file.
def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
  stop_words = make_hash(128)
  with open(stop_words_file, "r", encoding="utf-8") as file:
    for line in file:
      word = line.strip().lower()
      if word != "":
        add(stop_words, word, 0)
  with open(in_file, "r", encoding="utf-8") as infile:
    lines = infile.readlines()
  concordance = make_concordance(stop_words, lines)
  keys = hash_keys(concordance)
  keys.sort()
  with open(out_file, "w", encoding="utf-8") as outfile:
    for word in keys:
      numbers = lookup(concordance, word)
      numbers.sort()
      outfile.write(word + ": " + " ".join(str(number) for number in numbers) + "\n")

class Tests(unittest.TestCase):

  def test_hash_fn(self):
    self.assertEqual(hash_fn("a"), ord("a"))
    self.assertEqual(hash_fn("b"), ord("b"))
    self.assertNotEqual(hash_fn("a"), ord("b"))
  
  def test_make_hash(self):
    ht1 = make_hash(8)
    ht2 = make_hash(2)
    self.assertEqual(ht1, HashTable([None, None, None, None, None, None, None, None], 0))
    self.assertEqual(ht2, HashTable([None, None], 0))
  
  def test_hash_size(self):
    ht1 = make_hash(8)
    ht2 = make_hash(2)
    self.assertEqual(hash_size(ht1), 8)
    self.assertEqual(hash_size(ht2), 2)

  def test_hash_count(self):
        ht1 = make_hash(5)
        add(ht1, "Armaan", 1)
        self.assertEqual(hash_count(ht1), 1)

  def test_has_key(self):
    ht = make_hash(5)
    add(ht, "Ashlyn", 1)
    self.assertEqual(has_key(ht, "Ashlyn"), True)
    self.assertEqual(has_key(ht, "Armaan"), False)
    self.assertEqual(has_key(ht, "Philbrock"), False)

  def test_has_key_helper(self):
    n = WLNode(WordLines("Armaan", IntNode(1, None)), None)
    self.assertEqual(has_key_helper(n, "Armaan"), True)
    self.assertEqual(has_key_helper(n, "Ashlyn"), False)
    self.assertEqual(has_key_helper(n, "Philbrick"), False)
  
  def test_lookup(self):
    ht = make_hash(5)
    add(ht, "Armaan", 1)
    add(ht, "Ashlyn", 2)
    self.assertEqual(lookup(ht, "Armaan"), [1])
    self.assertEqual(lookup(ht, "Ashlyn"), [2])
    self.assertEqual(lookup(ht, "Philbrick"), [])

  def test_lookup_helper(self):
    n = WLNode(WordLines("Armaan", IntNode(1, None)), None)
    self.assertEqual(lookup_helper(n, "Armaan"), [1])
    self.assertEqual(lookup_helper(n, "Data"), [])

  def test_il_to_list(self):
    il = IntNode(1, IntNode(2, None))
    self.assertEqual(il_to_list(il), [1, 2])
    self.assertNotEqual(il_to_list(il), [1, 2, 3])
    self.assertNotEqual(il_to_list(il), [1, 3])

  def test_add(self):
    ht = make_hash(5)
    add(ht, "Armaan", 1)
    add(ht, "Armaan", 1)
    self.assertEqual(hash_count(ht), 1)
    self.assertNotEqual(hash_count(ht), 2)

  def test_resize(self):
    ht = make_hash(2)
    add(ht, "Armaan", 1)
    add(ht, "Ashlyn", 2)
    self.assertEqual(hash_size(ht) >= 2, True)
    self.assertEqual(has_key(ht, "Philbrick"), False)

  def test_rehash(self):
    n = WLNode(WordLines("Armaan", IntNode(1, None)), WLNode(WordLines("Ashlyn", IntNode(2, None)), None))
    bins : List[WordLinesList]= [None] * 4
    rehash(n, bins, 4)
    index_a = hash_fn("Armaan") % 4
    index_b = hash_fn("Ashlyn") % 4
    self.assertEqual(has_key_helper(bins[index_a], "Armaan"), True)
    self.assertEqual(has_key_helper(bins[index_b], "Ashlyn"), True)

  def test_hash_keys(self):
    ht = make_hash(5)
    add(ht, "Armaan", 1)
    add(ht, "Ashlyn", 2)
    self.assertEqual(hash_keys(ht), ["Armaan", "Ashlyn"])
    self.assertNotEqual(hash_keys(ht), ["Armaan", "Ashlyn", "Philbrick"])

  def test_make_concordance(self):
    ht = make_hash(5)
    add(ht, "the", 0)
    lst : list[str] = ["The class is fun", "The class is long"]
    concordance = make_concordance(ht, lst)
    self.assertEqual(has_key(concordance, "the"), False)
    self.assertEqual(lookup(concordance, "class"), [2, 1])

  
if (__name__ == '__main__'):
  unittest.main()
