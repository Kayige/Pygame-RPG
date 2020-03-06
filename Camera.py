import pygame 
import Constants

class Camera:
    def __init__(self, container_town, container_world, container_castle):
        self.x_offset = 0
        self.y_offset = 0
        self.container_town = container_town
        self.container_world = container_world
        self.container_castle = container_castle

    def update(self, player, container):
        self.x_offset = - player.rect.centerx + Constants.win_w / 2
        self.y_offset = - player.rect.centery + Constants.win_h / 2

        # Limit at borders
        if self.x_offset < -(container.width - Constants.win_w):
            self.x_offset = -(container.width - Constants.win_w)
        elif self.x_offset > 0:
            self.x_offset = 0
        if self.y_offset < -(container.height - Constants.win_h):
            self.y_offset = -(container.height - Constants.win_h)
        elif self.y_offset > 0:
            self.y_offset = 0

    def apply(self, obj):
     return obj.rect.move((self.x_offset, self.y_offset))