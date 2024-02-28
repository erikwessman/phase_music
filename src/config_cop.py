import json

from pydantic import ValidationError

from constants import PATH_CONFIGS
from dataobjects.config import Config
from util import generate_title_str, get_files_from_path


class ConfigCop:
    """
    👮 aka ConfigManager

    Purpose: Additions to a config and code must be reflected on all configs.
    """

    @staticmethod
    def parse_config(path: str) -> Config:
        with open(path) as f:
            data = json.load(f)

        return Config(**data)

    @staticmethod
    def assert_valid_configs() -> None:
        files = get_files_from_path(PATH_CONFIGS, "json")
        error = False

        for file in files:
            try:
                ConfigCop.parse_config(file)
            except ValidationError as e:
                print(generate_title_str(f"Invalid config: {file}"))
                print(e)
                error = True

        if error:
            raise ValidationError("Invalid config files")
