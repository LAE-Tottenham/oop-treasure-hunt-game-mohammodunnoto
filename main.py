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

            print("\nWhat would you like to do?")
            print("1. Attack")
            print("2. Use Item")
            action = input("Choose an action (1/2):\n").strip()

            if action == "1":
                damage = player.attack()
                enemy.take_damage(damage)

                if enemy.health <= 0:
                    break
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
        print("3. Drop an item")
        print("4. Back to exploring")
        
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

        elif choice == "4":
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
place3 = Place("The Crumbled Bridge", "You come across a broken bridge, barely hanging over a deep ravine. The mist swirls beneath.", [Enemy("Bridge Guardian", 25, 5, False, "You shall not pass!")])
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
place8 = Place("The Ruins", "Old, crumbled stone ruins emerge from the mist, half-sunken into the ground. Forgotten symbols mark the stone.", [Enemy("Ancient Guardian", 50, 10, False, "Leave my ruin now. Leave and don't turn back.")])
place8.add_item(Weapon("Shattered Amulet", 200, "A piece of a glowing amulet. It seems to hum when touched.", 5))
place8.add_item(Item("Dusty Relic", 350, "A small object, covered in dust, with intricate carvings."))
print("An ancient guardian, wary of your presence and intentions, attacks you to preserve the ruins it guards.")
fight(place8.enemies, player)
place8.explore(player)
place9 = Place("The Clearing", "A quiet, open area bathed in soft sunlight. A small stream flows nearby, offering some comfort. There seems to be no enemies here.", None)
place9.add_item(Weapon("Streamstone", 100, "A smooth, round stone that hums when placed in water.", 0))
place9.add_item(Medicine("Cleansing Herb", 40, "A rare herb used to detoxify poisons.", 30))
place9.add_item(Item("Small Beak", 50, "A rugged beak which seems to have been dismembered from a small bird."))
place9.explore(player)
place10 = Place("Abandoned Camp", "You stumble upon a deserted camp. Burnt-out fires and tattered tents suggest it’s been abandoned for a long time.", [Enemy("Rogue Scavenger", 60, 14, False, "Gimme your stuff! I need to earn a living!")])
place10.add_item(Weapon("Rusty Axe", 1000, "An old, worn-out axe. Heavy, but still sharp.", 18))
place10.add_item(Item("Tattered Map", 50, "A map that shows part of the forest. It's missing some pieces."))
place10.add_item(Medicine("Dried Berries", 10, "Edible berries that restore some health.", 10))
print("A rogue scavenger, in the area to search for any treasures or anything valuable stumbles upon you, a treasure trove of items, and decides they would like to loot you by force.")
fight(place10.enemies, player)
place10.explore(player)
place11 = Place("Overgrown Path", "A barely visible trail covered with dense vegetation. Every step is a struggle.", [Enemy("Venomous Vine", 65, 15)])
place11.add_item(Weapon("Machete", 800, "A sharp blade designed to cut through thick vegetation.", 15))
place11.add_item(Item("Jar of Sap", 300, "A sticky jar of sap that might be useful for crafting or traps."))
print("The forest doesn't seem to like you as much as you don't like it. A sentient vine attacks you for seemingly no reason.")
fight(place11.enemies, player)
place11.explore(player)
place12 = Place("Echoing Cave", "A dark, damp cave that amplifies every sound. Dripping water echoes eerily around you.", [Enemy("Echoing Wraith", 70, 16)])
place12.add_item(Item("Glowing Crystal", 500, "A mysterious crystal that emits a faint light."))
place12.add_item(Medicine("Energy Potion", 250, "A potion that restores your stamina and slightly heals you.", 20))
fight(place12.enemies, player)
place12.explore(player)
place13 = Place("Sunken Ruins", "Half-submerged ruins, with stagnant water pooling in the cracks. The air smells of decay.", [Enemy("Swamp Demon", 75, 17, False, "Get out of my swamp!")])
place13.add_item(Weapon("Trident Fragment", 400, "A broken trident piece, jagged but sharp.", 14))
place13.add_item(Medicine("Purifying Elixir", 300, "A rare liquid that heals and removes poison effects.", 30))
place13.add_item(Item("Shattered Scale", 950, "What seems to only just be a broken scale for weighing 2 items. Might have some use?"))
print("")
fight(place13.enemies, player)
place13.explore(player)
place14 = Place("Whispering Woods", "The trees seem to whisper as the wind blows, and you feel unseen eyes watching you.", [Enemy("Shadow Stalker", 80, 18)])
place14.add_item(Item("Whispering Amulet", 200, "An amulet that seems to hum faintly, as if alive."))
place14.add_item(Medicine("Mystic Herb", 50, "A glowing herb that heals and increases resistance to magic.", 25))
print("Something emerges from the shadows. You noticed the feeling of being watched ever since you left the last area, but to think it was coming from the shadows themselves.")
fight(place14.enemies, player)
place14.explore(player)
place15 = Place("Cliffside", "A narrow, precarious path along a cliff. The wind howls and the ground feels unstable.", [Enemy("Harpy", 85, 20)])
place15.add_item(Weapon("Throwing Knives", 300, "A set of lightweight knives for ranged combat.", 12))
place15.add_item(Item("Rope Ladder", 1000, "A rope ladder for climbing down steep cliffs."))
place15.add_item(Medicine("Big Yellow Eye", 500, "A stupidly massive yellow eye from God knows where. Is probably packed with nutrients.", 15))
print("From the sky a harpy swoops down on you, ready to feast.")
fight(place15.enemies, player)
place15.explore(player)
place16 = Place("Frozen Glade", "A clearing blanketed with snow. The cold bites at your skin, and the air feels heavy.", [Enemy("Frost Wolf", 90, 22), Enemy("Frost Wolf", 90, 22)])
place16.add_item(Medicine("Warmth Potion", 200, "A potion that restores health and protects against the cold.", 25))
place16.add_item(Item("Icicle Shard", 300, "A shard of ice that doesn’t melt, no matter the temperature."))
print("From the glade, a pair of Frost Wolves surround and encircle you, trying to earn their next meal.")
fight(place16.enemies, player)
place16.explore(player)
place17 = Place("Crystalline Cavern", "A shimmering cave filled with crystals that refract light into rainbows.", [Enemy("Crystal Golem", 95, 30, False, "Beep Beep.")])
place17.add_item(Weapon("Crystal Spear", 700, "A spear made of glowing crystal, sharp and deadly.", 20))
place17.add_item(Item("Shimmering Gem", 250, "A rare gem that glows faintly in the dark."))
print("A Crystal Golem forms in front of you in a similar manner to the Bridge Guardian you previously encountered. Why is it here in a cave though Is it protecting something?")
fight(place17.enemies, player)
place17.explore(player)

