from temdisponivellib.contracts import IDrawable
from temdisponivellib.component import Component
from temdisponivellib.loader import Loader
import pygame.transform


class SpriteRenderer(Component, IDrawable):
    """
    Class that holds a sprite that will be drawn into a surface.
    """

    def __init__(self, path=""):
        """
        The position of the sprite in screen will be the same as x and y of its game object.
        The area that will be draw will be always the whole surface, but the part that may be outside camera.
        Create a sprite renderer. If passed path parameter, this will load the image by its path
        (using Loader.load_image(path, true))
        :param path: Path of the sprite. If None or blank, nothing is  loaded.
        :return:
        """
        super(SpriteRenderer, self).__init__()
        self._image_path = path
        self._image = None
        self._rotated_image = None
        self._last_angle = 0

    def update(self):
        if self.transform.angle_local != self._last_angle:
            self._rotated_image = pygame.transform.rotate(self._image, self.transform.angle_local)
            self._last_angle = self.transform.angle_local

    @IDrawable.drawable.getter
    def drawable(self):
        if self._rotated_image is not None:
            return self._rotated_image
        return self._image

    def load(self):
        if self._image_path != "":
            self._image = Loader.load_image(self._image_path)[0]

    def unload(self):
        self._image = None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image