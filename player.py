import random
import time
import os
from item import Item, Medicine, Weapon

class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.weapon = "Fists"
        self.strength = 10
        self.inventory = []
        self.total_weight = 0
        self.weight_limit = 15000
    
    def unequip_weapon(self):
        if self.weapon == "Fists":
            print("You have no weapon equipped.")
            return
        old_weapon = self.weapon
        self.weapon = "Fists"
        self.strength = 10
        print(f"You unequipped {old_weapon}, now left with only your bare fists.")

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"You healed {amount} health. Current health: {self.health}")

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.die()
        else:
            print(f"You took {amount} damage! Current health: {self.health}")

    def die(self):
        death_message_num = random.randint(1,5)
        os.system("clear")
        if death_message_num == 1:
            print("""You lay on the ground. 
                  Your breathing starts to become increasingly shaky and your vision starts to falter. 
                  Your short life flashes by your eyes as you bleed. 
                  You accept your fate as you breathe your last.""")
        elif death_message_num == 2:
            print("""Life slowly fades from you with each passing moment.
                  Darkness closes in on your vision as you gradually, painfully lose your strenght
                  Your breathing abruptly stops, leaving only silence.""")
        elif death_message_num == 3:
            print("""Weakness overtakes you step by step.
                  Your breath grows shallow, and vision fades.
                  You can fight no longer, as you meet your end.""")
        elif death_message_num == 4:
            print("""Your body trembles as your wounds take their toll.
                  Your breath becomes shallow, your vision dimming with each passing second.
                  The world slips away, and soon your consciousness fades into nothing.""")
        elif death_message_num == 5:
            print("""Blood stains your hands and clothes as strength fades from your limbs.
                  Your breath comes in ragged gasps, each one harder than the last.
                  The world blurs as you collapse, never to get back up.""")
        time.sleep(3)
        exit("""
▓██   ██▓ ▒█████   █    ██    ▓█████▄  ██▓▓█████ ▓█████▄ 
 ▒██  ██▒▒██▒  ██▒ ██  ▓██▒   ▒██▀ ██▌▓██▒▓█   ▀ ▒██▀ ██▌
  ▒██ ██░▒██░  ██▒▓██  ▒██░   ░██   █▌▒██▒▒███   ░██   █▌
  ░ ▐██▓░▒██   ██░▓▓█  ░██░   ░▓█▄   ▌░██░▒▓█  ▄ ░▓█▄   ▌
  ░ ██▒▓░░ ████▓▒░▒▒█████▓    ░▒████▓ ░██░░▒████▒░▒████▓ 
   ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒     ▒▒▓  ▒ ░▓  ░░ ▒░ ░ ▒▒▓  ▒ 
 ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░     ░ ▒  ▒  ▒ ░ ░ ░  ░ ░ ▒  ▒ 
 ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░     ░ ░  ░  ▒ ░   ░    ░ ░  ░ 
 ░ ░         ░ ░     ░           ░     ░     ░  ░   ░    
 ░ ░                           ░                  ░      """)

    def attack(self):
        print(f"You attack with {self.weapon} for {self.strength} damage!")
        return self.strength

    def add_to_inventory(self, item):
        if self.total_weight + item.weight <= self.weight_limit:
            self.inventory.append(item)
            self.total_weight += item.weight
            print(f"You picked up {item.name}.")
        else:
            print(f"You couldn't pick up{item.name}, being unable to bear the weight of all your items.")

    def use_item(self, item):
        print(f"You tried to use the {item.name}.")
        time.sleep(1)
        item.use(self)

    def drop_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.total_weight -= item.weight
            print(f"You dropped {item.name}.")
        else:
            print("You don't have that item on you.")

    def describe_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            os.system("clear")
            print("Your inventory contains:")
            for item in self.inventory:
                print(f"{item.name}, weighing {item.weight}g")
            print(f"The total weight of your items is: {self.total_weight}/{self.weight_limit}g.")