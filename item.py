import random
import time
import os

class Item:
    def __init__(self, name, weight, description, item_type):
        self.name = name
        self.weight = weight
        self.description = description
        self.item_type = item_type

    def describe(self):
        print(f"Item: {self.name}")
        print(f"Description: {self.description}")
        print(f"Weight: {self.weight} kg")
        print(f"Item Type: {self.item_type}")

    def use(self, player):
        print(f"{player.name} tried to use this item but it did nothing.")


class Medicine(Item):
    def __init__(self, name, weight, description, heal_amount):
        super().__init__(name, weight, description, item_type="Medicine")
        self.heal_amount = heal_amount

    def use(self, player):
        print(f"You used the {self.name}. It healed {self.heal_amount} of your health.")
        player.heal(self.heal_amount)


class Weapon(Item):
    def __init__(self, name, weight, description, damage):
        super().__init__(name, weight, description, item_type="Weapon")
        self.damage = damage

    def use(self, player):
        if player.weapon != "Fists":
            print(f"You unequipped {player.weapon}.")
        print(f"You equipped the {self.name}.")
        player.strength = self.damage
        player.weapon = self.name