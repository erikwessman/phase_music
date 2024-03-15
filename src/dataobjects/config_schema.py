from typing import List

from pydantic import BaseModel


class PhaseSchema(BaseModel):
    name: str
    soundtracks: List[str]

    img: str
    """Image OR directory of images"""


class EndingSchema(BaseModel):
    key: str
    name: str

    img: str
    """Single image file"""

    audio: str
    """Single audio file"""


class SfxSchema(BaseModel):
    name: str
    key: str

    audio: str
    """Single audio file"""


class MetadataSchema(BaseModel):
    name: str
    assets_dir: str


class ConfigSchema(BaseModel):
    metadata: MetadataSchema
    phases: List[PhaseSchema]
    endings: List[EndingSchema]
    sfx: List[SfxSchema]
    font: str
