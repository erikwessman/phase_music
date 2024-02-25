import json
from typing import get_type_hints
from constants import PATH_CONFIGS
from dataobjects.config import Config, ConfigEnding, ConfigPhase, ConfigSfx
from util import get_files_from_path


class ConfigCop:
    """
    👮

    Purpose: Additions to a config and code must be reflected on all configs.
    """

    @staticmethod
    def parse_config(path: str) -> Config:
        with open(path) as f:
            data = json.load(f)

        config = Config(**data)
        return config

    @staticmethod
    def assert_valid_configs() -> None:
        files = get_files_from_path(PATH_CONFIGS, "json")

        for file in files:
            config = ConfigCop.parse_config(file)
            ConfigCop.assert_valid(config)

        print(files)

    @staticmethod
    def assert_valid(config: Config) -> None:
        return

        if config is None:
            raise ValueError("Config is None")

        for attr in ["phases", "endings", "sfx", "font"]:
            value = getattr(config, attr, None)
            if value is None or (isinstance(value, list) and not value):
                raise ValueError(f"Config attribute '{attr}' is None or empty")

            if isinstance(value, list):
                for item in value:
                    # Validate each attribute of the item
                    for field in vars(item).keys():
                        field_value = getattr(item, field, None)
                        if field_value is None or (
                            isinstance(field_value, str) and not field_value.strip()
                        ):
                            raise ValueError(
                                f"Attribute '{field}' in '{attr}' is not set or is empty"
                            )

        # Lengths
        if len(config.phases) == 0:
            raise ValueError("Config has no phases")

        if len(config.endings) == 0:
            raise ValueError("Config has no endings")

        if len(config.sfx) == 0:
            raise ValueError("Config has no sfx")

        if config.font is None:
            raise ValueError("Config has no font")


# phase_config: ConfigPhase = ConfigPhase()
# phase_config.name = "phase1"
# phase_config.imgs = "assets/phase1/imgs"
# # phase_config.audio = "wasd"

# conf = Config()
# conf.phases = [phase_config]

# ConfigCop.assert_valid(conf)
