import random
import math
import Algorithm

class Map:
	'''A class that holds the tiles in a set order for later retrieval.
	
	Arguments: user, is a boolean that denotes whether the user will create the map or if it will be randomly generated.
	
	Self Variables: map, start, end, length, width, user.
	
	Methods: make_map(), user_make_map().'''

	def __init__(self, user, width, length):
		self.map = []
		self.user = user
		self.width = width
		self.length = length

		if self.user is True: #user input
			
			while True:
				print("Input map start as two integers(x,y coordinates) seperated by a space:", end=" ")
				inp = [int(i) for i in input().split()]

				if inp[0] > self.length or inp[0] < 0 or inp[1] > self.width or inp[1] < 0:
					print("Your input was incorrectly formated try again.")
				elif self.start == self.end:
					print("Your start and end are the same point, input a different point.")
				else:
					break

			label = Gen.getLabel(self.start, self.end, self.length, self.width)
			requirementLoot = Gen.getRequirementLoot(self.length, self.width)
			weaponLoot = Gen.getWeaponLoot
			self.userMakeMap(label, requirementLoot, weaponLoot)

		else: #gen input
			self.start = Gen.getPoint(self.length, self.width) #get rand start
			self.end = Gen.getPoint(self.length, self.width) #get rand end

			while self.end == self.start:
				self.end = Gen.getPoint(self.length, self.width) #get rand end

			label = Gen.getLabel(self.start, self.end, self.length, self.width)
			mob = Gen.getMob(self.length, self.width)
			speed = Gen.getSpeed(self.length, self.width)
			requirement = Gen.getRequirement(self.length, self.width)
			requirementLoot = Gen.getRequirementLoot(self.length, self.width)
			weaponLoot = Gen.getWeaponLoot(mob)
			
			self.makeMap(label, mob, speed, requirement, requirementLoot, weaponLoot)

		print("Map made.")


	def userMakeMap(self, label, requirementLoot, weaponLoot):
		for x in range(self.width * self.length):
			print("The following inputs will be for tile ", x)
			self.map.append(Tile(self.user, x, label[x], requirementLoot[x], weaponLoot[x]))

	def makeMap(self, label, mob, speed, requirement, requirementLoot, weaponLoot):
		for x in range(self.width * self.length):
			self.map.append(Tile(self.user, x, label[x], mob[x], speed[x], requirement[x], requirementLoot[x], weaponLoot[x]))

	def drawMap(gameMap,character, length, width):
		for index in range(width*length):
			tile = gameMap.map[index]
			if tile == character.tileOn:
				print('@',end='')
			elif tile.label == "end":
				if tile.requirement == "gate" or tile.requirement == "hill":
					print('b',end='')
				else:
					print('B',end='')
			elif tile.requirement == "gate":
				#need another print statement checking if you have gate key (or there is key/gear on tile)
				
				if character.gear[1] != None:
					if tile.requirementLoot == "Climbing Gear" and character.gear[0] == None:
						print('C',end='')
					else: 
						print('-',end='')
				else:
					if tile.requirementLoot == "Gate Key" and tile.requirementLoot == "Climbing Gear":
						print('g',end='')
					else:
						print('G',end='')
			elif tile.requirement == "hill":
				#need another print statement checking if you have climbing gear (or there is key/gear on tile)
				if character.gear[0] != None: 
					if tile.requirementLoot == "Gate Key" and character.gear[1] == None:
						print('K',end='')
					else:
						print('-',end='')
				else:
						if tile.requirementLoot == "Gate Key" and tile.requirementLoot == "Climbing Gear":
							print('h',end='')
						else:
							print('H',end='')
			elif tile.requirementLoot == "Gate Key" and character.gear[1] == None:
				print('K',end='')
			elif tile.requirementLoot == "Climbing Gear" and character.gear[0] == None:
				print('C',end='')
			else:
				print('-',end='')
			print(" ",end='')
			if (index+1)%width==0:
				print("")
		print("\n? = character, B = boss (lowercase if hill/gate exists on tile), K = gate key, C = climbing gear\nH = hill (lowercase if key/gear exists on tile), G = gate (lowercase if key/gear exists on tile)")

	def __repr__ (self):
		rep = ""
		for x in range(self.width * self.length):
			rep += str(self.map[x])
			if (x+1)%self.width == 0:
				rep += "\n"
		return rep
			
