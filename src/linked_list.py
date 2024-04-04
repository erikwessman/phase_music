from typing import Optional


class Node:
    def __init__(self, value: any):
        self.value: any = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    def append(self, value: any):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def get_node(self, predicate) -> Optional[Node]:
        current = self.head

        while current:
            if predicate(current.value):
                return current

            current = current.next

        return None
