import random
import time
import os

class Enemy:
    def __init__(self, name, health, damage, is_boss=False, voice_lines=None, key_item=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.is_boss = is_boss
        self.voice_lines = voice_lines
        self.key_item = key_item

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        time.sleep(1)
        print(f"{self.name} has been beaten to death!")
        self.health = 0

    def speak(self):
        print(f"{self.voice_lines}")