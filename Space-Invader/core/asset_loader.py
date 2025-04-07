import os
import pygame

# Paths relative to the project structure
ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

class AssetLoader:
    def __init__(self):
        self.assets = {}  # For images
        self.sounds = {}  # For sound effects

    def load_image(self, name, filename, scale=None):
        """
        Loads and caches an image. Optionally scales it.
        
        :param name: Key name to cache under
        :param filename: Filename inside /assets/
        :param scale: Tuple (width, height) if scaling is needed
        :return: pygame.Surface
        """
        if name in self.assets:
            return self.assets[name]

        path = os.path.join(ASSET_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)

        self.assets[name] = image
        return image

    def load_sound(self, name, filename):
        """
        Loads and caches a sound file.

        :param name: Key name to cache under
        :param filename: Filename inside /assets/sounds/
        :return: pygame.mixer.Sound
        """
        if name in self.sounds:
            return self.sounds[name]

        path = os.path.join(SOUND_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sound not found: {path}")

        sound = pygame.mixer.Sound(path)
        self.sounds[name] = sound
        return sound

    def get(self, name):
        """Get a previously loaded image by name."""
        return self.assets.get(name)

    def get_sound(self, name):
        """Get a previously loaded sound by name."""
        return self.sounds.get(name)