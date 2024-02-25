import pygame


class Sfx:
    def __init__(self, key: int, audio_path: str) -> None:
        self.key = key
        self.sound = pygame.mixer.Sound(audio_path)
