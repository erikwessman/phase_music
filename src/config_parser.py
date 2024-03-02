import json
import random
import threading
from ast import Dict
from typing import List, Optional

import pygame
from pydantic import ValidationError

from constants import PATH_CONFIGS
from dataobjects.config import ConfigSchema
from dataobjects.ending import Ending
from dataobjects.phase import Phase
from dataobjects.sfx import Sfx
from util import generate_title_str, get_files_from_path


class ConfigParser:
    _latest_load: str = ""

    _phases: Optional[List[Phase]] = None
    _endings: Optional[List[Ending]] = None
    _sfxs: Optional[List[Sfx]] = None

    def load_assets(self, config: ConfigSchema) -> None:
        for method in [self._load_phases, self._load_endings, self._load_sfx]:
            thread = threading.Thread(target=method, args=(config,))
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

    def _load_phases(self, config: ConfigSchema) -> None:
        phases = []

        for phase in config.phases:
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

    def _load_endings(self, config: ConfigSchema) -> None:
        endings = []

        for ending in config.endings:
            self._latest_load = ending.name
            audio = random.choice(get_files_from_path(ending.audio))
            imgs = random.choice(get_files_from_path(ending.img))
            endings.append(
                Ending(getattr(pygame, ending.key), ending.name, audio, imgs)
            )

        self._endings = endings

    def _load_sfx(self, config: ConfigSchema) -> None:
        sfxs = []

        for sfx in config.sfx:
            self._latest_load
            sfxs.append(Sfx(getattr(pygame, sfx.key), sfx.audio))

        self._sfxs = sfxs

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
