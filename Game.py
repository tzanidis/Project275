import random
import math
import Algorithm
import os

class Map: #Done And Commented
	'''A class that holds the tiles in a set order for later retrieval,
	along with other key pieces of information.
	
	Self Variables: map, user, width, length, start, end.
	map, a list of Tile classes.
	user, boolean of whether the user wants to generate the map themselves or not.
	width, an integer that is one of the dimensions of the grid.
	length, an integer that is one of the dimensions of the grid.
	start, an integer that is the index of the start tile in the list map.
	end, an integer that is the index of the end tile in the list map.
	
	Methods: __init__(), userMakeMap(), makeMap(), drawMap() __repr__().'''

	def __init__(self, user, width, length):
		'''A function that initializes all self variables whether it is user or computer generated.'''

		self.map = []
		self.user = user
		self.width = width
		self.length = length

		if self.user: #user input
			demand = "Input map start and end points as two integers seperated by a space starting with the start :"
			err = "Your input was incorrectly formated try again."
			self.start, self.end = getInput(demand, err, 2, None, (self.width*self.length))
			
			label = Gen.getLabel(self.start, self.end, self.length, self.width)
			self.userMakeMap(label)

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

	def userMakeMap(self, label):
		'''A function that calls all the tiles to be made for the holder.'''

		for x in range(self.width * self.length):
			print("The following inputs will be for tile ", x)
			self.map.append(Tile(self.user, x, label[x]))

	def makeMap(self, label, mob, speed, requirement, requirementLoot, weaponLoot):
		'''A function that calls all the tiles to be made for the holder.'''
		
		for x in range(self.width * self.length):
			self.map.append(Tile(self.user, x, label[x], mob[x], speed[x], requirement[x], requirementLoot[x], weaponLoot[x]))

	def drawMap(gameMap,character, length, width):
		'''A function that draws a representation of the map in ascii keys.'''

		for index in range(width*length):
			tile = gameMap.map[index]
			if tile == character.tileOn:
				print('@',end='')
			elif tile.label == "end": #Decision for Boss tile
				if tile.requirement == "gate" or tile.requirement == "hill":
					print('b',end='')
				else:
					print('B',end='')

			elif tile.requirement == "gate": #Decision for Gate tiles
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

			elif tile.requirement == "hill": #Decision for Hill tiles
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

			elif tile.requirementLoot == "Gate Key" and character.gear[1] == None: #Tile if Gate Key on tile
				print('K',end='')

			elif tile.requirementLoot == "Climbing Gear" and character.gear[0] == None: #Tile if Climbing Gear on tile
				print('C',end='')

			else: #DEFAULT TILE
				print('-',end='')

			print(" ",end='') #new line if at edge
			if (index+1)%width==0:
				print("")

		#Print Legend
		print("\n? = character, B = boss (lowercase if hill/gate exists on tile), K = gate key, C = climbing gear\nH = hill (lowercase if key/gear exists on tile), G = gate (lowercase if key/gear exists on tile)")

	def __repr__ (self):
		'''print(Map) prints returned string.'''
		rep = ""
		for x in range(self.width * self.length):
			rep += str(self.map[x])
		return rep
			
