import random
import math

class Map:
	'''A class that holds the tiles in a set order for later retrieval.
	
	Arguments: user, is a boolean that denotes whether the user will create the map or if it will be randomly generated.
	
	Self Variables: map, start, end, length, width, user.
	
	Methods: make_map(), user_make_map().'''

	def __init__(self, user):
		self.map = []
		self.user = user		
		print("Input map length and width as two integers seperated by a space:", end=" ")
		self.length, self.width = [int(i) for i in input().split()]

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
			self.userMakeMap(label)

		else: #gen input
			self.start = Gen.getPoint(self.length, self.width) #get rand start
			self.end = Gen.getPoint(self.length, self.width) #get rand end
			label = Gen.getLabel(self.start, self.end, self.length, self.width)
			mob = Gen.getMob(self.length, self.width)
			speed = Gen.getSpeed(self.length, self.width)
			requirement = Gen.getRequirement(self.length, self.width)
			
			self.makeMap(label, mob, speed, requirement)

		print("Map made.")


	def userMakeMap(self, label):
		for x in range(self.width * self.length):
			print("/nThe following inputs will be for tile ", x)
			self.map.append(Tile(self.user, x, label[x]))

	def makeMap(self, label, mob, speed, requirement):
		for x in range(self.width * self.length):
			self.map.append(Tile(self.user, x, label[x], mob[x], speed[x], requirement[x]))
			if x%self.width == 0 and x != 0:
				print("")
			print("|", x, "|", end = "")
			

class Tile:
	'''A class that contains variables which makeup each tile.

	Arguments: user, is a boolean that denotes whether the user will create the tile or if it will be randomly generated.
	label, which will be one of three possible strings that outline the border of the map, start and end points.
	mob, an integer which denotes monsters are present on the tile specifically the int being the monsters health points.
	speed, an integer which denotes the speed or experience points given by a tile.
	requirement, a string that requires gear to be able to move to that tile.
	
	Self Variables: user, idx, label, mob, speed, requirement.

	Methods: make_tile(), user_make_tile().'''
	def __init__(self, user, idx, label, mob = None, speed = None, requirement = None):
		if user is True:
			self.userMakeTile(idx, label)
		else:
			self.makeTile(idx, label, mob, speed, requirement)

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



	def makeTile(self, idx, label, mob, speed, requirement):
		self.label = label
		self.idx = idx
		self.mob = mob
		self.speed = speed
		self.requirement = requirement

