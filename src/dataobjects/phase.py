import time
import pygame


class Phase:
    def __init__(self, name: str, audio_path: str, img_path: str) -> None:
        self.name = name
        self.audio_path = audio_path
        self.img_path = img_path  # Store the path in case we need to reload assets
        
        start_time = time.time()
        self.sound = pygame.mixer.Sound(audio_path)
        print("Sound:", time.time() - start_time)
        
        start_time = time.time()
        self.background = pygame.image.load(img_path).convert()
        print("Image:", time.time() - start_time)
