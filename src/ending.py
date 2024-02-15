from phase import Phase


class Ending(Phase):
    def __init__(self, key: int, name: str, audio_path: str, img_path: str):
        self.key = key
        super().__init__(name, audio_path, img_path)
