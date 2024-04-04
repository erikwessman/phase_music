import os
from datetime import datetime
from typing import List

from tabulate import tabulate

from constants import KEYBIND_FULLSCREEN, PATH_CONTROLS
from dataobjects.config_schema import ConfigSchema
from dataobjects.phase import Phase
from linked_list import LinkedList


def get_files_from_path(
    path: str,
    extension: str = None,
    recursive: bool = False,
    include_dirs: bool = False,
) -> List[str]:
    """
    Retrieves a list of file paths from the given directory path, with an option to search recursively.
    If the path is a file, returns a list with that file.

    Args:
        path (str): The directory path or file path to search.
        extension (str, optional): The file extension to filter the results by. If None, all files are included. Defaults to None.
        recursive (bool, optional): Whether to search directories recursively. Defaults to False.
        include_dirs (bool, optional): Whether to include directories in the results. Defaults to False.

    Returns:
        List[str]: A sorted list of file paths meeting the criteria.
    """

    # Base case: path is a file
    if os.path.isfile(path):
        if extension is None or path.endswith(extension):
            return [path]

        return []

    files = []
    for entry in os.scandir(path):
        full_path = entry.path

        # Recursive case: path is a directory
        if entry.is_dir() and recursive:
            files.extend(
                get_files_from_path(full_path, extension, recursive, include_dirs)
            )

            if include_dirs:
                files.append(full_path)

        # Base case: path is a file
        if entry.is_file():
            if extension is None or entry.name.endswith(extension):
                files.append(full_path)

    return sorted(files)


def create_linked_list(head: Phase, phases: List[Phase]) -> LinkedList:
    list = LinkedList()
    list.append(head)
    added_phases = [head.unique_id]

    while True:
        next_phase_id = list.tail.value.next_phase_id

        if next_phase_id in added_phases:
            # Loop to the already added phase
            tail = list.tail

            loop_to = list.get_node(lambda x: x.unique_id == next_phase_id)
            tail.next = loop_to
            break

        for phase in phases:
            if phase.unique_id == next_phase_id:
                added_phases.append(phase.unique_id)
                list.append(phase)
                break
        else:
            break

    return list


def get_local_time():
    now = datetime.now()
    time_as_string = now.strftime("%H:%M")
    return time_as_string


def generate_title_str(title: str, indent_index: int = 0) -> str:
    indent = " " * indent_index * 4
    char = "."
    border = char * (len(title) + 4)

    s = f"\n{indent}{border}\n"
    s += f"{indent}{char} {title} {char}\n"
    s += f"{indent}{border}\n"

    return s


def readable_keycode(key: str) -> str:
    """
    Example:
        K_v -> v
        K_SPACE -> Space
    """
    if key is None:
        return ""

    if key.startswith("K_"):
        return key[2:].title()

    return key


def generate_controls_file(config: ConfigSchema) -> None:
    headers = ["Action", "Key"]
    tablefmt = "github"

    with open(PATH_CONTROLS, "w") as f:
        # Generic
        f.write(generate_title_str("Generic") + "\n\n")
        rows = [
            ["Fullscreen", readable_keycode(KEYBIND_FULLSCREEN)],
            ["Next", "<- -> or Space"],
        ]
        f.write(tabulate(rows, headers, tablefmt) + "\n\n")

        # Sfx
        sfx = [(sfx.name, readable_keycode(sfx.key)) for sfx in config.sfx]
        f.write(generate_title_str("SFX") + "\n\n")
        f.write(tabulate(sfx, headers, tablefmt) + "\n\n")

        # Phases
        phases = sorted(
            [(phase.name, readable_keycode(phase.key)) for phase in config.phases],
            key=lambda x: x[1],
            reverse=True,
        )
        f.write(generate_title_str("Phases") + "\n\n")
        f.write(tabulate(phases, headers, tablefmt) + "\n\n")


def none_or_whitespace(f):
    return f is None or f.isspace()
