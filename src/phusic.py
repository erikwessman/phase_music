import json
import pygame
import argparse
import sys
import random
from itertools import zip_longest
from typing import List

from phase import Phase
from ending import Ending
from sfx import Sfx
import util


class Game:
    TOTAL_FADE_STEPS = 255
    TRANSITION_DURATION = 2
    FPS = 60
    WINDOWED_SIZE = (1280, 720)
    FONT_SIZE = 36
    FONT_COLOR = (255, 255, 255)

    def __init__(self, config: dict):
        pygame.font.init()
        pygame.mixer.init()

        # Window
        self.window_size = self.WINDOWED_SIZE
        self.screen = pygame.display.set_mode(self.WINDOWED_SIZE)
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        pygame.display.set_caption("phusic")

        # Load stuff
        self.phases = self._get_phases(config)
        self.endings = self._get_endings(config)
        self.sfx = self._get_sfx(config)

        # Setup state
        self.fade_step = 0
        self.is_fading = False
        self.is_fullscreen = False

        self.curr_phase = util.create_linked_list(self.phases).head
        self.next_phase = None

        self.frames_for_transition = self.TRANSITION_DURATION * self.FPS
        self.fade_step_increment = self.TOTAL_FADE_STEPS / float(
            self.frames_for_transition
        )

    def run(self):
        clock = pygame.time.Clock()
        running = True
        self._initial_phase()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 or event.key == pygame.K_f:
                        self._toggle_fullscreen()

                    if event.key == pygame.K_LEFT:
                        self._change_phase(self.curr_phase.prev)

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                        self._change_phase(self.curr_phase.next)

                    if (
                        event.key == pygame.K_c
                        and pygame.key.get_mods() & pygame.KMOD_CTRL
                    ):
                        print("Shutting down")
                        exit(0)

                    for ending in self.endings:
                        if event.key == ending.key:
                            self._change_phase(ending)

                    for sfx in self.sfx:
                        if event.key == sfx.key:
                            sfx.sound.play()

            self._draw()
            clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def _get_phases(self, config: dict) -> list[Phase]:
        print("Loading phase assets...")

        phases = []

        for phase in config["phases"]:
            phase_instances = []

            audio_paths = util.get_files_from_path(phase["audio"])
            img_paths = util.get_files_from_path(phase["imgs"])

            shorter_list = (
                audio_paths if len(audio_paths) < len(img_paths) else img_paths
            )

            for audio, img, in zip_longest(
                audio_paths, img_paths, fillvalue=random.choice(shorter_list)
            ):
                phase_instances.append(Phase(phase["name"], audio, img))

            phases.append(phase_instances)

        ordered_phases = []
        max_length = max(len(p) for p in phases)

        for i in range(max_length):
            for phase in phases:
                phase_index = i % len(phase)
                ordered_phases.append(phase[phase_index])

        return ordered_phases

    def _get_endings(self, config: dict) -> List[Ending]:
        print("Loading ending assets...")

        endings = []

        for ending in config["endings"]:
            audio = random.choice(util.get_files_from_path(ending["audio"]))
            imgs = random.choice(util.get_files_from_path(ending["img"]))
            endings.append(
                Ending(getattr(pygame, ending["key"]), ending["name"], audio, imgs)
            )

        return endings

    def _get_sfx(self, config: dict) -> List[Sfx]:
        sfxs = []

        for sfx in config["sfx"]:
            sfxs.append(Sfx(getattr(pygame, sfx["key"]), sfx["audio"]))

        return sfxs

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.WINDOWED_SIZE)

        # Scale background
        self.window_size = self.screen.get_size()
        background = self.curr_phase.background
        background = pygame.transform.scale(background, self.window_size)

    def _initial_phase(self):
        self.curr_phase.sound.set_volume(1.0)
        self.curr_phase.sound.play(-1)
        self.curr_phase.background = pygame.transform.scale(
            self.curr_phase.background, self.window_size
        )

    def _change_phase(self, next_phase: Phase):
        if self.is_fading:
            return

        self.is_fading = True
        self.fade_step = 0
        self.next_phase = next_phase

        next_phase.sound.set_volume(0.0)
        next_phase.sound.play(-1)
        next_phase.background = pygame.transform.scale(
            next_phase.background, self.window_size
        )

    def _draw(self):
        curr_phase = self.curr_phase
        next_phase = self.next_phase

        if self.is_fading:
            # Handle fade background
            alpha = int(self.fade_step * (255 / self.TOTAL_FADE_STEPS))
            next_phase.background.set_alpha(alpha)
            self.screen.blit(curr_phase.background, (0, 0))
            self.screen.blit(next_phase.background, (0, 0))

            # Handle fade sound
            new_volume = alpha / 255.0
            next_phase.sound.set_volume(new_volume)
            curr_phase.sound.set_volume(1.0 - new_volume)

            self.fade_step += self.fade_step_increment

            if self.fade_step > self.TOTAL_FADE_STEPS:
                self.is_fading = False
                curr_phase.sound.stop()
                self.curr_phase = self.next_phase
        else:
            self.screen.blit(curr_phase.background, (0, 0))

        # Draw phase name
        text_position = (10 + self.FONT_SIZE, self.window_size[1] - self.FONT_SIZE - 10)
        self._draw_text(self.curr_phase.name, text_position)

        pygame.display.flip()

    def _draw_text(self, text, position):
        text_surface = self.font.render(text, True, self.FONT_COLOR)
        self.screen.blit(text_surface, position)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start the game with a configuration file."
    )
    parser.add_argument(
        "--config",
        default="configs/eldritch_horror.json",
        type=str,
        help="Path to configuration file",
    )
    args = parser.parse_args()

    with open(args.config, "r") as file:
        config = json.load(file)

    game = Game(config)
    game.run()
