from typing import Optional

import pygame


class Phase:
    def __init__(
        self,
        unique_id,
        name: str,
        audio_path: str,
        img_path: str,
        key: Optional[str] = None,
        next_phase_id: Optional[str] = None,
    ) -> None:
        self.unique_id = unique_id
        self.next_phase_id: Optional[str] = next_phase_id

        self.name = name
        self.audio_path = audio_path
        self.sound = pygame.mixer.Sound(audio_path)
        self.background = pygame.image.load(img_path).convert()
        self.key = key
