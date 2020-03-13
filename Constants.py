import os
import pygame

current_path = os.path.dirname(__file__) # Where your .py file is located
image_path = os.path.join(current_path, 'images') # The resource folder path

pix_sz = 32
font_sz = pix_sz * 2 / 3
win_w = 16 * pix_sz
win_h = 22 * pix_sz
mar_1 = pix_sz * 0.5
mar_2 = pix_sz * 1
fps = 60

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (192, 192, 192)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (216, 216, 0)
LIGHT_GREEN = (128, 255, 128)
GREEN = (0, 255, 0)
LIGHT_BLUE = (128, 128, 255)
BLUE = (64, 64, 255)
LIGHT_BROWN = (255, 255, 0)
BROWN = (128, 128, 0)

# src
BG = os.path.join(image_path, "background.png")
CHEST = os.path.join(image_path, "Chest.png")
TANK = os.path.join(image_path, "Tank.png")
WARRIOR = os.path.join(image_path, "Warrior.png")
MAGE = os.path.join(image_path, "Mage.png")
HEALER = os.path.join(image_path, "Healer.png")
WOLF = os.path.join(image_path, "Wolf.png")
GHOUL = os.path.join(image_path, "Ghoul.png")
GOBLIN = os.path.join(image_path, "Goblin.png")
SKELETON = os.path.join(image_path, "Skeleton.png")
OGRE = os.path.join(image_path, "Ogre.png")
GARGOYLE = os.path.join(image_path, "Gargoyle.png")
BOSS = os.path.join(image_path, "Skeleton_King.png")
PLAYER = os.path.join(image_path, "Tank_Player.png")
