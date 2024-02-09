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
        self.screen_size = (640, 480)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Phase Music")

        # Load and stretch background
        self.background = pygame.image.load("img/background.png")
        self.background = pygame.transform.scale(self.background, self.screen_size)

        # UI
        self.font = pygame.font.Font(None, 36)
        self.button_color = (0, 128, 255)  # Example: A nice shade of blue
        self.button_highlight_color = (255, 100, 100)  # Example: Highlight color
        self.button = pygame.Rect(220, 190, 200, 50)
        self.button_border_color = (255, 255, 255)  # White border
        self.button_border_width = 2  # Border width

        # Music
        self.phases = [
            Phase("Action", "audio/action.mp3"),
            Phase("Encounter", "audio/encounter.mp3"),
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

        # Smooth transition between phases
        for vol in range(10, -1, -1):
            current_phase.sound.set_volume(vol / 10.0)
            next_phase.sound.set_volume((10 - vol) / 10.0)
            pygame.time.delay(100)

        current_phase.sound.stop()
        next_phase.sound.play(-1)
        self.current_phase_index = next_phase_index

    def _draw(self):
        # Draw stretched background
        self.screen.blit(self.background, (0, 0))

        # Draw button with styling
        pygame.draw.rect(self.screen, self.button_color, self.button)
        pygame.draw.rect(self.screen, self.button_border_color, self.button, self.button_border_width)
        
        # Button text
        button_text = self.font.render("Next Phase", True, (0, 0, 0))
        text_rect = button_text.get_rect(center=self.button.center)
        self.screen.blit(button_text, text_rect.topleft)

        # Current phase text
        phase_text = self.font.render("Current Phase: " + self.phases[self.current_phase_index].name, True, (0, 0, 0))
        self.screen.blit(phase_text, (20, 20))

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
