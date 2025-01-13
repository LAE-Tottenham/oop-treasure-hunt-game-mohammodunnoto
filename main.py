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
            else:
                print("You can't do that. Just pick one of the options.")

def fight(enemies, player):
    for enemy in enemies:
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
place1.add_item(Item("Mossy Stone", 100, "A smooth stone covered in moss. Might be useful for something."))
fight(place1.enemies, player)
place1.explore(player)
place2 = Place("Thicket", "An area of thicker trees. The trees are dense and intertwined, making movement difficult.", None)
place2.add_item(Medicine("Small Healing Herb", 20, "A bundle of herbs that may help with wounds.", 15))
place2.add_item(Item("Broken Compass", 200, "A compass with a cracked face, but it still points North."))
place2.explore(player)
place3 = Place("The Crumbled Bridge", "You come across a broken bridge, barely hanging over a deep ravine. The mist swirls beneath.", [Enemy("Bridge Guardian", 25, 5)])
print("Rocks and stones levitate together to the same spot, forming into a rock guardian.")
fight(place3.enemies, player)
place3.explore(player)
place4 = Place("The Hollow", "A small hollow in the forest where the trees form a perfect circle around you.", [Enemy("Feral Shade", 30, 6)])
place4.add_item(Medicine("Herbal Medicine", 100, "A soothing medicine made from forest herbs, good for healing.", 25))
print("A feral shade jumps out at you from the dark.")
fight(place4.enemies, player)
place4.explore(player)
place5 = Place("The Ancient Oak", "A massive oak tree stands in the middle of a clearing. Its branches are twisted, and a strange energy seems to pulse from it.", [Enemy("Forest Titan", 60, 10)])
place5.add_item(Weapon("Ritual Dagger", 500, "An ornate dagger with strange symbols carved into its blade.", 15))
place5.add_item(Item("Pine Sap", 50, "A small jar of sticky pine sap that could be useful for crafting."))
print("The forest titan, unhappy at your unnatural presence, decides to do something about you.")
fight(place5.enemies, player)
place5.explore(player)
place6 = Place("The Marshlands", "A wet, mucky area filled with deep puddles and decaying vegetation.", [Enemy("Mud Serpent", 40, 8)])
place6.add_item(Medicine("Swamp Fungus", 30, "A dark purple fungus that may have medicinal properties.", 20))
place6.add_item(Item("Clay Jar", 250, "A small jar filled with muddy water. It's hard to tell its purpose."))
print("A mud serpent comes out and tries to attack you, wanting to make you its next prey.")
fight(place6.enemies, player)
place6.explore(player)
place7 = Place("The Hollowed-out Tree", "You find a massive hollowed tree, offering shelter from the ever-thickening mist. But something feels off.", [Enemy("Tree Ent", 45, 9)])
place7.add_item(Weapon("Vine Whip", 600, "A long vine wrapped tightly, it can be used as a weapon or for climbing.", 10))
place7.add_item(Medicine("Herbal Medicine", 100, "A soothing medicine made from forest herbs, good for healing.", 25))
print("A tree ent comes swinging out of the trees to attack you.")
fight(place7.enemies, player)
place7.explore(player)
place8 = Place("The Ruins", "Old, crumbled stone ruins emerge from the mist, half-sunken into the ground. Forgotten symbols mark the stone.", [Enemy("Ancient Guardian", 50, 10)])
place8.add_item(Weapon("Shattered Amulet", 200, "A piece of a glowing amulet. It seems to hum when touched.", 5))
place8.add_item(Item("Dusty Relic", 350, "A small object, covered in dust, with intricate carvings."))
print("An ancient guardian, wary of your presence and intentions, attacks you to preserve the ruins it guards.")
fight(place8.enemies, player)
place8.explore(player)
place9 = Place("The Clearing", "A quiet, open area bathed in soft sunlight. A small stream flows nearby, offering some comfort.", None)
place9.add_item(Weapon("Streamstone", 100, "A smooth, round stone that hums when placed in water.", 0))
place9.add_item(Medicine("Cleansing Herb", 40, "A rare herb used to detoxify poisons.", 30))
fight(place9.enemies, player)
place9.explore(player)