class Tile: #Done And Commented
	'''A class that contains variables which makeup each tile.

	Self Variables: user, idx, label, mob, speed, requirement, requirementLoot, weaponLoot.
	user, is a boolean that denotes whether the user will create the tile or if it will be randomly generated.
	label, which will be one of three possible strings that outline the border of the map, start and end points.
	mob, an integer which denotes monsters are present on the tile specifically the int being the monsters health points.
	speed, an integer which denotes the speed or experience points given by a tile.
	requirement, a string that requires gear to be able to move to that tile.
	requirementLoot, a string that is the gear requiered to move through other tiles.
	weaponLoot, a tuple: string, integer that is a weapons name and damage.

	Methods: __init__(), userMakeTile(),  makeTile(), __repr__().'''

	def __init__(self, user, idx, label, mob = None, speed = None, requirement = None, requirementLoot = None, weaponLoot = None):
		'''A function that calls functions to initialize all self variables whether it is user or computer generated.'''

		if user:
			self.userMakeTile(idx, label)
		else:
			self.makeTile(idx, label, mob, speed, requirement, requirementLoot, weaponLoot)

	def userMakeTile(self, idx, label):
		'''A function that initializes all the classes variables generated by the users input.'''

		self.label = label
		self.idx = idx

		demand = "Input mob hit points for this tile (input 0 if no mob), as a positive integer:"
		err = "Your input was negative, try again."
		self.mob = getInput(demand, err, 3)

		demand = "Input speed it takes to cross this tile as a positive integer greater or equal to 0:"
		self.speed = getInput(demand, err, 3)
		
		demand = "Input requirement to travel accross this tile (hill/gate/plains if no requirement):"
		iterable = ["hill", "gate", "plains"]
		err = "Your answer was incorectly formated, try again."
		self.requirement = getInput(demand, err, 0, iterable)

		demand = "Input gear to travel accross tiles that have requirements (Climbing Gear/Gate Key/ None if no gear):"
		iterable = ["Climbing Gear","Gate Key", "None"]
		val = getInput(demand, err, 0, iterable)
		if val == "None":
			self.requirementLoot = None
		else:
			self.requirementLoot = val

		demand = "Input a weapon name then the damage it does seperated by a space (Sword 14), that damage being a positive integer"
		self.weaponLoot = getInput(demand, err, 4)

	def makeTile(self, idx, label, mob, speed, requirement, requirementLoot, weaponLoot):
		'''A function that initializes all the classes variables that have been computer generated.'''

		self.label = label
		self.idx = idx
		self.mob = mob
		self.speed = speed
		self.requirement = requirement
		self.requirementLoot = requirementLoot
		self.weaponLoot = weaponLoot

	#def __eq__(self, other):
	#	return self

	def __repr__ (self):
		'''print(Tile) prints returned string.'''

		return "|" + str(self.label) + ", idx: " + str(self.idx) + ", req: " + str(self.requirement) +"|"

class Character: #Done And Commented
	'''A class that contains variables which make the character.
	
	Self Variables: weaponName, weaponAtk, level, charAtk, exp, lvlUpExp, gear, tileOn.
	weaponName, an unused arbitrary string for the weapons name.
	weaponAtk, an integer that is the weapons damage.
	level, an integer which is a measuremen of "speed" or "distance".
	charAtk, the characters damage increased by the characters level.
	exp, an integer which is a measuremen of "speed" or "distance".
	lvlUpExp, and integer that when exp is equivalent the characters level is increased.
	gear, a tuple that contains the gear aquired by the character.
	tileOn, the tile the character is on.

	Methods: __init__(), updateChar().'''

	def __init__(self, gameMap):
		'''A function that initializes all self variables.'''

		self.weaponName = None
		self.weaponAtk = 0
		self.level = 1
		self.charAtk = 2*self.level
		self.exp = 0
		self.lvlUpExp = 50*self.level
		self.gear = [None]*2
		self.tileOn = gameMap.map[gameMap.start]

	def updateChar(self, gainedExp, weapon, gear):
		'''A function that updates all self values after each tile movement is made.'''

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

class Gen: #Done And Commented
	''' A class that uses random to generate all kinds of variables

	Methods: getPoint(), getLabel(), getMob(), getSpeed(), getRequirement(), getWeaponLoot(), 
	getWeapAsLoot(), getRequirementLoot(), getReqAsLoot()'''

	def getPoint(length, width):
		'''A function that picks a random number within the limits of the maps size.'''

		return random.randrange(0, (length * width))

	def getLabel(start, end, length, width):
		'''A function that makes a list of strings that indicate the following: the tile is the starting tile, 
		end tile, a tile on the edge, or the tile is in the middle of the board.'''

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
		'''A function that makes a list of integer that indicate whether the tile has a monster or not and its hit points.'''

		mob = []
		for x in range(length*width):
			if random.randrange(5) <= 3:
				mob.append(random.randrange(10, 200))
			else:
				mob.append(0)

		return mob

	def getSpeed(length, width):
		'''A function that makes a list of integers that are a measurement of the tiles "speed" or "distance" to cross it.'''

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
		'''A function that makes a list of strings that indicate whether the tile has specific requirements or not.'''

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
		'''A function that makes a list of tuples: (string, integer) representing a weapon for each tile,
		the string being the weapons names and the integer being the weapons damage.'''

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
		'''A function that checks if the tile the character is on has a weapon.'''

		if character.tileOn.weaponLoot != None:
			loot = character.tileOn.weaponLoot
			return loot
		else:
			return None

	def getRequirementLoot(length,width):
		'''A function that makes a list of strings that is the gear for that tile.'''

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
		'''A function that checks if the tile the character is on has any gear.'''

		if character.tileOn.requirementLoot != None:
			loot = character.tileOn.requirementLoot
			return loot
		else:
			return None

