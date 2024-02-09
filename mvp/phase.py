import pygame
import sys


class Phase:
    def __init__(self, name: str, audio: str) -> None:
        self.name = name
        self.audio = audio
        self.sound = pygame.mixer.Sound(audio)


current_phase_index = 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Phase Transition")
font = pygame.font.Font(None, 36)
button = pygame.Rect(220, 190, 200, 100)

phases: list[Phase] = [
    Phase("Action", "audio/action.mp3"),
    Phase("Encounter", "audio/encounter.mp3"),
    # Phase("Mythos", "audio/mythos.mp3"),
]

phases[current_phase_index].sound.set_volume(1.0)

def play_next_phase():
    global current_phase_index
    current_phase = phases[current_phase_index]
    next_phase_index = (current_phase_index + 1) % len(phases)
    next_phase = phases[next_phase_index]

    for vol in range(10, -1, -1):
        current_phase.sound.set_volume(vol / 10.0)
        next_phase.sound.set_volume((10 - vol) / 10.0)
        pygame.time.delay(100)

    current_phase.sound.stop()
    next_phase.sound.play(-1)
    current_phase_index = next_phase_index


def main():
    running = True
    phases[current_phase_index].sound.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    play_next_phase()

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), button)
        text = font.render(phases[current_phase_index].name, True, (255, 255, 255))
        screen.blit(text, (button.x + 50, button.y + 40))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
