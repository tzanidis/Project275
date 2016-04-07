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

	def updateChar(self, gainedExp, weapon, gear):
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

		if gear != None:
			if gear == "Climbing Gear" and self.gear[0] == None:
				self.gear[0] = gear
				return gear, weapon[0], weapon[1]
			elif gear == "Gate Key" and self.gear[1] == None:
				self.gear[1] = gear
				return gear, weapon[0], weapon[1]
		return None, None, None

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
			return loot
		else:
			return None

class Movement:
	''' A class that uses random to generate all kinds of variables

	Arguments:

	Self Variables: None

	Methods: getPoint(), getLabel(), getMob(), getSpeed(), getRequirement(), getLoot(), getRequirementAsLoot()'''

	def canMove(character, tileTo): #DONE done
			if tileTo is not None:
				if tileTo.requirement == "hill":
					if character.gear[0] != None:
						return True, True
					else:
						return True, False

				if tileTo.requirement == "gate":
					if character.gear[1] != None:
						return True, True
					else:
						return True, False

				return True, True
			else:
				return False, None

	def goToTile(character, tileTo):
		############################################## CanMove #################################################
		moveBools = Movement.canMove(character, tileTo)
		if moveBools[0] and moveBools[1]:
				character.tileOn = tileTo
		########################################################################################################

		###################################### Fight Mob & Tile Exp ############################################
		fightExp = math.ceil(character.tileOn.mob/(character.charAtk+character.weaponAtk))
		gainedExp = fightExp + character.tileOn.speed
		########################################################################################################

		######################################### Update Character #############################################
		items = character.updateChar(gainedExp, Gen.getWeapAsLoot(character), Gen.getReqAsLoot(character))
		########################################################################################################
		return fightExp, gainedExp, items[0], items[1], items[2]

	def lookAround(gameMap, character):#DONE done
		print("")
		print("You look around and see:")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "up"), "up")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "right"), "right")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "left"), "left")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "down"), "down")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "stay"), "stay")

	def examineTile(tile, direction):#DONE done
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

	def getTileInDir(gameMap, character, direction):#DONE done
		
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

def getInput(demand, err, iterable = None):
	print(demand, end = " ")
	if iterable != None:
		inp0 = input()
		while inp0 not in iterable:
			print(err)
			print(demand, end = " ")
		return inp0

	else:
		inp0, inp1 = [int(i) for i in input().split()]
		while (inp0 * inp1) <= 1:
			print(err)
			print(demand, end = " ")
		return inp0, inp1

def play(character, gameMap):
	turns = (gameMap.length * gameMap.width)
	while character.tileOn.idx != gameMap.end and turns > 0:
		Map.drawMap(gameMap, character, gameMap.length, gameMap.width)
		Movement.lookAround(gameMap, character)
		print("")
		print("You have ", turns, " turns left.")
		iterable = ["up", "left", "right", "down", "stay"]
		demand = "Enter a direction you want to go. (up/right/left/down/stay): \n"
		err = "Your answer was incorectly formated, try again."
		inp = getInput(demand, err, iterable)

		tileTo = Movement.getTileInDir(gameMap, character, inp)
		############################################## CanMove #################################################
		moveBools = Movement.canMove(character, tileTo)
		if tileTo != gameMap.map[gameMap.end] and moveBools[0]: #tile not None
			if moveBools[1]: #can move past obstacle
				if tileTo.requirement is not "plains": #is there an obstacle
					print("You deal with and move past the", tileTo.requirement, "that was in your way.")
				else: #there isn't
					print("You move freely in that direction")
				update = Movement.goToTile(character, tileTo)
			else:
				print("You are blocked by a", tileTo.requirement)
				print("Instead you wander around the same area you are in.")
				update = Movement.goToTile(character, tileTo)
		elif tileTo == gameMap.map[gameMap.end]:
			print("You move to the end game area")
			character.tileOn = tileTo
			break
		else: #tile None
			print("The world dissapears, you do not move continue in that direction.")
			print("Instead you wander around the same area you are in.")
			update = Movement.goToTile(character, tileTo)
		########################################################################################################
		###################################### Fight Mob & Tile Exp ############################################
		if update[0] == 0:
			print("You pass through without encounters.")
		else:
			print("You defeat a monster that tries to fight you. You gain", update[0], "xp the monster.")
		print("You gained", update[1], "total in this land.")
		########################################################################################################
		######################################### Update Character #############################################
		if update[3] != None:
			print("You got a", update[3], "and it does", update[4], "dmg.")
		else:
			print("You didn't get a new weapon.")

		if update[2] != None:
			print("You got", update[2], ".")
		else:
			print("You didn't get any gear.")

		print("Your character is now level", character.level, "and has", character.exp, "experience points.")
		########################################################################################################

		turns -= 1

def main(gameMap = None): 
	########################################### Create Game Map ##############################################
	if gameMap == None:
		iterable = ["y","n"]
		demand = "Do you want to generate the map yourself? (y/n):"
		err = "Your answer was incorectly formated, try again."
		inp = getInput(demand, err, iterable)
		
		if inp == "y":
			demand = "Input map width and length as two integers seperated by a space:"
			err = "Your input will not create a board larger than a single tile."
			width, length = getInput(demand, err)
			gameMap = Map(True, width, length)
			while Algorithm.howWinnable(gameMap) is not True:
				gameMap = Map(True, width, length)
			
		else:
			demand = "Input map width and length as two integers seperated by a space:"
			err = "Your input will not create a board larger than a single tile."
			width, length = getInput(demand, err)
			gameMap = Map(False, width, length)
			while Algorithm.howWinnable(gameMap) is not True:
				gameMap = Map(False, width, length)

	########################################## Create Character ##############################################
	char = Character(gameMap)
	if char.tileOn.requirement == "hill":
		print("You start with Climbing Gear.")
		char.gear[0] = "Climbing Gear"
	elif char.tileOn.requirement == "gate":
		print("You start with a Gate Key.")
		char.gear[1] = "Gate Key"

	############################################# Play Game ##################################################
	play(char, gameMap)

	############################################## End Game ##################################################
	if char.tileOn.idx != gameMap.end:
		print("You ran out of turns. You lose.")
	else:
		dump = char.updateChar(math.ceil(1000/(char.charAtk+char.weaponAtk)), Gen.getWeapAsLoot(char), Gen.getReqAsLoot(char))
		print("You find, battle, and destroy the boss!")
		print("You win! You finished with your chararacter being")
		print("level ", char.level, " and ", char.exp, " experience points in.")

if __name__ == "__main__":
	main()
