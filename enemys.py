import random

ENEMY_NAMES = (
		"Minotaur",
		"Hydra",
		"Griffin",
		)


class Enemy:
	name = None
	hp = 100
	maxHp = 100
	stat_defense = 0
	stat_attack = 0
	level = 1
	isPlayer = False
	weapon = None

	def __init__(self, level, weapon):
		self.name = random.choice(ENEMY_NAMES)
		self.weapon = weapon
		self.level = level
		self.fixStats()
		self.hp = self.maxHp

	def fixStats(self):
		"""fixes the stats (attack/defense) after the level
		has been changed"""
		level = self.level
		if self.isPlayer:
			level += 1
		self.stat_attack = 40 + (level * 5)
		self.stat_defense = 30 + (level * 5)
		self.maxHp = 100 + (10 * (level + 1))

	def hurt(self, amount):
		"""hurts the object, removes damaged based on the object's
		defense rating"""
		amount -= (self.stat_defense / 2)
		self.hp -= amount
		return self.hp

	def attack(self, target):
		"""attacks a target, and removes damaged based on the object
		attack rating"""
		damage = ((self.weapon.attack + self.stat_attack) / 2)
		target.hurt(damage)
		return damage

	def heal(self, value):
		"""heals the current object"""
		oldHP = self.hp
		self.hp += value
		if self.hp > self.maxHp:
			self.hp = self.maxHp
		return self.hp - oldHP

	def think(self, target):
		"""AI for the enemy"""
		if self.hp < 0:
			return																		# we can't think if we're dead
		if ((self.hp/self.maxHp < 0.4) and (random.choice([True, False]))):
			amount = self.heal(self.level * 10)
			print("Enemy used a healing potion, recovered ", amount, " HP!")
		else:
			damage = self.attack(target)
			#print(damage, target.name, self.name)
			print("Enemy ", self.name, " attacks,", target.name, " loses ", damage, " HP")