class Movement: #Done And Commented
	''' A class that deals with all character moving properties.

	Methods: canMove(), goToTile(), lookAround(), examineTile(), getTileInDir().'''

	def canMove(character, tileTo):
		'''A function that checks if you can move to a certain tile.'''

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
			return False, False

	def goToTile(character, tileTo):
		'''A function that takes a tile the character is going to, 
		checks if it is possible to go to, and updates the character based on the new tile.'''

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

	def lookAround(gameMap, character):
		'''A function that calls a different function 5 times.
		Pretty pointless, but clean looking.'''

		print("")
		print("You look around and see:")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "up"), "up")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "right"), "right")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "left"), "left")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "down"), "down")
		Movement.examineTile(Movement.getTileInDir(gameMap, character, "stay"), "stay")

	def examineTile(tile, direction):
		'''A function that describes a tile.
		Future note could be replaced by a different __repr__() in Tile.'''

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
		'''A function that takes a direction and finds the tile in that direction.
		Returns None if there is no tile there.'''
		
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

def getInput(demand, err, specialCase, iterable = None, numTiles = None): #Done And Commented
	'''A function that will ask check and return a users input.'''

	print(demand, end = " ")
	if iterable != None:
		inp0 = input()
		while inp0 not in iterable:
			print(err)
			print(demand, end = " ")
			inp0 = input()
		return inp0

	else:
		if specialCase == 1:
			while True:
				try:
					inp0, inp1 = [int(i) for i in input().split()]
					if (inp0 * inp1) <= 1:
						print(err)
						print(demand, end = " ")
					else:
						return inp0, inp1
				except:
					print(err)
					print(demand, end = " ")

		elif specialCase == 2:
			while True:
				try:
					inp0, inp1 = [int(i) for i in input().split()]
					if (inp0 == inp1) and (inp0 not in range(0,(numTiles)-1)) and (inp1 not in range(0,(numTiles)-1)):
						print(err)
						print(demand, end = " ")
					else:
						return inp0, inp1
				except:
					print(err)
					print(demand, end = " ")

		elif specialCase == 3:
			while True:
				try:
					inp0 = int(input())
					if inp0 < 0:
						print(err)
						print(demand, end = " ")
					else:
						return inp0
				except:
					print(err)
					print(demand, end = " ")

		elif specialCase == 4:
			while True:
				try:
					inp0, inp1 = input().split()
					if int(inp1) < 0:
						print(err)
						print(demand, end = " ")
					else:
						return inp0, int(inp1)
				except:
					print(err)
					print(demand, end = " ")

def play(character, gameMap): #Done And Commented
	'''A function that manages the core game-play.'''

	turns = (gameMap.length * gameMap.width)
	while character.tileOn.idx != gameMap.end and turns > 0:
		Map.drawMap(gameMap, character, gameMap.length, gameMap.width)
		Movement.lookAround(gameMap, character)
		print("")
		print("You have ", turns, " turns left.")
		iterable = ["up", "left", "right", "down", "stay"]
		demand = "Enter a direction you want to go. (up/right/left/down/stay): \n"
		err = "Your answer was incorectly formated, try again."
		inp = getInput(demand, err, 0, iterable)

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
		elif tileTo == gameMap.map[gameMap.end] and moveBools[0] and moveBools[1]:
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

def main(gameMap = None): #Done And Commented
	'''THE function that initializes the entire game and runs the game.'''

	########################################### Create Game Map ##############################################
	if gameMap == None:
		iterable = ["y","n"]
		demand = "Do you want to generate the map yourself? (y/n):"
		err = "Your answer was incorectly formated, try again."
		inp = getInput(demand, err, 0, iterable)
		
		if inp == "y":
			demand = "Input map width and length as two integers seperated by a space:"
			err = "Your input will not create a board larger than a single tile."
			width, length = getInput(demand, err, 1)
			gameMap = Map(True, width, length)
			win_exp = Algorithm.howWinnable(gameMap)
			while win_exp[0] is False:
				gameMap = Map(True, width, length)
				win_exp = Algorithm.howWinnable(gameMap)

			
		else:
			demand = "Input map width and length as two integers seperated by a space:"
			err = "Your input will not create a board larger than a single tile."
			width, length = getInput(demand, err, 1)
			gameMap = Map(False, width, length)
			win_exp = Algorithm.howWinnable(gameMap)
			while win_exp[0] is False:
				gameMap = Map(False, width, length)
				win_exp = Algorithm.howWinnable(gameMap)


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
		print("The computers best was: level", win_exp[1][0], ", experience", win_exp[1][1])

if __name__ == "__main__":
	main()
