import json
import os
from datetime import datetime
from typing import List
from tabulate import tabulate
from constants import KEYBIND_FULLSCREEN
from dataobjects.config import Config
from dataobjects.phase import Phase
from linked_list import CircularDoublyLinkedList


def get_files_from_path(path: str, extension=None) -> List[str]:
    if os.path.isfile(path):
        return [path]

    full_paths = []
    for entry in os.listdir(path):
        if extension and not entry.endswith(extension):
            continue

        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            full_paths.append(full_path)

    return sorted(full_paths)


def create_linked_list(phases: List[Phase]) -> CircularDoublyLinkedList:
    linked_list = CircularDoublyLinkedList()

    for phase in phases:
        linked_list.append(phase)

    return linked_list


def get_local_time():
    now = datetime.now()
    time_as_string = now.strftime("%H:%M")
    return time_as_string


def generate_title_str(title: str) -> str:
    char = " "
    border = char * (len(title) + 4)
    return f"\n{border}\n{char} {title} {char}\n{border}\n"


def readable_keycode(key: str) -> str:
    """
    Example:
        K_v -> v
        K_SPACE -> Space
    """
    if key.startswith("K_"):
        return key[2:].title()

    return key


def generate_controls_str(config: Config) -> str:
    headers = ["Action", "Key"]
    tablefmt = "github"
    output = ""

    # Generic
    output += generate_title_str("Generic") + "\n"
    rows = [
        ["Fullscreen", readable_keycode(KEYBIND_FULLSCREEN)],
        ["Next", "<- -> or Space"],
    ]
    output += tabulate(rows, headers, tablefmt) + "\n"

    # Sfx
    sfx = [(sfx.name, readable_keycode(sfx.key)) for sfx in config.sfx]
    output += generate_title_str("SFX") + "\n"
    output += tabulate(sfx, headers, tablefmt) + "\n"

    # Endings
    endings = [(ending.name, readable_keycode(ending.key)) for ending in config.endings]
    output += generate_title_str("Endings") + "\n"
    output += tabulate(endings, headers, tablefmt) + "\n"

    return output
