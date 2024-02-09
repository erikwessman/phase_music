import pygame
import sys


class Phase:
    def __init__(self, name: str, audio: str) -> None:
        self.name = name
        self.audio = audio
        self.sound = pygame.mixer.Sound(audio)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("phase music")

        # UI
        self.font = pygame.font.Font(None, 36)
        self.button = pygame.Rect(220, 190, 200, 100)

        # Music
        self.phases = [
            Phase("Action", "audio/action.mp3"),
            Phase("Encounter", "audio/encounter.mp3"),
            # Phase("Mythos", "audio/mythos.mp3"),
        ]
        self.current_phase_index = 0
        self.phases[self.current_phase_index].sound.set_volume(1.0)

    def run(self):
        running = True
        self.phases[self.current_phase_index].sound.play(-1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.collidepoint(event.pos):
                        self._play_next_phase()
            self._draw()

        pygame.quit()
        sys.exit()

    def _play_next_phase(self):
        current_phase = self.phases[self.current_phase_index]
        next_phase_index = (self.current_phase_index + 1) % len(self.phases)
        next_phase = self.phases[next_phase_index]

        for vol in range(10, -1, -1):
            current_phase.sound.set_volume(vol / 10.0)
            next_phase.sound.set_volume((10 - vol) / 10.0)
            pygame.time.delay(100)

        current_phase.sound.stop()
        next_phase.sound.play(-1)
        self.current_phase_index = next_phase_index

    def _draw(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 255), self.button)
        text = self.font.render(
            self.phases[self.current_phase_index].name, True, (255, 255, 255)
        )
        self.screen.blit(text, (self.button.x + 50, self.button.y + 40))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
