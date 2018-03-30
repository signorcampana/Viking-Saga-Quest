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
print('clouds roll over Akkarfjord...')
print('the salt spray from the sea rises over the long grass as you stride into the village.')
print('You wind your way through the bleak mud huts to the ramshackle cabin as village pub')
print('at the door you are met by a stout man with a bushy beard')
print('I am the inn keeper of Akkarfjord and I bid thee welcome,')
print('however none pass the entrance of my hall without identification...')

#!/usr/bin/env python

import weapons, enemys, items, players, random

# If you want to add in saving, check out the 'pickle' module.
# some configuration stuff
CHEATS = False 					# set to true for cheats. Good for debugging.

# menu constants
ATTACK = 1

RUN = 2

USE_ITEM = 3

EXIT = 4

class RPG:
	def main(self):
		"game setup, and main loop"
		self.player = players.Player()
		# for now, let's just make it a series of battles
		# you can add in more stuff if you want.
		for i in range(1, 5):
			self.battle()
			choice = "y"
			while 1:
				print("Use an item? (y/n)")
				choice = input()
				if choice == "n":
					break
				self.item_menu()

	def battle(self):
		"initiate a battle sequence"
		"""get an enemy, give it a random weapon, and give it a random level
		(but no more then one less then the player)"""
		level = range(1, self.player.level - 1)
		if not level:
			level = 1
		else:
			level = random.choice(level)
		new_enemy = enemys.Enemy(level = level, weapon=random.choice([weapons.Dagger(),
							weapons.ShortSword(),
							weapons.LongSword()]))
		print("Enemy %s appears!" % new_enemy.name)


		while self.player.hp > 0 and new_enemy.hp > 0:
			while 1:
				res = self.battleScreen(new_enemy)
				if res is EXIT:
					self.exit()
					break
				elif res is RUN:
					if random.choice([True, False]):
						print("You got away!")
						input()
						return
					else:
						print("couldn't escape!")
						input()
						return
				elif res is ATTACK:
					dmg = self.player.attack(new_enemy)
					print("Enemy took %s damage" % dmg)
					break
				elif res is USE_ITEM:
					#item_menu will return false when the user chooses back
					if self.item_menu():
						break
			#enemy's turn
			new_enemy.think(self.player)
			input()
		if self.player.hp <= 0:
			print("You have died.")
			self.exit()
		elif new_enemy.hp <= 0:
			print("Enemy %s has been defeated!" % new_enemy.name)
			expGain = new_enemy.level * 100
			self.player.giveExp(expGain)
			return

	def battleScreen(self, new_enemy):
		"prints the battle screen, and calls self.menu to get input in the form of a menu"
		print(".------------------->")
		print("| Level %s %s" % (new_enemy.level, new_enemy.name))
		print("| HP: %s/%s" % (new_enemy.hp, new_enemy.maxHp))
		print("'------------------->")
		print(".------------------->")
		print("| Level %s %s" % (self.player.level, self.player.name))
		print("| HP: %s/%s" % (self.player.hp, self.player.maxHp))
		print("'------------------->")
		print("")
		return self.menu()

	def menu(self):
		"draws the menu, and returns the action the user requested"
		print(".-----------.")
		print("| 1. Attack |")
		print("| 2. Item   |")
		print("| 3. Run    |")
		print("| 4. Exit   |")
		print("'-----------'")

		try:
			do = int(input())
		except ValueError:
			print("invalid choice")
			do = int(input())
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
			print("invalid choice")
			do = int(input())
			return

	def item_menu(self):
		"""draws the items menu based on the user's inventory.
		When an item is used, it's 'use' method is called,
		and then it is removed from their inventory."""

		inv = self.player.inventory
		print(".------------------->")
		for i in range(0, len(inv)):
			print("| %s. %s (%s)" % (i+1, inv[i].name, inv[i].extraText))
		print("| X. Back")
		print("'------------------->")
		do = input()
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
				print("invalid input")
				input()
				return self.item_menu()

	def exit(self):
		"exits the game"
		print("Goodbye")
		exit()

if __name__ == "__main__": 			# only run the game if we're the main script

	rpg = RPG()
	rpg.main()