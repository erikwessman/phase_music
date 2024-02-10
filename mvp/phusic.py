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

        self.phases = [
            Phase("Action", "audio/action.mp3", "img/action.png"),
            Phase("Encounter", "audio/encounter.mp3", "img/encounter.png"),
            Phase("Mythos", "audio/mythos.mp3", "img/mythos.png"),
        ]
        self.phase_index = 0
        self.is_fading = False
        self.fade_step = 0
        self.total_fade_steps = 255
        self.transition_duration = 6
        self.FPS = 60
        self.frames_for_transition = self.transition_duration * self.FPS
        self.fade_step_increment = self.total_fade_steps / float(
            self.frames_for_transition
        )
        self.next_background = None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self._start_phase(self.phase_index)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.is_fading:
                    self._next_phase()
            self._draw()
            clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def _start_phase(self, phase_index):
        phase = self.phases[phase_index]
        phase.sound.play(-1)
        phase.sound.set_volume(1.0)
        self.background = pygame.image.load(phase.img).convert()
        self.background = pygame.transform.scale(self.background, self.window_size)

    def _next_phase(self):
        self.is_fading = True
        self.fade_step = 0
        next_phase_index = (self.phase_index + 1) % len(self.phases)
        next_phase = self.phases[next_phase_index]
        next_phase.sound.play(-1)
        next_phase.sound.set_volume(0.0)
        self.next_background = pygame.image.load(next_phase.img).convert()
        self.next_background = pygame.transform.scale(
            self.next_background, self.window_size
        )

    def _draw(self):
        if self.is_fading:
            current_phase = self.phases[self.phase_index]
            next_phase = self.phases[(self.phase_index + 1) % len(self.phases)]
            alpha = int(self.fade_step * (255 / self.total_fade_steps))
            self.next_background.set_alpha(alpha)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.next_background, (0, 0))
            new_volume = alpha / 255.0
            next_phase.sound.set_volume(new_volume)
            current_phase.sound.set_volume(1.0 - new_volume)
            self.fade_step += self.fade_step_increment
            if self.fade_step > self.total_fade_steps:
                self.is_fading = False
                self.phase_index = (self.phase_index + 1) % len(self.phases)
                self.background = self.next_background
                current_phase.sound.stop()
        else:
            self.screen.blit(self.background, (0, 0))

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