class Tile:
	'''A class that contains variables which makeup each tile.

	Arguments: user, is a boolean that denotes whether the user will create the tile or if it will be randomly generated.
	label, which will be one of three possible strings that outline the border of the map, start and end points.
	mob, an integer which denotes monsters are present on the tile specifically the int being the monsters health points.
	speed, an integer which denotes the speed or experience points given by a tile.
	requirement, a string that requires gear to be able to move to that tile.
	
	Self Variables: user, idx, label, mob, speed, requirement.

	Methods: make_tile(), user_make_tile().'''
	def __init__(self, user, idx, label, mob = None, speed = None, requirement = None, requirementLoot = None, weaponLoot = None):
		if user is True:
			self.userMakeTile(idx, label)
		else:
			self.makeTile(idx, label, mob, speed, requirement, requirementLoot, weaponLoot)

	def userMakeTile(self, idx, label):
		self.label = label
		self.idx = idx

		while True:
			print("Input mob hit points for this tile (input 0 if no mob), as a positive integer:", end=" ")
			self.mob = int(input())

			if self.mob < 0:
				print("Your input was negative, try again.")
			else:
				break

		while True:
			print("Input speed it takes to cross this tile as a positive integer greater than 1:", end=" ")
			self.speed = int(input())

			if self.speed < 1:
				print("Your input was less than 1, try again.")
			else:
				break

		print("Input requirement to travel accross this tile (input plains if no requirement), as a string:", end=" ")
		self.requirement = input()



	def makeTile(self, idx, label, mob, speed, requirement, requirementLoot, weaponLoot):
		self.label = label
		self.idx = idx
		self.mob = mob
		self.speed = speed
		self.requirement = requirement
		self.requirementLoot = requirementLoot
		self.weaponLoot = weaponLoot

	def __repr__ (self):
		return "|" + str(self.label) + ", idx: " + str(self.idx) + ", req: " + str(self.requirement) +"|"

class Character:
	'''A class that contains variables which makeup each tile.

	Arguments: start, to initialize the staring tile.
	
	Self Variables: weaponName, weaponAtk, level, charAtk, exp, lvlUpExp, gear, tileOn.

	Methods: updateChar().'''

	def __init__(self, gameMap):
		self.weaponName = None
		self.weaponAtk = 0
		self.level = 1
		self.charAtk = 2*self.level
		self.exp = 0
		self.lvlUpExp = 50*self.level
		self.gear = [None]*2
		self.tileOn = gameMap.map[gameMap.start]
		if self.tileOn.requirement == "hill":
			print("You start with Climbing Gear.")
			self.gear[0] = "Climbing Gear"
		elif self.tileOn.requirement == "gate":
			print("You start with a Gate Key.")
			self.gear[1] = "Gate Key"

	def updateChar(self, gainedExp, weapon = None, gear = None):
		self.exp += gainedExp
		while self.exp >= self.lvlUpExp:
			self.exp -= self.lvlUpExp
			self.level += 1
			self.charAtk = 2*self.level
			self.lvlUpExp = 50*self.level

		if weapon != (None, None):
			if self.weaponAtk <= weapon[1]:
				self.weaponName = weapon[0]
				self.weaponAtk = weapon[1]
				print("You got a ", weapon[0], " and it does ", weapon[1], " dmg.")

		if gear != None:
			if gear == "Climbing Gear" and self.gear[0] == None:
				self.gear[0] = gear
			elif gear == "Gate Key" and self.gear[1] == None:
				self.gear[1] = gear

