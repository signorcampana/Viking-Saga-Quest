# theme page
print('VIKING SAGA QUEST')
print('  ||')
print('  ||______________________')
print('0:::______________________\ ')
print('0:::______________________/ ')
print('  ||')
print('  ||')
#introducing the story
#setting up name, weapon and quest
print('clouds roll over Akkarfjord...the salt spray from the sea rises over the long grass as you stride into the village.')
print('You wind your way through the bleak mud huts to the ramshackle cabin which serves Akkarfjord as village pub…/n at the door you are met by a stout man with a bushy beard')
print('I am the inn keeper of Akkarfjord and I bid thee welcome, however none pass the entrance of my hall without identification...')
name = input ('what is your name?')
print('Hello, ' + name + ' I knew a ' + name + ' once… welcome to my hall!')
quest = input ('what brings you to the island?:') 
print(quest +' you say? A noble cause I am sure,but round here you will be in need of some protection…there are fiends and monsters that roam the local area, do you have anything with which you can fight?')
items = input ('which item do you wish to bring? dagger, spear or shield? ')
print('You have chosen...' + items)
print('THE END')


import random



ENEMY_NAMES = (

	"Minotaur",

	"Hydra",

	"Griffin",

)



class Enemy:

	name=None

	hp=100

	maxHp=100

	stat_defense=0

	stat_attack=0

	level = 1

	isPlayer=False

	weapon=None

	

	def __init__(self, level, weapon):

		self.name = random.choice(ENEMY_NAMES)

		self.weapon = weapon

		self.level = level

		self.fixStats()

		self.hp = self.maxHp

		

	def fixStats(self):

		"fixes the stats (attack/defense) after the level has been changed"

		level = self.level

		if self.isPlayer:

			level = level+1 # give the player an extra advantage to keep things fun

		self.stat_attack = 40+(level*5)

		self.stat_defense = 30+(level*5)

		self.maxHp = 100+(10*((level+1)))

	def hurt(self, ammount):

		"hurts the object, removes damage based on the object's defense rating"

		ammount = ammount - (self.stat_defense/2)

		self.hp = self.hp - ammount

		return self.hp

	def attack(self, target):

		"attacks a target, and removes damage based on the object's attack rating"

		damage = ((self.weapon.attack+self.stat_attack)/2)+random.choice(range(self.stat_attack/6, self.stat_attack/4))

		target.hurt(damage)

		return damage

	def heal(self, value):

		"heals the current object"

		oldHp = self.hp

		self.hp = self.hp + value

		if self.hp > self.maxHp: self.hp = self.maxHp

		return self.hp - oldHp

	def think(self, target):

		"AI for the enemy"

		if self.hp < 0: return # we can't think if we're dead!

		if self.hp/self.maxHp < 0.4 and random.choice((True, False, False)):

			ammount = self.heal(self.level*10)

			print ("Enemy used a healing potion, recovered %s HP!") % ammount

		else:

			damage = self.attack(target)

			print ("Enemy %s attacks, %s looses %s HP") % (self.name, target.name, damage)

			class BaseItem:
        isWeapon=False

                name = "Item"

                extraText = "Does something"

	

	def use(self, target):

		"use the object on target"

		pass

		

class Potion(BaseItem):

	name = "Potion"

	extraText = "replenish 20 HP"

	hp = 20

	

	def __init__(self):

		self.extraText = "replenish %s HP" % self.hp

	

	def use(self, target):

		target.heal(self.hp)

		

class SuperPotion(Potion):

	name = "Super Potion"

	hp = 50

#!/usr/bin/env python



import weapons

from enemy import *

from items import *

from player import Player

import random



# If you want to add in saving, check out the 'pickle' module.



# some configuration stuff

CHEATS = False # set to true for cheats. Good for debugging.



# menu constants

ATTACK = 1

RUN = 2

USE_ITEM = 3

EXIT = 4



