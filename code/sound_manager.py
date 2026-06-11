import pygame
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = self.load_sounds()

    def load_sounds(self):
        # Load all sounds into a dictionary
        sounds = {
            "achievement": self.load_sound("pictures/actual/game sounds/standard/achievement.mp3"),
            "capture": self.load_sound("pictures/actual/game sounds/standard/capture.mp3"),
            "castle": self.load_sound("pictures/actual/game sounds/standard/castle.mp3"),
            "click": self.load_sound("pictures/actual/game sounds/standard/click.mp3"),
            "correct": self.load_sound("pictures/actual/game sounds/standard/correct.mp3"),
            "decline": self.load_sound("pictures/actual/game sounds/standard/decline.mp3"),
            "drawoffer": self.load_sound("pictures/actual/game sounds/standard/drawoffer.mp3"),
            "event_end": self.load_sound("pictures/actual/game sounds/standard/event-end.mp3"),
            "event_start": self.load_sound("pictures/actual/game sounds/standard/event-start.mp3"),
            "event_warning": self.load_sound("pictures/actual/game sounds/standard/event-warning.mp3"),
            "game_draw": self.load_sound("pictures/actual/game sounds/standard/game-draw.mp3"),
            "game_end": self.load_sound("pictures/actual/game sounds/standard/game-end.mp3"),
            "game_lose": self.load_sound("pictures/actual/game sounds/standard/game-lose.mp3"),
            "game_lose_long": self.load_sound("pictures/actual/game sounds/standard/game-lose-long.mp3"),
            "game_start": self.load_sound("pictures/actual/game sounds/standard/game-start.mp3"),
            "game_win": self.load_sound("pictures/actual/game sounds/standard/game-win.mp3"),
            "game_win_long": self.load_sound("pictures/actual/game sounds/standard/game-win-long.mp3"),
            "illegal": self.load_sound("pictures/actual/game sounds/standard/illegal.mp3"),
            "incorrect": self.load_sound("pictures/actual/game sounds/standard/incorrect.mp3"),
            "lesson_fail": self.load_sound("pictures/actual/game sounds/standard/lesson-fail.mp3"),
            "lesson_pass": self.load_sound("pictures/actual/game sounds/standard/lesson-pass.mp3"),
            "move_check": self.load_sound("pictures/actual/game sounds/standard/move-check.mp3"),
            "move_opponent": self.load_sound("pictures/actual/game sounds/standard/move-opponent.mp3"),
            "move_self": self.load_sound("pictures/actual/game sounds/standard/move-self.mp3"),
            "notification": self.load_sound("pictures/actual/game sounds/standard/notification.mp3"),
            "notify": self.load_sound("pictures/actual/game sounds/standard/notify.mp3"),
            "premove": self.load_sound("pictures/actual/game sounds/standard/premove.mp3"),
            "promote": self.load_sound("pictures/actual/game sounds/standard/promote.mp3"),
            "puzzle_correct": self.load_sound("pictures/actual/game sounds/standard/puzzle-correct.mp3"),
        }
        return sounds

    def load_sound(self, file_path):
        # Helper to load individual sound, handle exceptions if file is missing
        try:
            return pygame.mixer.Sound(file_path)
        except pygame.error as e:
            print(f"Error loading sound file '{file_path}': {e}")
            return None

    def play(self, sound_name):
        # Play sound if it exists in the dictionary
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()
        else:
            print(f"Sound '{sound_name}' not found or failed to load.")

    def stop(self, sound_name):
        # Stop a specific sound if it is playing
        sound = self.sounds.get(sound_name)
        if sound:
            sound.stop()
        else:
            print(f"Sound '{sound_name}' not found or failed to load.")

    def stop_all(self):
        # Stop all sounds
        pygame.mixer.stop()
