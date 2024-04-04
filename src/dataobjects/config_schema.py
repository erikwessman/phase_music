from typing import List, Optional

from pydantic import BaseModel


class PhaseSchema(BaseModel):
    name: str
    unique_id: str
    next_phase: Optional[str] = None
    soundtracks: List[str]

    img: str
    """Image OR directory of images"""

    key: Optional[str] = None
    """Optional key for the phase"""

    duration: Optional[int] = None
    """Optional, how long the phase should last in seconds"""


class SfxSchema(BaseModel):
    name: str
    key: str
    audio: str


class MetadataSchema(BaseModel):
    name: str
    assets_dir: str


class ConfigSchema(BaseModel):
    start_phase: str
    metadata: MetadataSchema
    phases: List[PhaseSchema]
    sfx: List[SfxSchema]
    font: str
