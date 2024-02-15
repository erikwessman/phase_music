import os
from typing import List

from linked_list import CircularDoublyLinkedList
from phase import Phase


def get_files_from_path(path: str):
    full_paths = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            full_paths.append(full_path)
    return sorted(full_paths)


def create_linked_list(phases: List[Phase]) -> CircularDoublyLinkedList:
    linked_list = CircularDoublyLinkedList()

    for phase in phases:
        linked_list.append(phase)

    return linked_list
