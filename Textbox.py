import pygame
import sys
import time
from Text import *
import Constants

class Textbox:
    def __init__(self, run, x, y, w, h, align):
        self.run = run
        self.color = Constants.BLUE
        self.image = pygame.Surface((w, h))
        self.image.convert()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.align = align
        self.text_list = []

        # Assigns coordinates of textbox based on alignment
        for line in range(0, 8):
            if self.align == "left":
                text = Text(Constants.font_sz, "", "left", x + Constants.mar_1,
                            y + Constants.mar_1 + Constants.font_sz * line, Constants.WHITE)
            else:
                text = Text(Constants.font_sz, "", "center", self.rect.centerx,
                            self.rect.y + Constants.mar_1 + Constants.font_sz * line, Constants.WHITE)
            self.text_list += [text]

    def prompt(self, new_text_list):
        # Produces a prompt that must be exited out of by pressing space
        self.update(new_text_list)
        while True:
            for event in pygame.event.get():
                # Allows the red button to function
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    # Space = return
                    if event.key == pygame.K_SPACE:
                        return 0
            self.textbox_blit()

    def message(self, new_text_list):
        # Produces a message that closes after a certain amount of time
        length = 2
        self.update(new_text_list)
        self.textbox_blit()
        time.sleep(length)

    def update(self, new_text_list):
        # Updates text in box
        for line in range(0, len(new_text_list) - 1):
            self.text_list[line].update_text(new_text_list[line])
            if self.text_list[line].align == "center":
                self.text_list[line].rect.centerx = self.rect.centerx
                
    def textbox_blit(self):
        # Renders all images of textbox
        self.run.screen.blit(self.image, self.rect)
        for line in self.text_list:
            self.run.screen.blit(line.image, line.rect)
        # Writes to main surface
        pygame.display.flip()