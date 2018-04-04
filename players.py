from enemys import Enemy
from weapons import Dagger


class Player(Enemy):
    experience = 0
    inventory = []
    isPlayer = True

    def __init__(self):
        self.weapon = Dagger()
        self.name = input("What is your name? ")
        self.level = 4
        self.fixStats()
        self.hp = self.maxHp

    def giveExp(self, amount):

        print((("You have gained %s experience points") % amount))
        self.experience += amount

        if (self.experience > (self.level + 1) ^ 2):
            self.level += 1
            self.fixStats()
            print("You have gained a level!")
            print((("Level - %s") % self.level))
            print((("Attack - %s") % self.stat_attack))
            print((("Defense - %s") % self.stat_defense))
            print((("Max HP - %s") % self.maxHp))
        else:
            print(("%s experience points until next level") % ((self.level + 1) ^ 2) - self.experience)

    def giveItem(self, item):
        """give the player an item, add to weapons or inventory slot"""
        if item.isWeapon:
            self.weapon = item
        else:
            self.inventory.append(item)
