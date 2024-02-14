import os
import json
import pygame
import argparse
import sys
from typing import List


class Phase:
    def __init__(self, name: str, audio: List[str], imgs: List[str]) -> None:
        self.name = name
        self.sound = None
        self.background = None
        self._iteration = 0

        self._initialize_assets(audio, imgs)
        self._update_phase()

    def next_iteration(self):
        self._iteration += 1
        self._update_phase()

    def prev_iteration(self):
        self._iteration -= 1
        self._update_phase()

    def _initialize_assets(self, audio: List[str], imgs: List[str]):
        print(f"Loading {self.name} assets...")

        self._audio = []
        for a in audio:
            self._audio.append(pygame.mixer.Sound(a))

        self._imgs = []
        for i in imgs:
            self._imgs.append(pygame.image.load(i))

    def _update_phase(self):
        self.sound = self._audio[self._iteration % len(self._audio)]
        self.background = self._imgs[self._iteration % len(self._imgs)]


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
    FONT_SIZE = 24
    FONT_COLOR = (255, 255, 255)

    def __init__(self, config: dict):
        pygame.font.init()
        pygame.mixer.init()

        # Window
        self.window_size = self.WINDOWED_SIZE
        self.screen = pygame.display.set_mode(self.WINDOWED_SIZE)
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        pygame.display.set_caption("phusic")

        self.phases = self._get_phases(config)
        self.endings = self._get_endings(config)
        self.sfx = self._get_sfx(config)

        # Setup state
        self.fade_step = 0
        self.is_fading = False
        self.is_fullscreen = False

        self.curr_phase_index = 0
        self.next_phase_index = 0

        self.frames_for_transition = self.TRANSITION_DURATION * self.FPS
        self.fade_step_increment = self.TOTAL_FADE_STEPS / float(
            self.frames_for_transition
        )

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self._initial_phase(self.curr_phase_index)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self._toggle_fullscreen()

                    if event.key == pygame.K_LEFT:
                        next_phase_index = (
                            self.curr_phase_index - 1) % len(self.phases)
                        self._change_phase(next_phase_index)

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                        next_phase_index = (
                            self.curr_phase_index + 1) % len(self.phases)
                        self._change_phase(next_phase_index)

                    for sfx in self.sfx:
                        if event.key == sfx.key:
                            sfx.sound.play()

            self._draw()
            clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def _get_phases(self, config: dict) -> list[Phase]:
        phases = []

        for phase in config["phases"]:
            audio = self._get_files_from_path(phase["audio"])
            imgs = self._get_files_from_path(phase["imgs"])
            phases.append(Phase(phase["name"], audio, imgs))

        return phases

    def _get_endings(self, config: dict) -> list[Phase]:
        endings = []

        for phase in config["endings"]:
            audio = self._get_files_from_path(phase["audio"])
            imgs = self._get_files_from_path(phase["imgs"])
            endings.append(Phase(phase["name"], audio, imgs))

        return endings

    def _get_sfx(self, config: dict) -> dict:
        sfxs = []
        for key, sfx_path in config["sfx"].items():
            if not os.path.exists(sfx_path):
                print(f"Sfx {sfx_path} does not exist")
                continue

            sfxs.append(Sfx(getattr(pygame, key), sfx_path))
        return sfxs

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.WINDOWED_SIZE)

        # Scale background
        self.window_size = self.screen.get_size()
        phase = self.phases[self.curr_phase_index]
        phase.background = pygame.transform.scale(
            phase.background, self.window_size)

    def _initial_phase(self, phase_index):
        phase = self.phases[phase_index]
        phase.sound.set_volume(1.0)
        phase.sound.play(-1)
        phase.background = pygame.transform.scale(
            phase.background, self.window_size)

    def _change_phase(self, next_phase_index: int):
        if self.is_fading:
            return

        self.is_fading = True
        self.fade_step = 0

        self.next_phase_index = next_phase_index

        phase = self.phases[next_phase_index]

        phase.sound.set_volume(0.0)
        phase.sound.play(-1)
        phase.background = pygame.transform.scale(
            phase.background, self.window_size
        )

    def _draw(self):
        curr_phase = self.phases[self.curr_phase_index]

        if self.is_fading:
            next_phase = self.phases[self.next_phase_index]

            # Handle next background
            alpha = int(self.fade_step * (255 / self.TOTAL_FADE_STEPS))
            next_phase.background.set_alpha(alpha)
            self.screen.blit(curr_phase.background, (0, 0))
            self.screen.blit(next_phase.background, (0, 0))

            # Handle next sound
            new_volume = alpha / 255.0
            next_phase.sound.set_volume(new_volume)
            curr_phase.sound.set_volume(1.0 - new_volume)

            self.fade_step += self.fade_step_increment

            if self.fade_step > self.TOTAL_FADE_STEPS:
                self.is_fading = False
                self.curr_phase_index = self.next_phase_index
                curr_phase.sound.stop()
                curr_phase.next_iteration()
        else:
            self.screen.blit(curr_phase.background, (0, 0))

        # Draw phase name
        phase_name = curr_phase.name
        text_position = (10, self.window_size[1] - self.FONT_SIZE - 10)
        self._draw_text(phase_name, text_position)

        pygame.display.flip()

    def _get_files_from_path(self, path: str):
        full_paths = []
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isfile(full_path):
                full_paths.append(full_path)
        return full_paths

    def _draw_text(self, text, position):
        text_surface = self.font.render(text, True, self.FONT_COLOR)
        self.screen.blit(text_surface, position)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start the game with a configuration file."
    )
    parser.add_argument(
        "--config", default="configs/eldritch_horror.json", type=str, help="Path to configuration file"
    )
    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = json.load(file)

    game = Game(config)
    game.run()
