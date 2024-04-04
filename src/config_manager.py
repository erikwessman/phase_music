import json
import os
import random
import threading
from typing import List, Optional

import pygame

from constants import PATH_ASSETS, PATH_COMMON
from dataobjects.config_schema import ConfigSchema
from dataobjects.phase import Phase
from dataobjects.sfx import Sfx
from util import get_files_from_path


class ConfigManager:
    _latest_load: str = ""

    _phases: Optional[List[Phase]] = None
    _sfxs: Optional[List[Sfx]] = None

    def __init__(self, config: ConfigSchema) -> None:
        if config is None:
            raise ValueError("Config is required")

        self._config = config

    def load_assets(self) -> None:
        for method in [self._load_phases, self._load_sfx]:
            thread = threading.Thread(target=method)
            thread.start()

    def get_font(self) -> str:
        return self._asset_to_path(self._config.font)

    def get_assets(self) -> dict:
        if not self._loading_complete():
            raise ValueError("Assets not loaded, use load_assets() first")

        return {"phases": self._phases, "sfx": self._sfxs}

    def status(self) -> dict:
        return {
            "loading": not self._loading_complete(),
            "latest_load": self._latest_load,
        }

    def _loading_complete(self) -> bool:
        return all(asset is not None for asset in [self._phases, self._sfxs])

    def _load_phases(self) -> None:
        phases = []

        for phase in self._config.phases:
            self._latest_load = phase.name
            phase_instances = []

            audio_paths = []
            for asset in phase.soundtracks:
                for path in self._get_files_from_asset(asset):
                    audio_paths.append(path)

            img_paths = self._get_files_from_asset(phase.img)

            for img in img_paths:
                audio = random.choice(audio_paths)
                phase_instances.append(
                    Phase(
                        phase.unique_id,
                        phase.name,
                        audio,
                        img,
                        key=phase.key,
                        next_phase_id=phase.next_phase,
                        duration=phase.duration,
                    )
                )

            phases.append(phase_instances)

        # If there are more of one type of phase than the others, loop back
        ordered_phases = []
        max_length = max(len(p) for p in phases)

        for i in range(max_length):
            for phase in phases:
                phase_index = i % len(phase)
                ordered_phases.append(phase[phase_index])

        self._phases = ordered_phases

    def _load_sfx(self) -> None:
        sfxs = []

        for sfx in self._config.sfx:
            fx_path = self._asset_to_path(sfx.audio)
            sfxs.append(Sfx(getattr(pygame, sfx.key), fx_path))

        self._sfxs = sfxs

    def _get_files_from_asset(self, asset: str) -> List[str]:
        return get_files_from_path(self._asset_to_path(asset))

    def _asset_to_path(self, asset: str) -> str:
        """
        Convert an asset string to a path.

        Examples:
            - "woof.mp3"            -> "assets/sfx/woof.mp3".
            - "phases/woof_sounds/" -> "assets/phases/woof_sounds/".
            - "idontexist"          -> FileNotFoundError.
        """

        path = os.path.join(PATH_ASSETS, self._config.metadata.assets_dir)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist")

        assets = get_files_from_path(path, recursive=True, include_dirs=True)
        common_assets = get_files_from_path(
            PATH_COMMON, recursive=True, include_dirs=True
        )

        for f in assets + common_assets:
            # Cross-platform compatibility, becuase Windows is 💩
            cleaned_f = f.replace("\\", "/").rstrip("/")
            cleaned_asset = asset.replace("\\", "/").rstrip("/")

            if cleaned_f.endswith(cleaned_asset):
                return f

        raise FileNotFoundError(f"Asset {asset} not found")

    @staticmethod
    def parse_schema(path: str) -> ConfigSchema:
        """Parse a config schema from a file."""
        with open(path) as f:
            data = json.load(f)

        schema = ConfigSchema(**data)
        return schema