class Gen:
	''' A class that uses random to generate all kinds of variables

	Self Variables: None

	Methods: getPoint(), getLabel(), getMob(), getSpeed(), getRequirement(), getLoot(), getRequirementLoot(), getReqAsLoot()'''

	def getPoint(length, width):
		return random.randrange(0, (length * width))

	def getLabel(start, end, length, width):
		label = []
		for x in range(length*width):
			if x == start:
				label.append("start")
			elif x == end:
				label.append("end")
			elif x in range(length)\
				or x in range(((width*length)-length), (width*length))\
			    or x in [0+(length*i) for i in range(width)]\
			    or x in [length+(length*i) for i in range(width-1)]:
				label.append("wall")
			else:
				label.append("middle")

		return label

	def getMob(length, width):
		mob = []
		for x in range(length*width):
			if random.randrange(5) <= 3:
				mob.append(random.randrange(10, 200))
			else:
				mob.append(0)

		return mob

	def getSpeed(length, width):
		speed = []
		for x in range(length*width):
			rnum = random.randrange(5)
			if rnum >= 3:
				speed.append(random.randrange(20, 40))
			elif rnum == 2:
				speed.append(random.randrange(10, 20))
			else:
				speed.append(random.randrange(40, 50))

		return speed

	def getRequirement(length, width):
		requirement = []
		for x in range(length*width):
			rnum = random.randrange(40)
			if rnum == 39 :
				requirement.append("gate")
			elif rnum in range(25, 30):
				requirement.append("hill")
			else:
				requirement.append("plains")

		return requirement

	def getWeaponLoot(mob):
		weaponLoot = []
		for mobHp in mob:
			if random.randrange(2) == 1 and mobHp != 0 and mobHp <= 999:
				weaponDmg = mobHp//4
				loot = ("Sword of jibberishishish", weaponDmg)
				weaponLoot.append(loot)
			else:
				weaponLoot.append((None, None))

		return weaponLoot

	def getWeapAsLoot(character):
		if character.tileOn.weaponLoot != None:
			loot = character.tileOn.weaponLoot
			print("You got a ", loot, ".")
			return loot
		else:
			return None

	def getRequirementLoot(length,width):
		requirementLoot = []
		for x in range(length*width):
			rnum = random.randrange(40)
			if rnum in range(37,39) :
				requirementLoot.append("Gate Key")
			elif rnum in range(25, 30):
				requirementLoot.append("Climbing Gear")
			else:
				requirementLoot.append(None)

		return requirementLoot

	def getReqAsLoot(character):
		if character.tileOn.requirementLoot != None:
			loot = character.tileOn.requirementLoot
			print("You got a ", loot, ".")
			return loot
		else:
			return None

class Movement:
	''' A class that uses random to generate all kinds of variables

	Arguments:

	Self Variables: None

	Methods: getPoint(), getLabel(), getMob(), getSpeed(), getRequirement(), getLoot(), getRequirementAsLoot()'''

	def canMove(character, tileTo):
		if character.tileOn.label == "wall" or character.tileOn.label == "start":
			if tileTo is not None:
				if Movement.checkReq(character, tileTo):
					return True
				else:
					return False
			else:
				print("The world dissapears there, you do not move there.") 
				return False
		else:
			if Movement.checkReq(character, tileTo):
				return True
			else:
				return False

	def checkReq(character, tileTo):
		if tileTo.requirement == "gate":
			if character.gear[1] != None:
				print("You unlock and go through the gate with your gate key.")
				return True
			else:
				print("You're blocked by a gate that you don't have a key for.")
				return False

		elif tileTo.requirement == "hill":
			if character.gear[0] != None:
				print("You climb the hill with your climbing gear.")
				return True
			else:
				print("You fail to climb the hill with your climbing gear.")
				return False
		else:
			print("You wander into the terrain.")
			return True

	def fightMob(character):
		if character.tileOn.mob != 0:
			mobToFight = character.tileOn.mob
			fightExp = math.ceil(mobToFight/(character.charAtk+character.weaponAtk))			
			print("You defeat a monster that tries to fight you. You gain "+str(fightExp)+" xp the monster.")
			return fightExp
		print("You pass through without encounters.")
		return 0

	def goToTile(character, tileTo):
		if Movement.canMove(character, tileTo):
			character.tileOn = tileTo
		else:
			print("You stay in the land you already are.")

		gainedExp = Movement.fightMob(character) + character.tileOn.speed
		print("You gained ", gainedExp, " total in this land.")
		character.updateChar(gainedExp, Gen.getWeapAsLoot(character), Gen.getReqAsLoot(character))	
		print("Your character is now level ", character.level, " and has ", character.exp, " experience points.")

	def lookAround(gameMap, character):
		print("")
		print("You look around and see:")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "up"), "up")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "right"), "right")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "left"), "left")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "down"), "down")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "stay"), "stay")

	def examineTile(tile, direction):
		if tile is not None:
			if tile.requirement == "gate":
				print("There is a gate", end=" ")
			elif tile.requirement == "hill":
				print("There is a hill", end=" ")
			else:
				print("There are grassy plains", end=" ")

			if tile.mob != 0:
				print("and has monsters " + str(direction) + "wards.")
			else:
				print("and has no monsters " + str(direction) + "wards.")
		else:
			print("There is no land ", direction)

	def getTileInDir(gameMap, character, direction):
		
		if direction == "up":
			if character.tileOn.idx < gameMap.width: #negative index
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx - gameMap.width]
		
		elif direction == "right":
			if character.tileOn.idx %gameMap.width == gameMap.width-1: #index off right side of board
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx + 1]

		elif direction == "left":
			if character.tileOn.idx % gameMap.width == 0: #index off left side of board:
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx - 1]

		elif direction == "down":
			if character.tileOn.idx >= (gameMap.width * (gameMap.length-1)): #index out of bounds
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx + gameMap.width]
		
		elif direction == "stay":
			tileTo = character.tileOn
		
		return tileTo

