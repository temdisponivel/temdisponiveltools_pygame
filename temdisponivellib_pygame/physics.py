"""
This is a temporary class. In future, hopefully, we will integrate a physics engine (box2d most probably)
"""

from builtin_components.collider import Collider
from gameobject import IUpdatable
from gameobject import IDrawable
from game import Game
from configuration import Configuration
from gameobject import Component


class Physics(object, IUpdatable, IDrawable):

    """
    Class that handles some physics functions.
    """

    instance = None

    def __init__(self):
        if Physics.instance is None:
            Physics.instance = self
        else:
            pass
        self._draw_colliders = False
        self._active_collisions = {}

    def update(self):
        if Game.instance.frame_count % Configuration.instance.collision_check_rate == 0:
            self.check_collision()

    def draw(self):
        if not self.draw_colliders:
            pass
        colliders = Collider.get_colliders()
        for game_objects in colliders:
            pass

    def check_collision(self):
        """
        Collides all colliders that ara in same region
        :return:
        """
        colliders = Collider.get_colliders()
        for list_colliders in colliders:
            length = 0
            for i in range(length=len(list_colliders)):
                if i >= length:
                    break
                collider_a = list_colliders[i]
                collider_b = list_colliders[i + 1]
                key_a = (collider_a.game_object.id, collider_b.game_object.id)
                key_b = (collider_b.game_object.id, collider_a.game_object.id)
                if collider_a.check_collision(collider_b):
                    if key_a in self._active_collisions:
                        callback = "collision_stay"
                    elif key_b in self._active_collisions:
                        callback = "collision_stay"
                    else:
                        callback = "collision_enter"
                        self._active_collisions[key_a] = (collider_a, collider_b)
                else:
                    if key_a in self._active_collisions:
                        callback = "collision_exit"
                        del self._active_collisions[key_a]
                    elif key_b in self._active_collisions:
                        callback = "collision_exit"
                        del self._active_collisions[key_b]
                self._call_callback(callback, collider_a, collider_b)

    def _call_callback(self, callback, collider_a, collider_b, key):
        for cls in Component.get_class_by_callback(callback):
            comp_a = collider_a.get_component(cls)
            comp_b = collider_b.get_component(cls)
            if comp_a is not None:
                if callback == "collider_enter":
                    comp_a.collider_enter(collider_b)
                elif callback == "collider_stay":
                    comp_a.collider_stay(collider_b)
                elif callback == "collider_exit":
                    comp_a.collider_exit(collider_b)
            if comp_b is not None:
                if callback == "collider_enter":
                    comp_b.collider_enter(comp_a)
                elif callback == "collider_stay":
                    comp_b.collider_stay(comp_a)
                elif callback == "collider_exit":
                    comp_b.collider_exit(comp_a)

    @property
    def draw_colliders(self):
        return self._draw_colliders

    @property.setter
    def draw_colliders(self, draw):
        self._draw_colliders = draw

    @property
    def active_collision(self):
        """
        :return: A dict (key: game_object_a.id, game_object_b.id, value: game_object_a, game_object_b) containing
        all active collisions
        """
        return self._active_collisions