class RPG:

	def main(self):

		"game setup, and main loop"

		self.player = Player()

		# for now, let's just make it a series of battles

		# you can add in more stuff if you want.

		for i in range(1, 5):

			self.battle()

			choice = "y"

			while 1:

				print "Use an item? (y/n)"

				choice = raw_input()

				if choice == "n":

					break

				self.item_menu()

	

	def battle(self):

		"initiate a battle sequence"

		#get an enemy, give it a random weapon, and give it a random level (but no more then one less then the player)

		level = range(1, self.player.level-1)

		if not level:

			level = 1

		else:

			level = random.choice(level)

		enemy = Enemy(level = level, weapon=random.choice([weapons.Dagger(),

								   weapons.ShortSword(),

								   weapons.LongSword()]))

		print "Enemy %s appears!" % enemy.name

		raw_input()

		while self.player.hp > 0 and enemy.hp > 0:

			while 1:

				res = self.battleScreen(enemy)

				if res is EXIT:

					self.exit()

					break

				elif res is RUN:

					if random.choice([True, False, False]):

						print "You got away!"

						raw_input()

						return

					else:

						print "couldn't escape!"

						raw_input()

						return

				elif res is ATTACK:

					dmg = self.player.attack(enemy)

					print "Enemy took %s damage" % dmg

					break

				elif res is USE_ITEM:

					# item_menu will return false when the user chooses back

					if self.item_menu():

						break

			

			#enemy's turn

			enemy.think(self.player)

			raw_input()

		if self.player.hp <= 0:

			print "You have died."

			self.exit()

		elif enemy.hp <= 0:

			print "Enemy %s has been defeated!" % enemy.name

			expGain = enemy.level * 100

			self.player.giveExp(expGain)

			return

			

	def battleScreen(self, enemy):

		"prints the battle screen, and calls self.menu to get input in the form of a menu"

		print ".------------------->"

		print "| Level %s %s" % (enemy.level, enemy.name)

		print "| HP: %s/%s" % (enemy.hp, enemy.maxHp)

		print "'------------------->"

		print ".------------------->"

		print "| Level %s %s" % (self.player.level, self.player.name)

		print "| HP: %s/%s" % (self.player.hp, self.player.maxHp)

		print "'------------------->"

		print ""

		return self.menu()

	def menu(self):

		"draws the menu, and returns the action the user requested"

		print ".-----------."

		print "| 1. Attack |"

		print "| 2. Item   |"

		print "| 3. Run    |"

		print "| 4. Exit   |"

		print "'-----------'"

		try:

			do = int(raw_input())

		except ValueError:

			print "invalid choice"

			raw_input()

			return

		if do == 1:

			return ATTACK

		elif do == 2:

			return USE_ITEM

		elif do == 3:

			return RUN

		elif do == 4:

			return EXIT

		else:

			print "invalid choice"

			raw_input()

			return

	def item_menu(self):

		"draws the items menu based on the user's inventory. When an item is used, it's 'use' method is called, and then it is removed from their inventory."

		inv = self.player.inventory

		print ".------------------->"

		for i in range(0, len(inv)):

			print "| %s. %s (%s)" % (i+1, inv[i].name, inv[i].extraText)

		print "| X. Back"

		print "'------------------->"

		do = raw_input()

		if do == "X" or do == "x":

			return False

		else:

			try:

				i = int(do)-1

				if i < 0:

					raise ValueError

				item = inv[i]

				item.use(self.player)

				left = inv[0:i]

				right = inv[i+1:len(inv)]

				if i-2 < 0:

					left = []

				if i >= len(inv)-1:

					right = []

				self.player.inventory = left+right

				return True

			except (LookupError,ValueError):

				print "invalid input"

				raw_input()

				return self.item_menu()

	def exit(self):

		"exits the game"

		print "Goodbye"

		exit()



# start the game

if __name__ == "__main__": # only run the game if we're the main script

	rpg = RPG()

	rpg.main()

from enemy import Enemy

from weapons import Dagger



class Player(Enemy):

	experience = 0

	inventory = []

	isPlayer = True

	def __init__(self):

		self.weapon = Dagger()

		print "What is your name?"

		self.name = raw_input()

		self.level = 2

		self.fixStats()

		self.hp = self.maxHp

		#give some starting items

		from items import Potion, SuperPotion

		from weapons import Excalibur

		self.giveItem(Excalibur)

		for i in range(1, 5):

			self.giveItem(Potion())

			self.giveItem(SuperPotion())

	def giveExp(self, ammount):

		"give the player a certain ammount of experience points, and print the new stats if they gained a level"

		print "You have gained %s experience points" % ammount

		self.experience = self.experience+ammount

		if self.experience > (self.level+1)^2:

			self.level = self.level + 1

			self.fixStats()

			print "You have gained a level!"

			print "Level - %s" % self.level

			print "Attack - %s" % self.stat_attack

			print "Defense - %s" % self.stat_defense

			print "Max HP - %s" % self.maxHp

			raw_input()

		else:

			print "%s experience points until next level" % ((self.level+1)^2)-self.experience

	def giveItem(self, item):

		"give the player an item, and add it to their inventory or weapon slot"

		if item.isWeapon:

			self.weapon = item

		else:

			self.inventory.append(item)
class BaseWeapon:

	attack=0

	isWeapon=True

	

class Dagger(BaseWeapon):

	attack=2

	

class ShortSword(BaseWeapon):

	attack=5

	

class LongSword(BaseWeapon):

	attack=10

	

class Excalibur(BaseWeapon):

	attack = 15

	

	def __init__(self):

		if CHEATS:

			self.attack = 9999 # IT'S OVER 9000!!!
