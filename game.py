import pygame
import sys
import time
import os
import random
import math

import Constants
from Textbox import *
from Pointer import *
from Platform import *
from Exit import *
from Loot import *
from Camera import *
from Player import *
from Hero import *
from CharacterHero import *
from Spell import *
from SpellVariant import *
from Enemy import *
from GoblinEnemy import *
from WolfEnemy import *
from OgreEnemy import *
from GhoulEnemy import *
from SkeletonEnemy import *
from GargoyleEnemy import *
from BossEnemy import *
from NoneEnemy import *

# Forces static position of screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

class Game:
   def __init__(self, frames):
       self.fps = frames
       self.screen = pygame.display.set_mode((Constants.win_w, Constants.win_h), pygame.SRCALPHA)
       self.beginning = self.running = self.ending = True
       self.clock = pygame.time.Clock()
       self.clock.tick(self.fps)
       image = pygame.image.load(Constants.BG)
       self.screen.blit(image, [0, 0])
       self.title = Text(Constants.win_h / 12, "--Click Here--",
                            "center", Constants.win_w / 2, Constants.win_h * 0.8, Constants.BLACK)
       self.end_title_win = Text(
           Constants.win_h / 6, "You Win!", "center", Constants.win_w / 2, Constants.win_h / 2 - 192, Constants.WHITE)
       self.end_title_lose = Text(
           Constants.win_h / 6, "You Lost", "center", Constants.win_w / 2, Constants.win_h / 2 - 192, Constants.WHITE)
       self.end_subtitle = Text(
           Constants.win_h / 12, "--Click to Close--", "center", Constants.win_w / 2, Constants.win_h / 2 + 64, Constants.WHITE)
       self.textbox_prompt = Textbox(self, 0, 0, Constants.win_w, Constants.pix_sz * 2, "center")
       self.textbox_top = Textbox(self, 0, 0, Constants.win_w, Constants.pix_sz * 2, "left")
       self.textbox_middle = Textbox(
           self, 0, Constants.pix_sz * 4, Constants.win_w, Constants.pix_sz * 13, "left")
       textbox_0 = Textbox(self, Constants.win_w * 0, Constants.win_h - Constants.pix_sz *
                           6, Constants.win_w * 0.16, Constants.pix_sz * 6, "left")
       textbox_1 = Textbox(self, Constants.win_w * 0.16, Constants.win_h -
                           Constants.pix_sz * 6, Constants.win_w * 0.24, Constants.pix_sz * 6, "left")
       textbox_2 = Textbox(self, Constants.win_w * 0.40, Constants.win_h -
                           Constants.pix_sz * 6, Constants.win_w * 0.24, Constants.pix_sz * 6, "left")
       self.textbox_health = Textbox(
           self, Constants.win_w * 0.64, Constants.win_h - Constants.pix_sz * 6, Constants.win_w * 0.36, Constants.pix_sz * 6, "left")
       self.textbox_combat_list = [textbox_0,
           textbox_1, textbox_2, self.textbox_health]
       self.textbox_menu_list = [textbox_0, textbox_1, textbox_2, self.textbox_health,
                                 self.textbox_prompt, self.textbox_middle]
       self.pointer = Pointer(Constants.WHITE)
       self.pointer_2 = Pointer(Constants.WHITE)

   def create_plat(self, x, y, name, location):
       p = Platform(x, y, name, location)
       # Platforms for town
       if location == "town":
           if name == (" " or "T" or "D" or "P" or "W"):
               p = Platform(x, y, name, location)
           # Loot
           elif name == "L":
               print("Loot: " + str(x / Constants.pix_sz) + " " + str(y / Constants.pix_sz))
       # Platforms for world
       elif location == "world":
           if name == (" " or "G" or "F" or "R" or "D" or "P"):
               p = Platform(x, y, name, location)
           # Town
           elif name == "T":
               print("Town: " + str(x / Constants.pix_sz) + " " + str(y / Constants.pix_sz))
           # Castle
           elif name == "C":
               print("Castle: " + str(x / Constants.pix_sz) + " " + str(y / Constants.pix_sz))
           # Loot
           elif name == "L":
               print("Loot: " + str(x / Constants.pix_sz) + " " + str(y / Constants.pix_sz))
       # Platforms for castle
       elif location == "castle":
           if name == " " or "W":
               p = Platform(x, y, name, location)
           # Loot
           elif name == "L":
               print("Loot: " + str(x / Constants.pix_sz) + " " + str(y / Constants.pix_sz))
           # Exit
           elif name == "E":
               print("Exit: " + str(x / Constants.pix_sz) + " " + str(y / Constants.pix_sz))
       return p

   def text_blit(self, obj_list):
       # Renders each obj given, if they have a surface and rect
       for obj in obj_list:
           if len(obj) > 1:
               # If an argument is given, make the object blink
               if obj[1] == 1:
                   if (pygame.time.get_ticks() % 1000) < 500:
                       self.screen.blit(obj[0].image, obj[0].rect)
           else:
               self.screen.blit(obj[0].image, obj[0].rect)

   def determ_enemies(self, player, enemy, enemy_list, plat_group_w, encounter_type):
       # Depending on the location of the player, enemies are assigned to enemy_list
       if player.location == "world":
           p = pygame.sprite.spritecollide(player, plat_group_w, False)
           number = random.randrange(1, 6)
           print("Random number: " + str(number))
           # Grass Map enemies
           if p[0].variant == "grass" or p[0].variant == "path":
               if number == 1:
                   enemy_list = [GoblinEnemy(enemy, 1),
                                 GoblinEnemy(enemy, 2),
                                 GoblinEnemy(enemy, 3)]
               elif number == 2:
                   enemy_list = [WolfEnemy(enemy, 1),
                                 WolfEnemy(enemy, 2),
                                 WolfEnemy(enemy, 3)]
               elif number == 3:
                   enemy_list = [GoblinEnemy(enemy, 1),
                                 GoblinEnemy(enemy, 2),
                                 GoblinEnemy(enemy, 3)]
               elif number == 4:
                   enemy_list = [GoblinEnemy(enemy, 1),
                                 OgreEnemy(enemy, 2),
                                 GoblinEnemy(enemy, 3)]
               elif number == 5:
                   enemy_list = [GoblinEnemy(enemy, 1),
                                 GoblinEnemy(enemy, 2),
                                 GoblinEnemy(enemy, 3)]
           elif p[0].variant == "forest":
                   if number == 1:
                       enemy_list = [GoblinEnemy(enemy, 1),
                                     GoblinEnemy(enemy, 2),
                                     GoblinEnemy(enemy, 3)]
                   elif number == 2:
                       enemy_list = [WolfEnemy(enemy, 1),
                                     WolfEnemy(enemy, 2),
                                     WolfEnemy(enemy, 3)]
                   elif number == 3:
                       enemy_list = [WolfEnemy(enemy, 1),
                                     WolfEnemy(enemy, 2),
                                     GoblinEnemy(enemy, 3)]
                   elif number == 4:
                       enemy_list = [GoblinEnemy(enemy, 1),
                                     OgreEnemy(enemy, 2),
                                     GoblinEnemy(enemy, 3)]
                   elif number == 5:
                       enemy_list = [GoblinEnemy(enemy, 1),
                                     GoblinEnemy(enemy, 2),
                                     GoblinEnemy(enemy, 3)]
           elif p[0].variant == "dirt":
                   if number == 1:
                       enemy_list = [
                           GhoulEnemy(enemy, 1),
                           GhoulEnemy(enemy, 2),
                           GhoulEnemy(enemy, 3)]
                   elif number == 2:
                       enemy_list = [SkeletonEnemy(enemy, 1),
                                     SkeletonEnemy(enemy, 2),
                                     SkeletonEnemy(enemy, 3)]
                   elif number == 3:
                       enemy_list = [OgreEnemy(enemy, 1),
                                     OgreEnemy(enemy, 2),
                                     GoblinEnemy(enemy, 3)]
                   elif number == 4:
                       enemy_list = [WolfEnemy(enemy, 1),
                                     WolfEnemy(enemy, 2),
                                     WolfEnemy(enemy, 3)]
                   elif number == 5:
                       enemy_list = [GoblinEnemy(enemy, 1),
                                     GoblinEnemy(enemy, 2),
                                     GoblinEnemy(enemy, 3)]
       elif player.location == "castle":
                   # If in final-boss room, loads encounter for final boss
                   if encounter_type == "boss":
                       enemy_list = [
                           GoblinEnemy(enemy, 1),
                           BossEnemy(enemy, 2),
                           GoblinEnemy(enemy, 3)]
                   # If chest is opened, force encounter
                   elif encounter_type == "forced":
                       enemy_list = [
                           SkeletonEnemy(enemy, 1),
                           SkeletonEnemy(enemy, 2),
                           SkeletonEnemy(enemy, 3)]
                   else:
                       number = random.randrange(1, 4)
                       print("Random number: " + str(number))
                       if number == 1:
                           enemy_list = [
                               GhoulEnemy(enemy, 1),
                               GhoulEnemy(enemy, 2),
                               GhoulEnemy(enemy, 3)]
                       elif number == 2:
                           enemy_list = [
                               SkeletonEnemy(enemy, 1),
                               SkeletonEnemy(enemy, 2),
                               SkeletonEnemy(enemy, 3)]
                       elif number == 3:
                           enemy_list = [
                               GargoyleEnemy(enemy, 1),
                               GargoyleEnemy(enemy, 2),
                               GargoyleEnemy(enemy, 3)]
       return enemy_list

   def combat_loop(self, player, hero_list, enemy, old_enemy_list, plat_group_w, encounter_type):
       # Runs a loop of combat where player selects actions, and combat continues until one side falls
       # Selections are Attack, Defend, Spells, Items, and Run
       enemy_list = self.determ_enemies(
           player, enemy, old_enemy_list, plat_group_w, encounter_type)

       print("Enemies: " + enemy_list[0].name +
             enemy_list[1].name + enemy_list[2].name)

       result = False
       encounter = True

       while encounter:
           # For all entities that are not downed, allows turn to be taken
           active_entities = []
           for c in hero_list:
               c.hero.check_health(c, hero_list)
               if not c.downed:
                   # If character is not downed, allows selection of character's actions
                   print("Selection: " + str(c.name))
                   active_entities += [c]
                   hero_name_list = []

                   for ch in hero_list:
                       hero_name_list += [ch.name]

                   enemy_obj_list = []
                   enemy_name_list = []

                   for e in enemy_list:
                       if not e.downed:
                           enemy_obj_list += [e]
                           enemy_name_list += [e.name]

                   spell_obj_list = []
                   spell_name_list = []

                   for s in c.spell_list:
                       if s == "None":
                           spell_obj_list += ["None"]
                           spell_name_list += ["None"]
                       else:
                           if s.targets == "ally":
                               spell_obj_list += [[s, hero_list]]
                               spell_name_list += [[s.name, hero_name_list]]
                           elif s.targets == "enemy":
                               spell_obj_list += [[s, enemy_list]]
                               spell_name_list += [[s.name, enemy_name_list]]

                   item_obj_list = []
                   for i in player.item_list:
                       item_obj_list += [[i, hero_name_list]]
                   g_obj = [c.name, [["Attack", enemy_obj_list],
                                        ["Defend"],
                                        ["Spells", spell_obj_list],
                                        ["Items", item_obj_list],
                                        ["Run"]]]
                   g_name = [c.name, [["Attack", enemy_name_list],
                                         ["Defend"],
                                         ["Spells", spell_name_list],
                                         ["Items", [["H. Pot.       " + str(player.item_inven[0]), hero_name_list],
                                                    ["P. Down  " +
                                                        str(player.item_inven[1]), hero_name_list],
                                                    ["E. Pot. " + str(player.item_inven[2]), hero_name_list]]],
                                         ["Run"]]]

                   output = self.selection(
                       player, hero_list, enemy_list, "combat", g_obj, g_name, c, 0, [0, 0, 0, 0])

                   c.update_selection(output)

                   if output[0][0] == 1:
                       c.defend_bonus = 75
                       c.defend_dura = 1
               else:
                   print(c.name + " is downed.")

           for e in enemy_list:
               if not e.downed:
                   active_entities += [e]

           turn_order = random.sample(active_entities, len(active_entities))

           for entity in turn_order:
               empty_text_list = ["", "", "", "", "", "", "", ""]
               for box in range(0, 3):
                   self.textbox_combat_list[box].update(empty_text_list)
               # Characters and enemies take their turn in a random order
               if isinstance(entity, CharacterHero):
                   entity.shift(Constants.pix_sz * (-2), hero_list, enemy_list)
                   response = entity.hero.attack(
                       player, entity, hero_list, enemy_list)
                   entity.shift(Constants.pix_sz * 2, hero_list, enemy_list)
                   if response == "run success":
                       for c in hero_list:
                           c.shift(Constants.pix_sz * 8, hero_list, enemy_list)
                       self.textbox_prompt.prompt(
                           ["The party successfully ran away.", "", "", "", "", "", "", ""])
                       return "Ran away"
               else:
                   entity.enemy.shift(Constants.pix_sz * 2, hero_list,
                                      enemy_list, entity)
                   entity.enemy.attack(entity, hero_list)
                   entity.enemy.shift(
                       Constants.pix_sz * (-2), hero_list, enemy_list, entity)
               result = self.determ_encounter_end(hero_list, enemy_list)
               if result != "false":
                   encounter = False
                   break

           for c in hero_list:
               c.hero.check_buffs(c)

       # Checks if result of encounter is a win or loss, gives rewards if a win
       if result == "win":
           print("Encounter has been won")
           self.combat_rewards(hero_list, enemy_list, player)
           return "win"
       else:
           print("Encounter has been lost")
           print("Game Over")
           return "lose"

   def determ_encounter_end(self, hero_list, enemy_list):
       # Determines if encounter is over, and returns which side wins
       # If all characters are downed, return "lose"
       if hero_list[0].downed and hero_list[1].downed and hero_list[2].downed and hero_list[3].downed:
           return "lose"
       # If all enemies are downed, return "win"
       elif enemy_list[0].downed and enemy_list[1].downed and enemy_list[2].downed:
           return "win"
       # If encounter is not over, return false
       else:
           return "false"

   def combat_rewards(self, hero_list, enemy_list, player):
       # Handles exp and gil gained, also handles character level-ups
       print("Distributing combat rewards.")
       gained_gil = 0
       gained_exp = 0

       for e in enemy_list:
           gained_gil += random.randrange(int(e.gil_drop * 0.7),
                                          int(e.gil_drop * 1.3))

           gained_exp += random.randrange(int(e.exp_drop * 0.7),
                                          int(e.exp_drop * 1.3))

       print("Obtained " + str(gained_gil) + " gil.")
       player.gil += gained_gil
       print("Gil: " + str(player.gil))
       self.textbox_prompt.prompt(
           ["Obtained " + str(gained_gil) + " gil.", "", "", "", "", "", "", ""])
       self.textbox_prompt.prompt(
           ["Obtained " + str(gained_exp) + " exp.", "", "", "", "", "", "", ""])

       # Adds exp to all characters that are not downed
       for c in hero_list:
           if not c.downed:
               c.exp += gained_exp
           print(c.name + " exp: " + str(c.exp))
           # If character's exp exceeds or meets required amount, character levels up
           if c.exp >= c.exp_needed:
               c.level += 1
               print(c.name + " is now level " + str(c.level) + "!")
               self.textbox_prompt.prompt(
                   [c.name + " is now level " + str(c.level) + "!", "", "", "", "", "", "", ""])
               c.multiplier = c.multiplier * 1.1
               c.exp -= c.exp_needed
               c.exp_needed += 50
               c.hero.update_stats(c)

       # Updates equip and/or items if they are dropped
       # Randomly distributes equipment
       chance = random.random() * 100

       if 0 <= chance < 10:
           drop = random.sample(player.equip_list, 1)[0]
           print("Obtained " + drop.name + ".")
           self.textbox_prompt.prompt(
               ["Obtained " + drop.name + ".", "", "", "", "", "", "", ""])
           player.equip_inventory += drop
       elif 10 <= chance <= 30:
           drop = random.sample(player.item_list, 1)[0]
           print("Obtained " + drop.name)
           self.textbox_prompt.prompt(
               ["Obtained " + drop.name + ".", "", "", "", "", "", "", ""])
           if drop.name == "Potion":
               player.item_inven[0] += 1
           if drop.name == "Phoenix Down":
               player.item_inven[1] += 1
           if drop.name == "Energy Potion":
               player.item_inven[2] += 1

       print("Exiting combat.")

   def menu_loop(self, player, hero_list):
       # Pause Menu, out of combat
       # Selections are Stats, Equipment, Spells, Items, and Tips
       print("Selection: Pause Menu")
       hero_name_list = []
       spell_obj_list = []
       spell_name_list = []

       for c in hero_list:
           hero_name_list += [c.name]
           for spell in c.spell_list:
               if isinstance(spell, SpellVariant):
                if spell.out_of_combat:
                   spell_obj_list += [[spell, hero_list]]
                   spell_name_list += [[spell.name, hero_name_list]]

       equip_obj_list = []
       equip_name_list = []

       for eq in player.equip_list:
           equip_obj_list += [eq]
           equip_name_list += [eq.name]

       item_obj_list = []
       for i in player.item_list:
           item_obj_list += [[i, hero_name_list]]

       g_obj = ["Select Action:", [["Stats", hero_list],
                                   ["Equip", equip_obj_list],
                                   ["Spells", spell_obj_list],
                                   ["Items", item_obj_list],
                                   ["Tips"]]]

       g_name = ["Select Action:", [["Stats", hero_name_list],
                                    ["Equip", equip_name_list],
                                    ["Spells", spell_name_list],
                                    ["Items", ["Potion        " + str(player.item_inven[0]),
                                               "Phoenix Down  " + str(player.item_inven[1]),
                                               "Energy Potion " + str(player.item_inven[2])]],
                                    ["Tips"]]]

       # Player remains in menu until pressing "b"
       while True:
           turn_output = self.selection(player, hero_list, None, "pause", g_obj, g_name, None, 0, [0, 0, 0, 0])
           if turn_output == "false":
               return 0
           else:
               pos_list = turn_output[0]

   def selection(self, player, hero_list, enemy_list, variant, g_obj, g_name, source, iteration, pos_list):
       # Command for navigating menu
       pos = 0
       new_text_list = []

       for line in range(0, 8):
           if line == 0:
               new_text_list += [g_name[0] + ":"]
           elif len(g_name[1]) >= line:
               if isinstance(g_name[1][line - 1], list):
                   new_text_list += [g_name[1][line - 1][0]]
               else: # isinstance(g_name[1][line - 1], basestring):
                   new_text_list += [g_name[1][line - 1]]
           else:
               new_text_list += [""]
       print(new_text_list)

       empty_text_list = ["", "", "", "", "", "", "", ""]

       # Sets initial text and cursor positions
       self.textbox_combat_list[iteration].update(new_text_list)

       for box in range(iteration + 1, 3):
           self.textbox_combat_list[box].update(empty_text_list)

       self.pointer.update(self.textbox_combat_list[iteration].text_list[pos + 1].rect.x - Constants.pix_sz * .5,
                           self.textbox_combat_list[iteration].text_list[pos + 1].rect.centery)

       # Initial render
       self.screen.fill(Constants.WHITE)

       if variant == "combat":
           for textbox in self.textbox_combat_list:
               textbox.textbox_blit()

           for c in hero_list:
               self.screen.blit(c.image, c.rect)

           for e in enemy_list:
               if not e.downed:
                    self.screen.blit(e.image, e.rect)
       # Blits all textboxes to fill screen with menu
       else:
           for textbox in self.textbox_menu_list:
               textbox.textbox_blit()

       self.screen.blit(self.pointer.image, self.pointer.rect)

       # Writes to main surface
       pygame.display.flip()

       # Grid is a list of lists, denoting positions on the UI
       # Checks inputs, updates UI based on responses
       print(g_name[0])
       print(g_name[1][pos][0])

       while True:
           for event in pygame.event.get():
               # Allows the Constants.RED button to function
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       sys.exit()

                   if event.key == pygame.K_w:
                       pos -= 1
                       if pos < 0:
                           pos = len(g_obj[1]) - 1
                       print(g_name[1][pos][0])
                       self.pointer.update(self.textbox_combat_list[iteration].text_list[pos + 1].rect.x - Constants.pix_sz * .5,
                                           self.textbox_combat_list[iteration].text_list[pos + 1].rect.centery)

                   if event.key == pygame.K_s:
                       pos += 1
                       if pos > len(g_obj[1]) - 1:
                           pos = 0
                       print(g_name[1][pos][0])
                       self.pointer.update(self.textbox_combat_list[iteration].text_list[pos + 1].rect.x - Constants.pix_sz * .5,
                                           self.textbox_combat_list[iteration].text_list[pos + 1].rect.centery)

                   if event.key == pygame.K_b:
                       if iteration > 0 or variant != "combat":
                           return "false"
                       else:
                           print("Cannot go back")
                   # Space = select, returns action and target

                   if event.key == pygame.K_SPACE:
                       # If list is detected, further goes to select targets
                       if len(g_name[1][pos]) > 1 and type(g_name[1][pos]) is list:
                           if type(g_obj[1][pos][0]) is Spell and source.spell_list[pos].cost > source.energy:
                               print("Not enough mana.")
                           elif type(g_obj[1][pos][0]) is Item and player.item_inven[pos] <= 0:
                               print("None available.")
                           else:
                               output = self.selection(player, hero_list, enemy_list, variant, g_obj[1][pos],
                                                       g_name[1][pos], source, iteration + 1, pos_list)
                               if output != "false":
                                   new_pos_list = output[0]
                                   new_pos_list[iteration] = pos
                                   return new_pos_list, g_obj, g_name
                               else:
                                   empty_text_list = ["", "", "", "", "", "", "", ""]

                                   # Sets initial text and cursor positions
                                   self.textbox_combat_list[iteration].update(new_text_list)

                                   for box in range(iteration + 1, 3):
                                       self.textbox_combat_list[box].update(empty_text_list)

                                   self.pointer.update(
                                       self.textbox_combat_list[iteration].text_list[pos + 1].rect.x - Constants.pix_sz * .5,
                                       self.textbox_combat_list[iteration].text_list[pos + 1].rect.centery)
                       # Unselectable option
                       elif g_name[1][pos] == "None":
                           print("Option cannot be selected.")
                       # If no other options, returns values
                       else:
                           new_pos_list = pos_list
                           new_pos_list[iteration] = pos
                           print(new_pos_list)
                           return new_pos_list, g_obj, g_name
                   # Render game
                   self.screen.fill(Constants.WHITE)
                   if variant == "combat":
                       for textbox in self.textbox_combat_list:
                           textbox.textbox_blit()

                       for c in hero_list:
                           self.screen.blit(c.image, c.rect)

                       for e in enemy_list:
                           if not e.downed:
                                self.screen.blit(e.image, e.rect)
                   # Blits all textboxes to fill screen with menu
                   else:
                       for textbox in self.textbox_menu_list:
                           textbox.textbox_blit()

                   self.screen.blit(self.pointer.image, self.pointer.rect)

                   # Writes to main surface
                   pygame.display.flip()

