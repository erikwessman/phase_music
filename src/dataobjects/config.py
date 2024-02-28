from typing import List

from pydantic import BaseModel


class ConfigPhase(BaseModel):
    name: str
    imgs: str
    audio: str


class ConfigEnding(BaseModel):
    key: str
    name: str
    img: str
    audio: str


class ConfigSfx(BaseModel):
    name: str
    key: str
    audio: str


class Config(BaseModel):
    phases: List[ConfigPhase]
    endings: List[ConfigEnding]
    sfx: List[ConfigSfx]
    font: str
