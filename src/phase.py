import pygame


class Phase:
    def __init__(self, name: str, audio_path: str, img_path: str) -> None:
        self.name = name
        self.sound = pygame.mixer.Sound(audio_path)
        self.background = pygame.image.load(img_path).convert()

        self.next = None  # Keep track of which phases are before and after
        self.prev = None