place18 = Place(
    "Shadowed Clearing",
    """You step into an eerily dark but open patch of the forest. No canopy overhead, yet the sunlight doesn’t seem to reach here.
    The air is cold, and a strange silence fills the space. Something about this place feels unnatural.""",
    None
)
place18.add_item(Item("Shadowed Pendant", 200, "A mysterious pendant that absorbs light around it."))
place18.add_item(Medicine("Elixir of Light", 300, "A glowing potion that restores health and grants temporary resistance to shadow attacks.", 40))
while True:
    place18.explore(player)
    if not place18.available_items:
        print("\nAfter thoroughly exploring the clearing, you notice a stone pedestal in the center. "
              "It has shallow carvings that seem to depict three objects: a large eye, a shattered scale, and a small beak.")
        
        required_items = {"Big Yellow Eye", "Shattered Scale", "Small Beak"}
        player_items = {item.name for item in player.inventory}

        if required_items.issubset(player_items):
            print("\nThe pedestal glows faintly as you place the three items upon it. The ground begins to rumble.")
            time.sleep(2)
            print("""The Big Yellow Eye begins to glow a deep yellow, letting off immense light. 
            A Big Bird, with an uncountable number of big yellow eyes appears.""")
            time.sleep(3)
            print("""The Shattered Scale begins to glow a pale blue, mending itself and making you wary of your sins. 
            A Judgement Bird, with a bandaged had and a scale around its neck appears.""")
            time.sleep(3)
            print("""The Small Beak begins to glow a dark purple, growing in size and sprouting several sharp teeth.
            A Punishing Bird, with a very small stature but a seemingly endless hole in its belly appears.""")
            time.sleep(3)
            print("Deafening cres echoes through the forest from all things as the air grows heavy and the three birds grow closer.")
            time.sleep(2)
            print("""Then, in the middle of all the chaotic cries, unable to control your fear you shout:
            'It's the monster! The big, terrible monster that lives in the dark, black forest!'""")
            time.sleep(3)
            print("Monster? The three birds, now as one, looked around but there was no one to be seen.")
            time.sleep(2)
            print("""The bird began to prowl the forest, looking for the monster. 
            The forest would be in trouble if the monster really showed up.""")
            time.sleep(2)
            print("But there was nothing. There were no creatures, no sun and moon, and no beast.")
            time.sleep(2)
            print("All that was left was just a bird and the black forest. Only cold, dark night continued from then.")
            time.sleep(2)
            print("Until the Bird found you. Since you were the only other one there, it judged that you must be the monster.")
            time.sleep(2)
            print("To protect the forest, it decided that the only thing it could do was to eliminate the 'monster'.")
            time.sleep(3)
            print("It is **The Monster in the Black Forest, The Apocalypse Bird.**")

            apocalypse_bird = Enemy("The Monster in the Black Forest, The Apocalypse Bird", 300, 40, is_boss=True)
            fight(apocalypse_bird, player)
            
            if apocalypse_bird.health <= 0:
                print("\nWith a final strike, the Apocalypse Bird collapses. Its massive form dissolves into glowing feathers, leaving behind a weapon.")
                twilight_weapon = Weapon("Twilight", 0, "A fragment of the Apocalypse Bird. Feels incredibly light in your hands, despite being so massive.", 40)
                player.add_to_inventory(twilight_weapon)
                print("You have obtained **Twilight**, a weapon of immense power.")
            break
        else:
            print("\nThe carvings seem to call for three specific items. You feel like you're missing something.")
            print("For now, there's nothing more to do here.")
            break