class Character:
	'''A class that contains variables which makeup each tile.

	Arguments: start, to initialize the staring tile.
	
	Self Variables: weaponName, weaponAtk, level, charAtk, exp, lvlUpExp, gear, tileOn, tileLast.

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
		self.tileLast = gameMap.map[gameMap.start]

	def updateChar(self, gainedExp, weapon = None, gear = None):
		self.exp += gainedExp
		if self.exp >= self.lvlUpExp:
			self.exp -= self.lvlUpExp
			self.level += 1
			self.charAtk = 2*self.level
			self.lvlUpExp = 50*self.level

		if weapon != None:
			if self.weaponAtk <= int(loot[1]):
				self.weaponName = loot[0]
				self.weaponAtk = int(loot[1])

		if gear != None:
			if gear == "Climbing Gear" and self.gear[0] == None:
				self.gear[0] = gear
			elif self.gear[1] == None:
				self.gear[1] = gear

class Gen:
	''' A class that uses random to generate all kinds of variables

	Self Variables: None

	Methods: getPoint(), getLabel(), getMob(), getSpeed(), getRequirement(), getLoot(), getRequirementAsLoot()'''

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
			if random.randrange(1, 4) <= 3:
				mob.append(random.randrange(10, 200))
			else:
				mob.append(0)

		return mob


	def getSpeed(length, width):
		speed = []
		for x in range(length*width):
			rnum = random.randrange(1, 4)
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
			rnum = random.randrange(1,30)
			if rnum == 30 :
				requirement.append("gate")
			elif rnum in range(20, 29):
				requirement.append("hill")
			else:
				requirement.append("plains")

		return requirement

	def getLoot(mobHp):
		if random.randrange(1,2) == 2:
			rnum = random.randrange(1,(mobhp//4))
			loot = ("Sword of jibberishishish ", str(rnum))
			print("You got a ", loot, ".")
			return loot
		else:
			return None

	def getRequirementAsLoot():
		if random.randrange(1,30) == 30:
			if random.randrange(1,2) == 2:
				loot = "Climbing Gear"
			else:
				loot = "Gate Key"
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
				print("The world dissapears there, you do not move up.") 
				return False
		else:
			if Movement.checkReq(character, tileTo):
				return True
			else:
				return False

	def checkReq(character, tileTo):
		if tileTo.requirement == "gate":
			if character.gear[1] != None:
				character.gear[1] = None
				print("You unlock and go through the gate with your gate key, which remains stuck in the gate.")
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
			print("You move onwards.")
		else:
			print("You stay in the land you already are.")

		gainedExp = Movement.fightMob(character) + character.tileOn.speed
		print("You gained ", gainedExp, " total in this land.")
		character.updateChar(gainedExp, Gen.getLoot(character.tileOn.mob), Gen.getRequirementAsLoot())	

	def lookAround(gameMap, character):
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "up"), "up")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "right"), "right")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "left"), "left")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "down"), "down")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "stay"), "stay")

	def examineTile(tile, direction):
		if tile is not None:
			if tile.requirement == "gate":
				print(direction, ", there is a gate", end=" ")
			elif tile.requirement == "hill":
				print(direction, ", there is a hill", end=" ")
			else:
				print(direction, ", there are grassy plains", end=" ")

			if tile.mob != 0:
				print("and has monsters.")
			else:
				print("and has no monsters.")
		else:
			print("There is no land ", direction)

	def getTileInDir(gameMap, character, direction):
		
		if direction == "up":
			if (character.tileOn.idx - gameMap.width) < 0: #negative index
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx - gameMap.width]
		
		elif direction == "right":
			if (character.tileOn.idx + 1)%gameMap.width == 1: #index off right side of board
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx + 1]

		elif direction == "left":
			if (character.tileOn.idx - 1)%gameMap.width == gameMap.width - 1: #index off left side of board:
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx - 1]

		elif direction == "down":
			if (character.tileOn.idx + gameMap.width) > (gameMap.length * gameMap.width): #index out of bounds
				tileTo = None
			else:
				tileTo = gameMap.map[character.tileOn.idx + (gameMap.width-(character.tileOn.idx%gameMap.width))]
		
		elif direction == "stay":
			tileTo = character.tileOn
		
		return tileTo

def main(): 
	while True:
		print("Do you want to generate the map yourself? (y/n)", end = ": ")
		inp = input()
		if inp == "y":
			gameMap = Map(True)
			break
		elif inp == "n":
			gameMap = Map(False)
			break
		else:
			print("Your answer was incorectly formated, try again.")

	char = Character(gameMap)
	turns = 0

	while char.tileOn != gameMap.end or turns <= (gameMap.length * gameMap.width * 3):
		Movement.lookAround(gameMap, char)
		print("You have ", ((gameMap.length * gameMap.width * 3) - turns), " turns left.")
		print("")
		while True:
			print("Enter a direction you want to go. (up/right/left/down/stay)")
			inp = input()

			if inp == "up":
				break
			elif inp == "right":
				break
			elif inp == "left":
				break
			elif inp == "down":
				break
			elif inp == "stay":
				break
			else:
				print("Your answer was incorectly formated, try again.")

		direction = inp
		tileTo = Movement.getTileInDir(gameMap, char, direction)
		Movement.goToTile(char, tileTo)
		turns += 1

	if turns > (gameMap.length * gameMap.width * 3) and char.tileOn != gameMap.end:
		print("You ran out of turns. You lose.")
	else:
		print("You battle the boss!")
		print("... ... ...")
		print("... ...")
		print("...")
		print("You destroy him!")
		boss = 1000
		fightExp = math.ceil(boss/(char.charATK+char.weaponAtk))			
		updateChar(fightExp, getLoot(boss), getRequirementAsLoot())
		print("You win! You finished with your char being")
		print("level ", char.level, " and ", char.exp, " experience points.")

if __name__ == "__main__":
	main()
