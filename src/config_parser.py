import json
import random
import threading
import time
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
    _assets: Optional[Dict] = None
    _latest_load: str = ""

    def load_assets(self, config: ConfigSchema) -> None:
        t = threading.Thread(target=self._load_assets_thread, args=(config,))
        t.start()

    def _load_assets_thread(self, config: ConfigSchema) -> None:
        phases = self._get_phases(config)
        endings = self._get_endings(config)
        sfx = self._get_sfx(config)
        self._assets = {"phases": phases, "endings": endings, "sfx": sfx}

    def get_assets(self) -> dict:
        if self._assets is None:
            raise ValueError("Assets not loaded, use load_assets() first")

        return self._assets

    def status(self) -> dict:
        return {
            "loading": True if self._assets is None else False,
            "latest_load": self._latest_load,
        }

    def _get_phases(self, config: ConfigSchema) -> list[Phase]:
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

        return ordered_phases

    def _get_endings(self, config: ConfigSchema) -> List[Ending]:
        endings = []

        for ending in config.endings:
            self._latest_load = ending.name
            audio = random.choice(get_files_from_path(ending.audio))
            imgs = random.choice(get_files_from_path(ending.img))
            endings.append(
                Ending(getattr(pygame, ending.key), ending.name, audio, imgs)
            )

        return endings

    def _get_sfx(self, config: ConfigSchema) -> List[Sfx]:
        sfxs = []

        for sfx in config.sfx:
            self._latest_load
            sfxs.append(Sfx(getattr(pygame, sfx.key), sfx.audio))

        return sfxs

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
