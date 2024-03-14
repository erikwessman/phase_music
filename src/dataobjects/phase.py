import pygame


class Phase:
    def __init__(self, name: str, audio_path: str, img_path: str) -> None:
        self.name = name
        self.audio_path = audio_path
        print(f"audioooo_path: {audio_path}")
        self.sound = pygame.mixer.Sound(audio_path)
        self.background = pygame.image.load(img_path).convert()