place19 = Place(
    "Twilight Grove",
    """The forest begins to thin, revealing a glade bathed in an eerie twilight. The sky above is a strange, swirling mix of purple and gold,
    yet there’s no visible source of light. The air here feels heavy, like the forest is holding its breath, waiting for something.""",
    [Enemy("Twilight Stag", 70, 25)]
)
place19.add_item(Item("Twilight Shard", 300, "A fragment of light and shadow, pulsating with a strange energy."))
place19.add_item(Weapon("Silverfang Dagger", 800, "A sharp dagger that glints with an otherworldly light.", 30))
if "Twilight" in [item.name for item in player.inventory]:
    essence_heal = player.max_health
else:
    essence_heal = 25
place19.add_item(Medicine("Essence of Darkness", 250, "A strange black, tar-like liquid is present inside a vial. What is it?", essence_heal))
fight(place19.enemies, player)
place19.explore(player)
place20 = Place(
    "The Abyssal Gate",
    """You find yourself standing before a towering gate of black stone, adorned with intricate carvings that seem to shift and writhe as you stare at them.
    The air is cold and biting, and the sound of your own breath echoes unnaturally in the silence. This is it. The end of your journey.""",
    [
        Enemy("Abyssal Minion", 60, 20),
        Enemy("Abyssal Minion", 60, 20),
        Enemy("The Abyssal Gatekeeper", 200, 40, is_boss=True, key_item="Fragment of the End")
    ]
)
place20.add_item(Item("Gate Key Fragment", 500, "A jagged piece of a mysterious key, pulsing with ominous energy."))

