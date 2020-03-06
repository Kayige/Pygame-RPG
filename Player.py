import pygame 
import Constants
import random 
from Equipment import *
from Item import *

class Player(pygame.sprite.Sprite):
    def __init__(self, container_town, container_world, container_castle, equip_list, item_list, run):
        pygame.sprite.Sprite.__init__(self)
        self.container_town = container_town
        self.container_world = container_world
        self.container_castle = container_castle
        self.equip_list = equip_list
        self.item_list = item_list
        self.run = run
        self.speed = Constants.pix_sz * 0.125
        self.town_x = self.container_town.centerx
        self.town_y = self.container_town.height - 15 * Constants.pix_sz
        self.world_x = self.container_world.centerx
        self.world_y = self.container_world.height - 15 * Constants.pix_sz
        self.castle_x = self.container_castle.centerx
        self.castle_y = self.container_castle.height - 15 * Constants.pix_sz

        self.image = pygame.image.load(Constants.PLAYER)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.world_x
        self.rect.y = self.world_y

        self.color = Constants.GRAY

        self.location = "world"

        self.encounter_number = random.randrange(100, 150)

        self.gil = 1000
        self.equip_inventory = [self.equip_list[4], self.equip_list[4], self.equip_list[4],
                                self.equip_list[4], self.equip_list[-2], self.equip_list[-1]]
        self.item_inven = [2, 0, 0]

        print(self.equip_inventory)
        print(self.item_inven)

        self.forced_encounter = False

    def update(self, border_group, exit_group, loot_group, hero_list):
        # Reads player inputs out of battle
        if pygame.key.get_pressed:
            encounter = "no encounter"
            key = pygame.key.get_pressed()

            # Moves player on map
            if key[pygame.K_w]:
                self.move(border_group, exit_group, loot_group, "up")
                encounter = self.check_encounter()
            if key[pygame.K_s]:
                self.move(border_group, exit_group, loot_group, "down")
                encounter = self.check_encounter()
            if key[pygame.K_a]:
                self.move(border_group, exit_group, loot_group, "left")
                encounter = self.check_encounter()

            if key[pygame.K_d]:
                self.move(border_group, exit_group, loot_group, "right")
                encounter = self.check_encounter()

            # Opening menu
            if key[pygame.K_m]:
                print("Menu opened")
                self.run.menu_loop(self, hero_list)

            if self.location == "town":
                return "false"
            else:
                return encounter

    def move(self, border_group, exit_group, loot_group, direction):
        # Moves spaces based on player's speed
        if direction == "up":
            self.rect.y -= self.speed
        elif direction == "down":
            self.rect.y += self.speed
        elif direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

        # print("Location: " + str(self.rect.x / Constants.pix_sz) + " " + str(self.rect.y / Constants.pix_sz))
        # If player collides with a wall, move is undone
        if pygame.sprite.spritecollide(self, border_group, False):
            self.encounter_number += 1
            if direction == "up":
                self.rect.y += self.speed
            elif direction == "down":
                self.rect.y -= self.speed
            elif direction == "left":
                self.rect.x += self.speed
            elif direction == "right":
                self.rect.x -= self.speed

        # If player comes into contact with an exit (or goes out of town), goes to exit's destination
        if pygame.sprite.spritecollide(self, exit_group, False):
            ex = pygame.sprite.spritecollide(self, exit_group, False)[0]
            if ex.location == self.location:
                self.location = ex.destination
                self.rect.x = ex.dest_x
                self.rect.y = ex.dest_y
                print("warp")
        elif self.location == "town" and (not 15 * Constants.pix_sz < self.rect.x < 93 * Constants.pix_sz or not 9 * Constants.pix_sz < self.rect.y < 47 * Constants.pix_sz):
            self.location = "world"
            self.rect.x = 38 * Constants.pix_sz
            self.rect.y = 96 * Constants.pix_sz
            print("warp")

        # If player comes into contact with a loot chest, obtains loot
        if pygame.sprite.spritecollide(self, loot_group, False):
            l = pygame.sprite.spritecollide(self, loot_group, False)[0]
            # If in the same zone, adds item/equip to inventory
            if self.location == l.location:
                if l.unopened:
                    # If in castle, begins forced encounter
                    if self.location == "castle":
                        self.forced_encounter = True
                    self.run.textbox_prompt.prompt(["Obtained " + l.treasure.name + ".", "", "", "", "", "", "", ""])

                    if isinstance(l.treasure, Equipment):
                        print("Equipment obtained")
                        self.update_equipment(l.treasure, "add", None)
                    elif isinstance(l.treasure, Item):
                        print("Item obtained")
                        self.update_items(l.treasure, "add", None)

                    l.unopened = False
                else:
                    self.run.textbox_prompt.prompt(["The chest is empty.", "", "", "", "", "", "", ""])
                self.encounter_number += 1
                if direction == "up":
                    self.rect.y += self.speed
                elif direction == "down":
                    self.rect.y -= self.speed
                elif direction == "left":
                    self.rect.x += self.speed
                elif direction == "right":
                    self.rect.x -= self.speed

    def check_encounter(self):
        # If in a hostile area, encounters will randomly occur when the counter reaches 0
        if self.location == "world" or self.location == "castle":
            self.encounter_number -= 1
            # Random Encounter
            if self.encounter_number <= 0:
                if self.location == "world":
                    self.encounter_number = random.randrange(200, 600)
                elif self.location == "castle":
                    self.encounter_number = random.randrange(300, 700)
                print("Random encounter")
                return "random"

            # Forced Encounter
            elif self.forced_encounter:
                print("Forced encounter")
                return "forced"
            # Boss Encounter
            elif self.location == "castle" and 47.75 * Constants.pix_sz < self.rect.x < 60.25 * Constants.pix_sz and 26.0 * Constants.pix_sz < self.rect.y < 32.0 * Constants.pix_sz:
                print("Boss encounter")
                return "boss"
            else:
                return "no encounter"
        else:
            return "no encounter"

    def update_equipment(self, equip, variant, target):
        # Updates the player's equipment inventory, effects vary on variant
        # If equipment is dropped by enemies or found in chest
        if variant == "add":
            print("Obtained " + equip.name)
            self.equip_inventory += [equip]
        # If equipment is bought
        elif variant == "buy":
            if equip.buy_value < self.gil:
                self.equip_inventory += [equip]
                self.gil -= equip.buy_value
                print(equip.name + " bought.")
            else:
                print("You don't have enough gil!")
        # If equipment is equipped
        elif variant == "equip":
            no_weapon = self.equip_list[-2]
            no_armor = self.equip_list[-1]
            if target.variant in equip.can_equip:
                # If equipment is a weapon
                if equip.type == "weapon":
                    if target.weapon != no_weapon:
                        self.equip_inventory += [target.weapon]
                    target.weapon = equip
                # If equipment is armor
                elif equip.type == "armor":
                    if target.armor != no_armor:
                        self.equip_inventory += [target.weapon]
                    target.armor = equip
                if equip != "None":
                    self.equip_inventory -= [equip]
                target.hero.update_stats(target)
            # If equipment is not usable by character, item is not equipped
            else:
                print("Cannot be equipped by character's class")
        elif variant == "sell":
            self.equip_inventory -= [equip]
            self.gil += equip.sell_value

        lst = []
        for e in self.equip_inventory:
            lst += [e.name]
        print(lst)

    def update_items(self, item, variant, target):
        # Updates the player's item inventory, effects vary on variant
        # Item is added/subtracted to stock in inventory, position is needed for each stock
        if item.name == "Potion":
            i_pos = 0
        elif item.name == "Phoenix Down":
            i_pos = 1
        else:
            i_pos = 2

        # If item is dropped by enemies or found in chest
        if variant == "add":
            print("Obtained " + item.name)
            self.item_inven[i_pos] += 1
        # If item is bought
        elif variant == "buy":
            if item.buy_value < self.gil:
                self.item_inven[i_pos] += 1
                self.gil -= item.buy_value
                print(item.name + " bought.")
            else:
                print("You don't have enough gil!")
        elif variant == "consume":
            if self.item_inven[i_pos] >= 1:
                self.item_inven[i_pos] -= 1
                item.use_item(target)
            else:
                print("No more " + item.name + "s in inventory")
        elif variant == "sell":
            self.item_inven[i_pos] -= 1
            self.gil += item.sell_value

        print(self.item_inven)
