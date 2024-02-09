import pygame
import sys


class Phase:
    def __init__(self, name: str, audio: str, img: str) -> None:
        self.name = name
        self.audio = audio
        self.img = img
        self.sound = pygame.mixer.Sound(audio)


class Game:
    def __init__(self):
        pygame.font.init()
        pygame.mixer.init()
        screen_size = 640

        self.window_size = (screen_size, screen_size)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Phase Music")

        # Music
        self.phases = [
            Phase("Action", "audio/action.mp3", "img/action.png"),
            Phase("Encounter", "audio/encounter.mp3", "img/encounter.png"),
            Phase("Mythos", "audio/mythos.mp3", "img/mythos.png"),
        ]
        self.current_phase_index = 0

        phase = self.phases[self.current_phase_index]
        phase.sound.set_volume(1.0)
        self.background = pygame.image.load(phase.img)
        self.background = pygame.transform.scale(self.background, self.window_size)

    def run(self):
        running = True
        self.phases[self.current_phase_index].sound.play(-1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._play_next_phase()
            self._draw()

        pygame.quit()
        sys.exit()

    def _play_next_phase(self):
        current_phase = self.phases[self.current_phase_index]
        next_phase_index = (self.current_phase_index + 1) % len(self.phases)
        next_phase = self.phases[next_phase_index]

        next_phase.sound.play(-1)
        for vol in range(10, -1, -1):
            current_phase.sound.set_volume(vol / 10.0)
            next_phase.sound.set_volume((10 - vol) / 10.0)
            pygame.time.delay(700)

        current_phase.sound.stop()
        self.current_phase_index = next_phase_index

        # Background
        self.background = pygame.image.load(next_phase.img)
        self.background = pygame.transform.scale(self.background, self.window_size)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
