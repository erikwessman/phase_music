import json
import random
from typing import List

import pygame
from pydantic import ValidationError

from constants import PATH_CONFIGS
from dataobjects.config import ConfigSchema
from dataobjects.ending import Ending
from dataobjects.phase import Phase
from dataobjects.sfx import Sfx
from util import generate_title_str, get_files_from_path


class ConfigManager:
    def get(self, config: ConfigSchema) -> dict:
        return {
            "phases": self._get_phases(config),
            "endings": self._get_endings(config),
            "sfx": self._get_sfx(config),
        }

    def _get_phases(self, config: ConfigSchema) -> list[Phase]:
        phases = []

        for i, phase in enumerate(config.phases):
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
            audio = random.choice(get_files_from_path(ending.audio))
            imgs = random.choice(get_files_from_path(ending.img))
            endings.append(
                Ending(getattr(pygame, ending.key), ending.name, audio, imgs)
            )

        return endings

    def _get_sfx(self, config: ConfigSchema) -> List[Sfx]:
        sfxs = []

        for sfx in config.sfx:
            sfxs.append(Sfx(getattr(pygame, sfx.key), sfx.audio))

        return sfxs

    def parse_config(self, path: str) -> ConfigSchema:
        with open(path) as f:
            data = json.load(f)

        return ConfigSchema(**data)

    def assert_valid_configs(self) -> None:
        files = get_files_from_path(PATH_CONFIGS, "json")
        error = False

        for file in files:
            try:
                self.parse_config(file)
            except ValidationError as e:
                print(generate_title_str(f"Invalid config: {file}"))
                print(e)
                error = True

        if error:
            raise ValidationError("Invalid config files")
