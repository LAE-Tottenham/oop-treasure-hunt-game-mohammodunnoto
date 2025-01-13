import random
import time
import os
from threading import Timer
from player import Player
from enemy import Enemy
from item import Item, Medicine, Weapon

class Place:
    def __init__(self, name, description, enemies):
        self.name = name
        self.description = description
        self.enemies = enemies
        self.exploration_count = 0  
        self.available_items = []

    def add_item(self, item):
        self.available_items.append(item)
        print(f"Item {item.name} has been added to the {self.name}.")

    def explore(self, player):
        print(f"\nYou are now in the {self.name}.")
        time.sleep(1)
        print(self.description)
        while True:
            action = input(f"Do you want to explore the area, manage your inventory or go ahead?:\n").lower()
            if action == "explore":
                if not self.available_items:
                    print("You explored so thoroughly there is nothing left to find.")
                else:
                    print(f"\nYou explore the {self.name} and find something...")
                    item = self.available_items.pop()
                    print(f"You found a {item.name}!")
                    player.add_to_inventory(item)
            elif action == "go ahead" or action == "go":
                print(f"You move on to the next area.")
            elif action == "manage inventory":
                manage_inventory(player)
                break
            else:
                print("You can't do that. Just pick one of the options.")

def fight(enemy, player):
    print(f"A wild {enemy.name} appears!")
    time.sleep(1)

    while enemy.health > 0 and player.health > 0:
        enemy.speak()

        # Player's action
        print("\nWhat would you like to do?")
        print("1. Attack")
        print("2. Use Item")
        action = input("Choose an action (1/2):\n").strip()

        if action == "1":
            damage = player.attack()
            enemy.take_damage(damage)

            if enemy.health <= 0:
                break  # Exit the fight loop if the enemy dies
            print(f"\n{enemy.name} has {enemy.health} health left.")
        elif action == "2":
            if not player.inventory:
                print("Your inventory is empty.")
                continue

            print("\nYour inventory:")
            for i, item in enumerate(player.inventory):
                print(f"{i + 1}. {item.name}")
            
            while True:
                item_choice = input("\nWhich item would you like to use? (Enter the number): ").strip()
                if item_choice.isdigit():
                    item_choice = int(item_choice) - 1
                    if 0 <= item_choice < len(player.inventory):
                        item = player.inventory[item_choice]
                        player.use_item(item)
                        break
                    else:
                        print("Please choose a valid item from the list.")
                else:
                    print("Please enter a valid number.")

        # Check if enemy is defeated
        if enemy.health <= 0:
            enemy.die()
            if enemy.is_boss and enemy.key_item:
                print(f"You obtained the {enemy.key_item}!")
                player.add_to_inventory(Item(name=enemy.key_item, weight=1, description="A key item."))
            return True

        print(f"{enemy.name} attacks you!")
        damage_taken = enemy.damage

        timeout = 1
        t = Timer(timeout, print, ["You missed your chance to react!"])
        t.start()
        start_time = time.time()
        prompt = f"You have {timeout} seconds to react. Press ENTER...\n"
        input(prompt)
        t.cancel()
        reaction_time = time.time() - start_time

        if reaction_time <= 0.5:
            print("You parried the attack! No damage taken.")
            damage_taken = 0
        elif reaction_time <= 1:
            print("You blocked the attack and reduced damage!")
            damage_taken *= 0.2
        else:
            print("You failed to react in time!")

        player.take_damage(int(damage_taken))
        if player.health <= 0:
            player.die()

    return False

def post_boss_prompt(player, key_item_name, area):
    while True:
        print(f"\nYou have obtained the {key_item_name}. What would you like to do?")
        print("1. Use the key to proceed to the next area.")
        print("2. Explore the current area further.")
        choice = input("Choose an action (1/2):\n").strip()

        if choice == "1":
            print(f"\nYou used the {key_item_name} to unlock the path to the next area.")
            break
        elif choice == "2":
            print("\nYou decide to explore the area again.")
            area.explore(player)
        else:
            print("That is not a valid option.")

def manage_inventory(player):
    if player.total_weight > player.weight_limit:
        print(f"\nYour inventory weight exceeds the limit ({player.total_weight}/{player.weight_limit}). You need to drop an item.")
        for i, item in enumerate(player.inventory):
            print(f"{i + 1}. {item.name} - {item.weight} kg")
        while True:
            item_choice = input("\nWhich item would you like to drop? (Enter the number):\n")
            if item_choice.isdigit():
                item_choice = int(item_choice) - 1
                if 0 <= item_choice < len(player.inventory):
                    item_to_drop = player.inventory[item_choice]
                    player.drop_item(item_to_drop)
                    print(f"You dropped {item_to_drop.name}.")
                    return
                else:
                    print("Please choose a valid item.")
            else:
                print("Invalid input. Please enter a number.")
    else:
        print("\nYour inventory weight is within the limit.")
    
    while True:
        print("\nYour inventory:")
        if player.inventory:
            for idx, item in enumerate(player.inventory):
                print(f"{idx + 1}. {item.name} - {item.description}")
        else:
            print("Your inventory is empty.")

        print("\nOptions:")
        print("1. Use or equip an item")
        print("2. Unequip weapon")
        print("3. Back to exploring")
        
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            while True:
                item_choice = input("\nWhich item would you like to use/equip? (Enter the number): ")
                if item_choice.isdigit():
                    item_choice = int(item_choice) - 1
                    if 0 <= item_choice < len(player.inventory):
                        item = player.inventory[item_choice]

                        if isinstance(item, Weapon):
                            item.use(player)
                            print(f"You have equipped {item.name}. Your strength is now {player.strength}.")
                        else:
                            player.use_item(item)
                        break
                print("Please choose a valid item.")

        elif choice == "2":
            player.unequip_weapon()
        
        elif choice == "3":
            print("Returning to exploration...")
            break

        else:
            print("Invalid choice. Please try again.")

    
print("""You wake up with a start. Cold dirt beneath you. The smell of damp earth in the air. 
          Your head aches, and your thoughts are clouded. You don’t know how long you’ve been unconscious, or even where you are. 
          The only thing you know for sure is that you’re not at home.""")
time.sleep(3)
print("""You sit up slowly, looking around. The trees rise like giants, their twisted branches blocking most of the light from the sky.
          A thick mist clings to the ground, swirling as though the forest itself is breathing.
          You have no idea how you ended up here — not even how you got knocked out. One moment, you were going about your life, the next you woke up.""")
time.sleep(3)
print("""With no memory of what happened, no clear direction, you have no idea what to do.
          The first thing you notice is the silence. There are no animals chirping, no insects buzzing. It’s as if the entire forest is holding its breath.
          You stand up, feeling disoriented, but something urges you forward. You take a step into the mist, left with no other conclusion about what to do.""")
name = input("\nYour head aches immensely but you hope it will go away with time. What was your name again:\n")
player = Player(name)
print("\nYeah, that was your name. Here starts your journey.")

place1 = Place("???", "You just woke up here. You have no idea where you are.", [Enemy("Unhappy Squirrel", 15, 3)])
fight(place1.enemies, player)