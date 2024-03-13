import json
import os
from pprint import pprint
import random
import threading
from typing import List, Optional
import re

import pygame
from pydantic import ValidationError

from constants import PATH_CONFIGS
from dataobjects.config import ConfigSchema
from dataobjects.ending import Ending
from dataobjects.phase import Phase
from dataobjects.sfx import Sfx
from util import generate_title_str, get_files_from_path, none_or_whitespace


class ConfigParser:
    _latest_load: str = ""

    _phases: Optional[List[Phase]] = None
    _endings: Optional[List[Ending]] = None
    _sfxs: Optional[List[Sfx]] = None

    _ASSETS_DIR = "assets"

    def __init__(self, config: ConfigSchema) -> None:
        if config is None:
            raise ValueError("Config is required")

        self._config = config

    def load_assets(self) -> None:
        for method in [self._load_phases, self._load_endings, self._load_sfx]:
            thread = threading.Thread(target=method)
            thread.start()

    def get_assets(self) -> dict:
        if not self._loading_complete():
            raise ValueError("Assets not loaded, use load_assets() first")

        return {
            "phases": self._phases,
            "endings": self._endings,
            "sfx": self._sfxs,
        }

    def status(self) -> dict:
        return {
            "loading": not self._loading_complete(),
            "latest_load": self._latest_load,
        }

    def _loading_complete(self) -> bool:
        return all(
            asset is not None for asset in [self._phases, self._endings, self._sfxs]
        )

    def _load_phases(self) -> None:
        phases = []

        for phase in self._config.phases:
            self._latest_load = phase.name
            phase_instances = []

            audio_paths = get_files_from_path(phase.audio)
            img_paths = get_files_from_path(phase.imgs)

            for img in img_paths:
                audio = random.choice(audio_paths)
                phase_instances.append(Phase(phase.name, audio, img))

            phases.append(phase_instances)

        # If there are more of one type of phase than the others, loop back
        ordered_phases = []
        max_length = max(len(p) for p in phases)

        for i in range(max_length):
            for phase in phases:
                phase_index = i % len(phase)
                ordered_phases.append(phase[phase_index])

        self._phases = ordered_phases

    def _load_endings(self) -> None:
        endings = []

        for ending in self._config.endings:
            self._latest_load = ending.name
            audio = random.choice(get_files_from_path(ending.audio))
            imgs = random.choice(get_files_from_path(ending.img))
            endings.append(
                Ending(getattr(pygame, ending.key), ending.name, audio, imgs)
            )

        self._endings = endings

    def _load_sfx(self) -> None:
        sfxs = []

        for sfx in self._config.sfx:
            self._latest_load
            sfxs.append(Sfx(getattr(pygame, sfx.key), sfx.audio))

        self._sfxs = sfxs

    def to_path(self, asset: str) -> dict:
        path = f"{self._ASSETS_DIR}/{self._config.metadata.subdir}"

        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist")

        config_specific_assets = get_files_from_path(path, recursive=True)

        all_files = get_files_from_path(config_path)

        pass

    @staticmethod
    def parse_schema(path: str) -> ConfigSchema:
        with open(path) as f:
            data = json.load(f)

        return ConfigSchema(**data)

    @staticmethod
    def assert_valid_configs() -> None:
        files = get_files_from_path(PATH_CONFIGS, "json")
        error = False

        for file in files:
            try:
                ConfigParser.parse_schema(file)
            except ValidationError as e:
                print(generate_title_str(f"Invalid config: {file}"))
                print(e)
                error = True

        if error:
            raise ValidationError("Invalid config files")

    @staticmethod
    def assert_valid_names() -> None:
        files = get_files_from_path(ConfigParser._ASSETS_DIR, recursive=True)

        error = False
        for f in files:
            filename = os.path.basename(f)

            if none_or_whitespace(f) or not re.match(r"^[a-z0-9_.]*$", filename):
                print(generate_title_str(f"❗ Invalid file name: {f}", 1))
                error = True

        if error:
            raise ValueError("Invalid file name(s)")

    @staticmethod
    def assert_non_clashing_assets() -> None:
        """
        Every direct folder in the assets directory should have unique file
        names. May overlap between the directories, but not recursively
        within the same directory.
        """

        for directory in os.listdir(ConfigParser._ASSETS_DIR):
            directory_path = os.path.join(ConfigParser._ASSETS_DIR, directory)

            if os.path.isdir(directory_path):
                ConfigParser._assert_no_duplicates(directory_path)

    @staticmethod
    def _assert_no_duplicates(directory: str) -> None:
        print(directory)
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
