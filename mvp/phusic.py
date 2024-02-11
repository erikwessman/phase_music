import json
import pygame
import argparse
import sys


class Phase:
    def __init__(self, name: str, audio: str, img: str) -> None:
        self.name = name
        self.audio = audio
        self.img = img
        self.sound = pygame.mixer.Sound(audio)


class Sfx:
    def __init__(self, key: int, audio: str) -> None:
        self.key = key
        self.audio = audio
        self.sound = pygame.mixer.Sound(audio)


class Game:
    TOTAL_FADE_STEPS = 255
    TRANSITION_DURATION = 6
    FPS = 60
    WINDOWED_SIZE = (1280, 720)

    def __init__(self, config: dict):
        pygame.font.init()
        pygame.mixer.init()
        self.phases = self._config_to_phases(config)

        self.sfx: list[Sfx] = [
            Sfx(pygame.K_e, "assets/sfx/evil-laugh.mp3"),
            Sfx(pygame.K_t, "assets/sfx/thunder.mp3"),
        ]

        # Window
        self.window_size = self.WINDOWED_SIZE
        self.screen = pygame.display.set_mode(self.WINDOWED_SIZE)
        pygame.display.set_caption("phusic")

        # Setup state
        self.phase_index = 0
        self.is_fading = False
        self.fade_step = 0
        self.is_fullscreen = False

        self.frames_for_transition = self.TRANSITION_DURATION * self.FPS
        self.fade_step_increment = self.TOTAL_FADE_STEPS / float(
            self.frames_for_transition
        )
        self.next_background = None

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self._initial_phase(self.phase_index)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self._toggle_fullscreen()

                    if event.key == pygame.K_SPACE:
                        self._next_phase()

                    for sfx in self.sfx:
                        if event.key == sfx.key:
                            sfx.sound.play()

            self._draw()
            clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def _config_to_phases(self, config: dict) -> list[Phase]:
        phases = []

        print(config)

        for phase in config["phases"]:
            phases.append(Phase(phase["name"], phase["audio"], phase["img"]))

        return phases

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.WINDOWED_SIZE)

        # Scale background
        self.window_size = self.screen.get_size()
        phase = self.phases[self.phase_index]
        self.background = pygame.image.load(phase.img).convert()
        self.background = pygame.transform.scale(self.background, self.window_size)

    def _initial_phase(self, phase_index):
        phase = self.phases[phase_index]
        phase.sound.play(-1)
        phase.sound.set_volume(1.0)
        self.background = pygame.image.load(phase.img).convert()
        self.background = pygame.transform.scale(self.background, self.window_size)

    def _next_phase(self):
        if self.is_fading:
            return

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
            alpha = int(self.fade_step * (255 / self.TOTAL_FADE_STEPS))
            self.next_background.set_alpha(alpha)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.next_background, (0, 0))
            new_volume = alpha / 255.0
            next_phase.sound.set_volume(new_volume)
            current_phase.sound.set_volume(1.0 - new_volume)
            self.fade_step += self.fade_step_increment

            if self.fade_step > self.TOTAL_FADE_STEPS:
                self.is_fading = False
                self.phase_index = (self.phase_index + 1) % len(self.phases)
                self.background = self.next_background
                current_phase.sound.stop()
        else:
            self.screen.blit(self.background, (0, 0))

        pygame.display.flip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start the game with a configuration file."
    )
    parser.add_argument(
        "--config", type=str, help="Path to configuration file", required=True
    )
    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = json.load(file)

    game = Game(config)
    game.run()