while True:
    place20.explore(player)
    if not place20.available_items:
        print("\nAs you approach the gate, the carvings on its surface glow faintly. The air grows impossibly cold.")
        for i in range(len(place20.enemies) - 1):
            enemy = place20.enemies[i]
            print(f"\nA chilling presence manifests before you: {enemy.name} emerges from the shadows!")
            fight(enemy, player)

        gatekeeper = place20.enemies[2]
        print(f"\nWith the minions defeated, a booming voice echoes through the air.")
        print(f"'I am the Gatekeeper. With the blood of the forest on your hands and the sins of your killings on your soul, you are not worthy to pass through and reach salvation.'")
        print(f"\nThe ground shakes as {gatekeeper.name} steps forward, wielding immense power!")

        if fight(gatekeeper, player):
            print("\nWith a final blow, the Abyssal Gatekeeper collapses, his body shattered, leaving behind a shimmering object.")
            time.sleep(2)
            print("You have obtained the 'Fragment of the End', a piece that looks necessary to unlock the gate.")
            if "Twilight" in [item.name for item in player.inventory]:
                print("\nThe weapon Twilight hums faintly in your hands, resonating with the gate's energy.")
                time.sleep(2)
                print("You see a fragment of your weapon's memories, and the memories of the Birds it was fragmented from.")
                time.sleep(2)
                print("You now realise, after defeating the Apocalypse Bird, the guardians of the forest, you have left the forest vulnerable.")
                time.sleep(2)
                print("You now have a choice. You can either leave through the gateway, hopefully to home, or ensure the forest's safety.")
                time.sleep(2)
                choice_final = input("What will you do - Protect or Leave?")
                if choice_final == "Protect":
                    print("""You contemplate whether protecting is the right decision as you hear a feeble rumbling behind you.""")
                    time.sleep(2)
                    print("You turn around, only to meet the previously defeated Abyssal Gatekeeper face to face.")
                    time.sleep(2)
                    print("You stand on guard, weary of the suddenly resurrected Gatekeeper, unsure if you can win another fight.")
                    time.sleep(2)
                    print("However, the Gatekeeper instead converses with you.")
                    time.sleep(2)
                    print("'I have seen your intentions. I wasn't fully mistaken, as you aren't a good person, but not an evil one either, thinking about the wellbeing of the forest.'")
                    time.sleep(2)
                    print("'Worry not, as you do not have to remain here. If you leave 'Twilight' to me, I can resurrect the Apocalypse Bird to guard the forest.'")
                    time.sleep(2)
                    print("You hand the Gatekeeper 'Twilight', unsure about whether to trust him or not, but it doesn't really matter to you if he is or isn't as long as you can leave.")
                    time.sleep(2)
                    print("You turn away from the Gatekeeper, and place the 'Fragment of the End' in the space in the pedestal next to the Gate.")
                    time.sleep(2)
                    print("The black rocky Gate activates, the portal swirling spontaneously with a deep purple hue.")
                    time.sleep(2)
                    print("You step through the portal, hoping you'll finally get to go home and sleep a little.")
                    time.sleep(2)
                    exit("""
▀█████████▄     ▄████████    ▄████████     ███             ▄████████ ███▄▄▄▄   ████████▄   ▄█  ███▄▄▄▄      ▄██████▄  
  ███    ███   ███    ███   ███    ███ ▀█████████▄        ███    ███ ███▀▀▀██▄ ███   ▀███ ███  ███▀▀▀██▄   ███    ███ 
  ███    ███   ███    █▀    ███    █▀     ▀███▀▀██        ███    █▀  ███   ███ ███    ███ ███▌ ███   ███   ███    █▀  
 ▄███▄▄▄██▀   ▄███▄▄▄       ███            ███   ▀       ▄███▄▄▄     ███   ███ ███    ███ ███▌ ███   ███  ▄███        
▀▀███▀▀▀██▄  ▀▀███▀▀▀     ▀███████████     ███          ▀▀███▀▀▀     ███   ███ ███    ███ ███▌ ███   ███ ▀▀███ ████▄  
  ███    ██▄   ███    █▄           ███     ███            ███    █▄  ███   ███ ███    ███ ███  ███   ███   ███    ███ 
  ███    ███   ███    ███    ▄█    ███     ███            ███    ███ ███   ███ ███   ▄███ ███  ███   ███   ███    ███ 
▄█████████▀    ██████████  ▄████████▀     ▄████▀          ██████████  ▀█   █▀  ████████▀  █▀    ▀█   █▀    ████████▀  
                                                                                                                     
""")
            else:
                print("You turn away from the Gatekeeper, and place the 'Fragment of the End' in the space in the pedestal next to the Gate.")
                time.sleep(2)
                print("The black rocky Gate activates, the portal swirling spontaneously with a deep purple hue.")
                time.sleep(2)
                print("You step through the portal, hoping you'll finally get to go home and sleep a little.")
                exit("""
   _____                 _   ______           _ _             
  / ____|               | | |  ____|         | (_)            
 | |  __  ___   ___   __| | | |__   _ __   __| |_ _ __   __ _ 
 | | |_ |/ _ \ / _ \ / _` | |  __| | '_ \ / _` | | '_ \ / _` |
 | |__| | (_) | (_) | (_| | | |____| | | | (_| | | | | | (_| |
  \_____|\___/ \___/ \__,_| |______|_| |_|\__,_|_|_| |_|\__, |
                                                         __/ |
                                                        |___/""")
        else:
            print("\nYou failed to defeat the Abyssal Gatekeeper. The gate remains locked, and your story ends here.")
            exit("""
 ▄▄▄▄   ▄▄▄     ▓█████▄    ▓█████ ███▄    █▓█████▄ ██▓███▄    █  ▄████ 
▓█████▄▒████▄   ▒██▀ ██▌   ▓█   ▀ ██ ▀█   █▒██▀ ██▓██▒██ ▀█   █ ██▒ ▀█▒
▒██▒ ▄█▒██  ▀█▄ ░██   █▌   ▒███  ▓██  ▀█ ██░██   █▒██▓██  ▀█ ██▒██░▄▄▄░
▒██░█▀ ░██▄▄▄▄██░▓█▄   ▌   ▒▓█  ▄▓██▒  ▐▌██░▓█▄   ░██▓██▒  ▐▌██░▓█  ██▓
░▓█  ▀█▓▓█   ▓██░▒████▓    ░▒████▒██░   ▓██░▒████▓░██▒██░   ▓██░▒▓███▀▒
░▒▓███▀▒▒▒   ▓▒█░▒▒▓  ▒    ░░ ▒░ ░ ▒░   ▒ ▒ ▒▒▓  ▒░▓ ░ ▒░   ▒ ▒ ░▒   ▒ 
▒░▒   ░  ▒   ▒▒ ░░ ▒  ▒     ░ ░  ░ ░░   ░ ▒░░ ▒  ▒ ▒ ░ ░░   ░ ▒░ ░   ░ 
 ░    ░  ░   ▒   ░ ░  ░       ░     ░   ░ ░ ░ ░  ░ ▒ ░  ░   ░ ░░ ░   ░ 
 ░           ░  ░  ░          ░  ░        ░   ░    ░          ░      ░ 
      ░          ░                          ░                          """)
        break