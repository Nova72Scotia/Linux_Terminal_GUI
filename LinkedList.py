"""
File: LinkedList.py
Author: James Scott Ferguson
"""
#Import Statements
from Linux_Terminal_GUI.Node import Node
from Linux_Terminal_GUI.AbstractCollection import AbstractCollection

class LinkedList(AbstractCollection):
  """The class LinkedList is a doubly linked list. It has AbstractCollection for a parent class. It can take an iterable collection as a source."""
  def __init__(self, initial_collection = None):
    """Sets self.head and self.tail and calls the parent constructor. 1 Arguments: 1st: Optional iterable object"""
    self.head = None
    self.tail = None
    super().__init__(initial_collection)

  def get_current(self, index):
    """Helper method which finds a node based on index. 1 Arguments: 1st: int within between 0 and len(self) - 1"""
    #The if-else conditionals are used to increase efficiency
    if index <= len(self) // 2:
      current = self.head
      for i in range(index - 1):
        current = current.next
    else:
      current = self.tail
      print(current.data)
      for i in range(len(self) - index):
        current = current.prev
    return current

  def add(self, item, index):
    """Adds item to the linked list. 2 Arguments: 1st: any object; 2nd: int between 0 and len(self)"""
    if index < 0 or index > len(self):
      raise IndexError
    elif not self.head:
      self.head = Node(item, None, None)
      self.tail = self.head
    elif index == 0:
      self.head.prev = Node(item, None, self.head)
      self.head = self.head.prev
    elif index == len(self):
      self.tail.next = Node(item, self.tail, None)
      self.tail = self.tail.next
    else:
      current = self.get_current(index)
      current.next = Node(item, current, current.next)
      current.next.next.prev = current.next
    self.size += 1

  def remove(self, index):
    """Removes item from the list. 1 Arguments: 1st: int between 0 and len(self) - 1"""
    if index < 0 or index >= len(self):
      self.size += 1
      raise indexError
    elif len(self) == 1 and index == 0:
      self.head = None
      self.tail = None
    elif index == 0:
      self.head = self.head.next
      self.head.prev = None
    elif index == len(self) - 1:
      self.tail = self.tail.prev
      self.tail.next = None
    else:
      current = self.get_current(index)
      current.next = current.next.next
      current.next.prev = current
    self.size -= 1

  def clear(self):
    """Resets internal references to default values, list no longer contains items. 0 arguments."""
    self.head = None
    self.tail = None
    self.size = 0

  def __getitem__(self, index):
    """Returns item corresponding to index; 1 Argument: 1st: int between 0 and len(self) - 1"""
    current = self.get_current(index + 1)
    return current.data

  def __setitem__(self, index, item):
    """Replaces item corresponding to index with a new item; 2 Arguments: 1st: int between 0 and len(self) - 1"""
    current = self.get_current(index + 1)
    current.data = item

  def __str__(self):
    """Returns a string represntation of the linked list similar to the string representation of a Python builtin list. 0 Arguments"""
    result = "["
    i = 0
    if self.head:
      current = self.head
      result += '"' + str(current.data) + '"'
      for i in range(len(self) - 1):
        i += 1
        current = current.next
        result += ', "' + str(current.data) + '"'
    result += "]"
    return result