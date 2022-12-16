"""
Name: Node.py
Author: James Scott Ferguson
"""

class Node():
  """The objects of this class make up the contents of LinkedList and LinkedStack. Facilitates a doubly linked structure."""
  def __init__(self, data = None, prev = None, next = None):
    self.data = data
    self.prev = prev
    self.next = next