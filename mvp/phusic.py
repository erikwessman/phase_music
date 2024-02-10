import pygame
import sys


class Phase:
    def __init__(self, name: str, audio: str, img: str) -> None:
        self.name = name
        self.audio = audio
        self.img = img
        self.sound = pygame.mixer.Sound(audio)


class Game:
    is_fading = False

    def __init__(self):
        pygame.font.init()
        pygame.mixer.init()
        screen_size = 640

        self.window_size = (screen_size, screen_size)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Phase Music")

        # Music and Backgrounds
        self.phases = [
            Phase("Action", "audio/action.mp3", "img/action.png"),
            Phase("Encounter", "audio/encounter.mp3", "img/encounter.png"),
            Phase("Mythos", "audio/mythos.mp3", "img/mythos.png"),
        ]
        self.current_phase_index = 0

    def run(self):
        running = True
        phase = self.phases[self.current_phase_index]
        phase.sound.play(-1)
        phase.sound.set_volume(1.0)
        self.background = pygame.image.load(phase.img).convert()
        self.background = pygame.transform.scale(self.background, self.window_size)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.is_fading:
                    self.is_fading = True
                    print("Fading!")
                    self._play_next_phase()
                    self.is_fading = False
            self._draw()

        pygame.quit()
        sys.exit()

    def _play_next_phase(self):
        current_phase = self.phases[self.current_phase_index]
        next_phase_index = (self.current_phase_index + 1) % len(self.phases)
        next_phase = self.phases[next_phase_index]
        next_phase.sound.play(-1)
        next_phase.sound.set_volume(0.0)

        # Capture current screen
        current_screen = pygame.Surface(self.window_size).convert()
        current_screen.blit(self.screen, (0, 0))

        # Load next background
        next_background = pygame.image.load(next_phase.img).convert()
        next_background = pygame.transform.scale(next_background, self.window_size)

        total_steps = 255
        for step in range(total_steps + 1):
            alpha = step * (255 // total_steps)
            self.screen.blit(current_screen, (0, 0))
            next_background.set_alpha(alpha)
            self.screen.blit(next_background, (0, 0))
            pygame.display.flip()
            pygame.time.delay(100)

            new_volume = alpha / 255.0
            next_phase.sound.set_volume(new_volume)
            current_phase.sound.set_volume(1.0 - new_volume)

        current_phase.sound.stop()
        self.current_phase_index = next_phase_index
        self.background = next_background

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