def main():
   pygame.display.set_caption("Turn Based RPG")
   run = Game(Constants.fps)

   # Local variables
   result = "false"

   # Town: " " = grass, T = tree, D = dirt, P = path, W = wall, L = loot, E = exit
   town = [
       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                            ",

       "                                                                                                             ",

       "                 WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W                                  L                                      W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W           P                                                 P           W                 ",

       "                 W           P                                                 P           W                 ",

       "                 W        PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP        W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W               P                                         P               W                 ",

       "                 W           P   P                                         P   P           W                 ",

       "                 W           P   P                                         P   P           W                 ",

       "                 W        PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP        W                 ",

       "                 W                                    P                                    W                 ",

       "                 W                               T    P    T                               W                 ",

       "                 W                                    P                                    W                 ",

       "                 W                               T    P    T                    T          W                 ",

       "                 W      T   T                         P                      T             W                 ",

       "                 W    T                          T    P    T                      T        W                 ",

       "                 W        T                           P                        T           W                 ",

       "                 W                               T    P    T                               W                 ",

       "                 W                                    P                                    W                 ",

       "                 WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  P  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                 ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             "]

   # Level: " " = water, G = grass, F = forest, R = rock, D = dirt, P = path, T = town, C = castle, L = loot
   world = [
       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                 DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                 ",

       "                 DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                 ",

       "                                          DDDDDDDDDDDDDDDDDD                                                 ",

       "                                      DDDDDDDDDDDDDDDDDDDDDDDDDDD                                            ",

       "                                   DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                          ",

       "                                DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                       ",

       "                               DDDDDDDDDDDDDDDDDDDDCDDDDDDDDDDDDDDDDDD                                       ",

       "                              DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                    ",

       "                             DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                   ",

       "                             DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                ",

       "                             DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                   ",

       "                             DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                  ",

       "                             DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                   ",

       "                             DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                     ",

       "                              DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                     ",

       "                               DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                     ",

       "                                DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                       ",

       "                             DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                   ",

       "                            DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                            ",

       "                            DDDDDDDDDDDDDDDDDGGGDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDGGGG                           ",

       "                             DDDDDDDDDDDGGGGGGGGGGGGGGGGGDDDDDDDDDDDDDDDDDDDDGGGGGGGG                        ",

       "                           GGGGGDDDDGGGGGGGGGGGGGGGGGGGGGGGGGGDDDDGGGGGGGGGGGGGGGGGGG                        ",

       "                         GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDGGGGGGGGGGGGGGG                            ",

       "                         GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                              ",

       "                         GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                ",

       "                     GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                               ",

       "                   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                               ",

       "                   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                            ",

       "                    GGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGRRRRRRRRRRRR                        ",

       "                   GGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGRRRRRRRRRRRRRRRR                     ",

       "                    GGGGRRRRRRRRRRRRRRRRRGGGGGGGGGGGGRRRRRRRRRRGGGGGGGRRRRRRRRRRRRRRRRRRR                    ",

       "                    GGGGGGRRRRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRR                     ",

       "                   GGGGGRRRRRRRRRRRRGGGGGGRRRRGGGGGRRRRRGGGGGGGGGRRRRRRRRGGRRRRRRRRRRRRR                     ",

       "                    GGGGRRRRRRRRRRRRGGGGRRRRRRGGGGRRRRRRRRRRRRRRRRRRRRRGGGGGGGGRRRRRRRRRR                    ",

       "                    GGGGGGRRRRRRRRRRRRRRRRRRRRGGGRRRRRRRRRRRRRRRRRRRRRGGGGGGGGRRRRRRRRR                      ",

       "                   GGGGGRRRRRRRRRRRRRRRRRRRRRGGGGRRRRRRRRRRRRRRRRRRRRRGGGGGRRRRRRRRRRRRR                     ",

       "                    GGGGRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGRRRRRRRRRRRRRRGGGGRRRRRRRRRRRRRRRR                    ",

       "                     GGGGRRRRRRRRRRRRRRRRRGGGGRRRGGGGGGGGGGGRRRRRRGGGGGGRRRRRRRRRRRRRRRRR                    ",

       "                     GGGGGGRRRRRRRRRRRRRRGGGGRRRRRRRRRRGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRR                   ",

       "                      GGGGGRRRRRRRRRRRRRRGGRRRRRRRRRRRRRRGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRR                    ",

       "                      GGLGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGRRRRRRRRRRRRRRRRRRRRRRRR                     ",

       "                     GGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGRRRRRRRRRRRRRRRRRRRRRR                       ",

       "                      GGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGRRRRRRRRRRRRRRRR                             ",

       "                                        RRRRRRRRRRRRRRRRRRGGGGGGGGRRRRRRRRR                                  ",

       "                                                          GGGGGGGG                                           ",

       "                                     GGG                  GGGGGGGGG                                          ",

       "                                   GGGGGGGGGG      GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                          ",

       "                        GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGG                    ",

       "                   GGGGGGGGGGGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGG                 ",

       "                 GGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGG                 ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                   ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                 ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                   ",

       "                 GGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGG                 ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGGGGG                   ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGGGG                 ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                   ",

       "                   GGGGGGGFGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                        ",

       "                   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                ",

       "                     GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                    ",

       "                      GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGGGG                                                 ",

       "                      GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGG                                                    ",

       "                     GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFG                                                      ",

       "                   GGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGGGG                                                ",

       "                    GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGG                                            ",

       "                     GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGG                                        ",

       "                      GGGFFFFFFFFFFFFFFFFFFGFFFFFFFFFFFFFFFFFFFFFFFFFGGGGGGG                                 ",

       "                         GFFFFFFFFFFFFFFFFGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGG                              ",

       "                          GFFFFFFFFFFFFFFFGGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGG                            ",

       "                          GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGG                        ",

       "                         GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGFFFFFFFFFFFFFFFGGG                       ",

       "                     GGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGFFFFFFFFFFFFFGGGGGGGG                    ",

       "                  GGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGGGGGGGGGGG                   ",

       "                 GGGGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGGGGGGGGGGGGGGGGGG                  ",

       "                 GGGGGGGGFFFFFFFFFFFFFFFFFFFFFFGGFFFFFFFFFFFFFFFFFFFFGGGGGGGGGGGGGGGGGGGGGG                  ",

       "                 GGGGGGGGGGGGGGGGFFFFFFFFFFFFFGGGGGGFFFFFFFFFFFGGGGGGGGGGGGGGGGGGGGGGGGGGG                   ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                     ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                         ",

       "                 GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                            ",

       "                  GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                            ",

       "                  GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                           ",

       "                   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                          ",

       "                   GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                           ",

       "                     GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                           ",

       "                      GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                              ",

       "                        GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                 ",

       "                         GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                     ",

       "                         GGGGGGGGGGGGGTGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                         ",

       "                          GGGGGGGGGGGGGGGGGGGGGGGGGGGGG        GGGGGG                                        ",

       "                           GG  GGGGGGGGGGGGG                    GGGGGG                                       ",

       "                            GG   GGGGGGGGGG                        GGGG                                      ",

       "                             GGG  GGGGGGGGG                          G                                       ",

       "                                   GGGGGGG                                                                   ",

       "                                     GGGGGGG                                                                 ",

       "                                       GGGGGGGG                                                              ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             "]

   # Castle: " " = floor, W = wall, L = loot, E = exit
   castle = [
       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                 WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                 ",

       "                 W                      W                           W                      W                 ",

       "                 W                      W                           W                      W                 ",

       "                 W                      WWWWWWWWWWWWWWWWWWWWWWWWWWWWW                      W                 ",

       "                 W   WWWWWWWWWWWWWWWW                                   WWWWWWWWWWWWWWWW   W                 ",

       "                 W   W           L  W                                   W  L           W   W                 ",

       "                 W   W              W                                   W              W   W                 ",

       "                 W   W              W             W       W             W              W   W                 ",

       "                 W   W              W             W       W             W              W   W                 ",

       "                 W   W              W             W       W             W              W   W                 ",

       "                 W   WWWW  WWWWWWWWWWWWWWWWWWWWWWWW       WWWWWWWWWWWWWWWWWWWWWWWW  WWWW   W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW   W                 ",

       "                 W   W                         W             W                         W   W                 ",

       "                 W   W                         W      E      W                         W   W                 ",

       "                 W   W                         W             W                         W   W                 ",

       "                 W   W                         W             W                         W   W                 ",

       "                 W   W                         W             W                         W   W                 ",

       "                 W   W                         W             W                         W   W                 ",

       "                 W   W                         W             W                         W   W                 ",

       "                 W   W                         WWWWWW   WWWWWW                         W   W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W   W                                                                 W   W                 ",

       "                 W   W                                                                 W   W                 ",

       "                 W   W                                                                 W   W                 ",

       "                 W   WWWWWWWWWWWW   WWWWWWWWWWWWWWW       WWWWWWWWWWWWWWW   WWWWWWWWWWWW   W                 ",

       "                 W                                W       W                                W                 ",

       "                 W                                W       W                                W                 ",

       "                 W                                W       W                                W                 ",

       "                 W   WWWWWWWWWWWWWWWW                                   WWWWWWWWWWWWWWWW   W                 ",

       "                 W   W           L  W                                   W  L           W   W                 ",

       "                 W   W              W                                   W              W   W                 ",

       "                 W   W              W             W       W             W              W   W                 ",

       "                 W   W              W             W       W             W              W   W                 ",

       "                 W   W              W             W       W             W              W   W                 ",

       "                 W   WWWW  WWWWWWWWWWWWWWWWWWWWWWWW       WWWWWWWWWWWWWWWWWWWWWWWW  WWWW   W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 W                                                                         W                 ",

       "                 WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                 ",

       "                                                    W   W                                                    ",

       "                                                    W   W                                                    ",

       "                                                    W   W                                                    ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             ",

       "                                                                                                             "]

   town_w = len(town[0]) * Constants.pix_sz
   town_h = len(town) * Constants.pix_sz
   world_w = len(world[0]) * Constants.pix_sz
   world_h = len(world) * Constants.pix_sz
   castle_w = len(castle[0]) * Constants.pix_sz
   castle_h = len(castle) * Constants.pix_sz

   # Objects

   # Weapons
   broadsword = Equipment("Broadsword", "weapon", 15, 5, 1000, [0])
   saber = Equipment("Saber", "weapon", 20, 0, 900, [0, 1])
   nunchucks = Equipment("Nunchucks", "weapon", 20, 5, 500, [2])
   staff = Equipment("Staff", "weapon", 10, 0, 200, [0, 1, 2, 3, 4, 5])
   dagger = Equipment("Dagger", "weapon", 5, 0, 50, [0, 1, 2, 3, 4, 5])
   ph_we = Equipment("No Weapon", "weapon", 0, 0, 0, [0, 1, 2, 3, 4, 5])

   # Armor
   plate_armor = Equipment("Plate Armor", "armor", 0, 30, 1000, [0])
   leather_armor = Equipment("Leather Armor", "armor", 0, 15, 600, [0, 1, 2])
   cloth_robes = Equipment("Cloth Armor", "armor", 0, 10, 300, [0, 1, 2, 3, 4, 5])
   ph_ar = Equipment("No Armor", "armor", 0, 0, 0, [0, 1, 2, 3, 4, 5])
   equip_list = [broadsword, saber, nunchucks, staff, dagger, plate_armor, leather_armor, cloth_robes, ph_we, ph_ar]

   # Items
   potion = Item("Potion", "health", 40, 50, "Heals 40 HP")
   phoenix_down = Item("Phoenix Down", "greater_health", 1, 500, "Revives Downed Party Members")
   energy_potion = Item("Energy Potion", "energy", 25, 50, "Recovers 25 Energy")
   item_list = [potion, phoenix_down, energy_potion]

   # Spells
   spell = Spell(run)

   # Constants.WHITE Magic
   cure = SpellVariant(spell, "Cure", "heal", 1, "ally", 3, -30, True, "Heals One Ally")
   protect = SpellVariant(spell, "Protect", "buff", 1, "ally", 3, 30, False, "Raises DEF of One Ally (3 Turns)")
   heal = SpellVariant(spell, "Heal", "heal_all", 1, "ally", 8, -30, True, "Heals All Allies")
   dia = SpellVariant(spell, "Dia", "attack_all", 1, "enemy", 3, 50, False, "Deals Damage to All Undead Foes")

   # Constants.BLACK Magic
   fire = SpellVariant(spell, "Fire", "attack", 2, "enemy", 3, 50, False, "Deals Damage to One Enemy")
   temper = SpellVariant(spell, "Temper", "buff", 2, "ally", 3, 30, False, "Raises ATK of One Ally (3 Turns)")
   weaken = SpellVariant(spell, "Weaken", "debuff", 2, "enemy", 3, 30, False, "Lowers ATK of One Enemy (3 Turns)")
   fira = SpellVariant(spell, "Fira", "attack_all", 2, "enemy", 8, 100, False, "Deals Damage to All Enemies")
   spell_list = [cure, protect, heal, dia, fire, temper, weaken, fira]

   # [health, energy, attack, %defense, use_magic, usable_equipment]

   # use_magic: 0 = none, 1 = Constants.WHITE, 2 = Constants.BLACK, 3 = all
   class_list = [[100, 0, 25, 30, 0], [75, 0, 35, 20, 0],
                 [90, 0, 30, 30, 0], [70, 30, 15, 5, 1],
                 [60, 25, 15, 5, 2], [55, 25, 15, 5, 3]]

   container_town = pygame.Rect(0, 0, town_w, town_h)
   container_world = pygame.Rect(0, 0, world_w, world_h)
   container_castle = pygame.Rect(0, 0, castle_w, castle_h)
   camera = Camera(container_town, container_world, container_castle)
   player = Player(container_town, container_world, container_castle, equip_list, item_list, run)

   # Create groups
   hero = Hero(equip_list, run)
   hero_1 = CharacterHero("Tank", 0, 1, class_list, spell_list, run, hero, Constants.TANK)
   hero_2 = CharacterHero("Warrior", 1, 2, class_list, spell_list, run, hero, Constants.WARRIOR)
   hero_3 = CharacterHero("Mage", 4, 3, class_list, spell_list, run, hero, Constants.MAGE)
   hero_4 = CharacterHero("Healer", 3, 4, class_list, spell_list, run, hero, Constants.HEALER)
   hero_list = [hero_1, hero_2, hero_3, hero_4]

   enemy = Enemy(run)
   enemy_1 = GoblinEnemy(enemy, 1)
   enemy_2 = GoblinEnemy(enemy, 2)
   enemy_3 = GhoulEnemy(enemy, 3)
   enemy_list = [enemy_1, enemy_2, enemy_3]

   # Platforms/exits/loot for town
   plat_group_t = pygame.sprite.Group()
   bord_group_t = pygame.sprite.Group()

   x = y = 0
   print("Town:")
   for row in town:
       for column in row:
           p = run.create_plat(x, y, column, "town")
           plat_group_t.add(p)
           if p.variant == "wall":
               bord_group_t.add(p)
           x += Constants.pix_sz
       y += Constants.pix_sz
       x = 0

   loot_t_1 = Loot(87, 9, "town", broadsword)

   # Platforms/exits/loot for world
   plat_group_w = pygame.sprite.Group()
   bord_group_w = pygame.sprite.Group()
   x = y = 0
   print("World:")
   for row in world:
       for column in row:
           p = run.create_plat(x, y, column, "world")
           plat_group_w.add(p)
           if p.variant == "wall":
               bord_group_w.add(p)
           x += Constants.pix_sz
       y += Constants.pix_sz
       x = 0

   exit_w_1 = Exit(51, 14, "castle", 54, 53, "world")
   exit_w_2 = Exit(38, 95, "town", 54, 44, "world")
   loot_w_1 = Loot(24, 48, "world", phoenix_down)

   # Platforms/exits/loot for castle
   plat_group_c = pygame.sprite.Group()
   bord_group_c = pygame.sprite.Group()
   x = y = 0
   print("Castle:")
   for row in castle:
       for column in row:
           p = run.create_plat(x, y, column, "castle")
           plat_group_c.add(p)
           if p.variant == "wall":
               bord_group_c.add(p)
           x += Constants.pix_sz
       y += Constants.pix_sz
       x = 0

   exit_c_1 = Exit(53, 55, "world", 51, 16, "castle")
   exit_c_2 = Exit(54, 55, "world", 51, 16, "castle")
   exit_c_3 = Exit(55, 55, "world", 51, 16, "castle")

   loot_c_1 = Loot(33, 45, "castle", dagger)
   loot_c_2 = Loot(75, 45, "castle", plate_armor)
   loot_c_3 = Loot(33, 16, "castle", saber)
   loot_c_4 = Loot(75, 16, "castle", potion)

   container = camera.container_world

   plat_group = plat_group_w
   bord_group = bord_group_w

   exit_group = pygame.sprite.Group()
   exit_group.add(exit_w_1, exit_w_2, exit_c_1, exit_c_2, exit_c_3)

   loot_group = pygame.sprite.Group()
   loot_group.add(loot_t_1, loot_w_1, loot_c_1, loot_c_2, loot_c_3, loot_c_4)

   while True:
       run.beginning = run.running = run.ending = True

       # Runs Intro
       while run.beginning:
           # Read inputs
           for event in pygame.event.get():
               # Allows the Constants.RED button to function
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       sys.exit()
               # Exit loop
               if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE] != 0:
                   run.beginning = False
           # Render Title
           run.text_blit([[run.title, 1]])

           # Writes to main surface
           pygame.display.flip()

       # Runs Game
       while run.running:
           # Read inputs
           for event in pygame.event.get():
               # Allows the Constants.RED button to function
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       sys.exit()

           if player.location == "town":
               container = camera.container_town
               plat_group = plat_group_t
               bord_group = bord_group_t
           elif player.location == "world":
               container = camera.container_world
               plat_group = plat_group_w
               bord_group = bord_group_w
           elif player.location == "castle":
               container = camera.container_castle
               plat_group = plat_group_c
               bord_group = bord_group_c

           # Update
           encounter = player.update(bord_group, exit_group, loot_group, hero_list)
           camera.update(player, container)

           if encounter == "random" or encounter == "forced" or encounter == "boss":
               print("Starting encounter")
               result = run.combat_loop(player, hero_list, enemy, enemy_list, plat_group_w, encounter)
               if result == "lose" or encounter == "boss":
                   run.running = False
           # Render game
           run.screen.fill(Constants.WHITE)

           for p in plat_group:
               run.screen.blit(p.image, camera.apply(p))
           for ex in exit_group:
               if ex.location == player.location:
                   run.screen.blit(ex.image, camera.apply(ex))
           for l in loot_group:
               if l.location == player.location:
                   run.screen.blit(l.image, camera.apply(l))

           run.screen.blit(player.image, camera.apply(player))

           # Writes to main surface
           pygame.display.flip()

       # Runs ending
       while run.ending:
           # Read inputs
           for event in pygame.event.get():
               # Allows the Constants.RED button to function
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               elif event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_ESCAPE:
                       sys.exit()
               # Exits loop
               if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] or pygame.key.get_pressed()[pygame.K_SPACE] != 0:
                   run.ending = False

           # Render ending
           run.screen.fill(Constants.BLACK)
           if result == "win":
               run.text_blit([[run.end_title_win], [run.end_subtitle, 1]])
           else:
               run.text_blit([[run.end_title_lose], [run.end_subtitle, 1]])

           # Writes to main surface
           pygame.display.flip()

       break

if __name__ == "__main__":
 main()
