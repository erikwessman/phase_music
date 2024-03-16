from typing import List, Optional

from pydantic import BaseModel


class PhaseSchema(BaseModel):
    name: str
    soundtracks: List[str]

    img: str
    """Image OR directory of images"""

    key: Optional[str] = None
    """Optional key for the phase"""


class SfxSchema(BaseModel):
    name: str
    key: str
    audio: str


class MetadataSchema(BaseModel):
    name: str
    assets_dir: str


class ConfigSchema(BaseModel):
    metadata: MetadataSchema
    phases: List[PhaseSchema]
    sfx: List[SfxSchema]
    font: str