def main(gameMap = None): 
	if gameMap == None:
		while True:
			print("Do you want to generate the map yourself? (y/n)", end = ": ")
			inp = input()
			if inp == "y":
				while True:
					print("Input map width and length as two integers seperated by a space:", end=" ")
					width, length = [int(i) for i in input().split()]
					if (width * length) <= 1:
						print("Your input will not create a board larger than a single tile.")
					else:
						break

				gameMap = Map(True, width, length)
				while Algorithm.howWinnable(gameMap) is not True:
					gameMap = Map(True, width, length)
				break

			elif inp == "n":
				while True:
					print("Input map width and length as two integers seperated by a space:", end=" ")
					width, length = [int(i) for i in input().split()]
					if (width * length) <= 1:
						print("Your input will not create a board larger than a single tile.")
					else:
						break

				gameMap = Map(False, width, length)
				while Algorithm.howWinnable(gameMap) is not True:
					gameMap = Map(False, width, length)
				break

			else:
				print("Your answer was incorectly formated, try again.")

	char = Character(gameMap)
	turns = (gameMap.length * gameMap.width * 3)

	while char.tileOn.idx != gameMap.end and turns > 0:
		Map.drawMap(gameMap, char, gameMap.length, gameMap.width)
		Movement.lookAround(gameMap, char)
		print("")
		print("You have ", turns, " turns left.")
		while True:
			print("Enter a direction you want to go. (up/right/left/down/stay)")
			inp = input()

			if inp == "up" or inp == "right" or inp == "left" or inp == "down" or inp == "stay":
				break
			else:
				print("Your answer was incorectly formated, try again.")
		print("")

		tileGoingTo = Movement.getTileInDir(gameMap, char, inp)
		canMoveBool = Movement.canMove(char, tileGoingTo)
		if tileGoingTo != gameMap.map[gameMap.end] and canMoveBool:
			Movement.goToTile(char, tileGoingTo)
		elif canMoveBool is False:
			Movement.goToTile(char, char.tileOn)
		else:
			char.tileOn = gameMap.map[gameMap.end]
			print("You move to the end game area.")
		print(char.tileOn.idx,end=' ')
		print(gameMap.end)
		turns -= 1


	if char.tileOn.idx != gameMap.end:
		print("")
		print("You ran out of turns. You lose.")
	else:
		print("")
		print("You battle the boss!")
		print("... ... ...")
		print("... ...")
		print("...")
		print("You destroy him!")
		boss = 1000
		fightExp = math.ceil(boss/(char.charAtk+char.weaponAtk))			
		char.updateChar(fightExp, Gen.getWeapAsLoot(char), Gen.getReqAsLoot(char))
		print("You win! You finished with your char being")
		print("level ", char.level, " and ", char.exp, " experience points in.")
		main(gameMap)

if __name__ == "__main__":
	main()
