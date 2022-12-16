"""
File: LinkedStack.py
Author: James Scott Ferguson
"""
#Import Statements
from Linux_Terminal_GUI.Node import Node
from Linux_Terminal_GUI.LinkedList import LinkedList

class LinkedStack(LinkedList):
  """The class LinkedStack is a linked stack. It has LinkedList as a parent. It can take an iterable object as a source."""
  def __init__(self, initial_collection = None):
    """Calls parents constructor. 1 Arguments: 1st: Optional iterable collection"""
    super().__init__(initial_collection)

  def push(self, item):
    """Adds item to the top of the stack. 1 Arguments: 1st: Any object."""
    self.add(item, 0)

  def pop(self):
    """Removes the item from the top of the stack and does not return the item. 0 Arguments"""
    self.remove(0)

  def peek(self):
    """Returns the item at the top of the stack. 0 Arguments"""
    if self.head:
      return self.head.data
    else:
      return None

  def clone(self):
    """Returns a LinkedStack identical to itself. 0 Arguments"""
    other = LinkedStack()
    other.head = self.head
    other.tail = self.tail
    other.size = len(self)
    return other

  def convert_to_list(self):
    """Returns a LinkedList with the same contents as itself. 0 Arguments"""
    other = LinkedList()
    other.head = self.head
    other.tail = self.tail
    other.size = len(self)
    return other