import os
import pprint
import re

from pydantic import ValidationError

from config_manager import ConfigManager
from constants import PATH_ASSETS, PATH_CONFIGS
from dataobjects.config_schema import ConfigSchema
from util import generate_title_str, get_files_from_path, none_or_whitespace

"""Functions to assert the validity of the config files and assets."""


def patrol() -> None:
    _assert_valid_filenames()
    _assert_valid_configs()
    _assert_non_clashing_assets()


def _assert_valid_configs() -> None:
    files = get_files_from_path(PATH_CONFIGS, "json")
    error = False

    for f in files:
        try:
            config = ConfigManager.parse_schema(f)
            _assert_valid_config(config)
        except ValidationError as e:
            print(generate_title_str(f"Invalid config: {f}"))
            print(e)
            error = True

    if error:
        raise ValidationError("Invalid config files")


def _assert_valid_config(config: ConfigSchema) -> None:
    """Ensure the config is valid."""

    if config is None:
        raise ValueError("Config is required")

    _assert_files_exists(config)

    # Ensure unique ids
    unique_ids = [p.unique_id for p in config.phases]
    if len(unique_ids) != len(set(unique_ids)):
        raise ValueError("Duplicate unique ids")

    # Ensure next_phase is valid
    for phase in config.phases:
        if phase.next_phase is not None:
            if phase.next_phase not in unique_ids:
                raise ValueError("Invalid next_phase")


def _assert_valid_filenames() -> None:
    """Ensure all files have valid names."""

    files = get_files_from_path(PATH_ASSETS, recursive=True)

    error = False
    for f in files:
        filename = os.path.basename(f)

        if none_or_whitespace(f) or not re.match(r"^[a-z0-9_.]*$", filename):
            print(generate_title_str(f"❗ Invalid file name: {f}", 1))
            error = True

    if error:
        raise ValueError("Invalid file name(s)")


def _assert_files_exists(config: ConfigSchema) -> None:
    """Ensure all files in the config exist."""

    for phase in config.phases:
        cm = ConfigManager(config)
        cm._asset_to_path(phase.img)

        for soundtrack in phase.soundtracks:
            cm._asset_to_path(soundtrack)

    for sfx in config.sfx:
        cm._asset_to_path(sfx.audio)

    cm._asset_to_path(config.font)


def _assert_non_clashing_assets() -> None:
    """
    Every direct folder in the assets directory should have unique file
    names. May overlap between the directories, but not recursively
    within the same directory.
    """

    for directory in os.listdir(PATH_ASSETS):
        directory_path = os.path.join(PATH_ASSETS, directory)

        if os.path.isdir(directory_path):
            _assert_no_duplicate_files(directory_path)


def _assert_no_duplicate_files(directory: str) -> None:
    """Ensure there are no duplicate files in the directory."""

    files = get_files_from_path(directory, recursive=True)

    found_files = []
    error = False
    clashes = []

    for path in files:
        filename = os.path.basename(path)
        if filename in found_files:
            print(generate_title_str(f"❗ Clashing file name: {filename}", 1))
            error = True
            clashes.append(path)

        found_files.append(filename)

    if error:
        print(generate_title_str("🚨 Clashing files! Exiting 🚨"))
        pprint(clashes)
        raise ValueError("Clashing file names")
