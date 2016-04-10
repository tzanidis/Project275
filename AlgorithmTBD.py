import Game
import math
import copy
import sys
from collections import deque

class Utilities():
	''' A class that determines a sub-optimal path for a map larger than 12 tiles.
	In general, the algorithm works better for large maps with a wide gap between start and end.
	This is due to the algorithm's assumptions in optimizing a path.
	
	Methods: distance_to_boss(), is_reachable(), boss_direction(), tile_xp(), priorities(), opposite_direction(),
	final_requirements(), search_for_req(), recurse()'''
	
	def __init__(self,gameMap):
		'''
		In initialization, algorithm will be started.
		Global variables are set during this phase before the recursive algorithm.
		
		Returns: A class of which the variable global_result will contain the algorithm's sub-optimal minimum XP.
		
		Running time analysis: Let n be the number of tiles. Take the smallest case: a 5x5 map.
		Under the assumption that the algorithm will path around any lone obstacles, the longest path
		would be from one corner of the map to another; a maximum of 8 tiles crossed. After crossing the 8 tiles,
		it will search for any final requirements. In an average case, this will also be relatively small since it
		does a breadth-first search of the area around it. Therefore, the big O running time will usually be O(log(n)).
		In the worst case, the final requirements needed to fight the boss are on the farthest-most tile from the boss tile.
		Additionally, the path to the boss could be cluttered with 'obstacle walls' that make the algorithm take an
		extreme detour-like path. In this case, the big O running time is O(n). (There are constants of n, but each tile
		is only searched once)
		
		Explanation for global variables:
		-As soon as boss is defeatable with sub-optimal path, make global_finished = True
		-If a requirement loot is found, make global_restart = True
		-Before running algorithm, prioritize gear needed to beat boss.
		-If boss is on top of a hill or on a gate, always try to find that 'specific' requirement first.
		-To make sure a character is always updated to latest recursive call, use global_character.
		-By putting in already searched tiles into global_searched_tiles, function won't revisit the same location
		under the assumption that it's already found the most optimal path to the same tile (not always true).
		-Clear global_searched_tiles when item is found: Incase there's another path available to boss through tiles
		that have already been traversed.
		'''
		self.global_finished = False
		self.global_restart = True #Start as True to initialize recursive function
		self.global_character = Game.Character(gameMap)
		self.global_priority = Utilities.priorities(gameMap,self.global_character)
		self.global_searched_tiles = set()
		self.global_result = 0
		
		#~ gameMap.drawMap(self.global_character,gameMap.length,gameMap.width) #For testing purposes only
		
		#Loop for global_restart to function.
		while True:
			if self.global_finished == True:
				return None
			elif self.global_restart == True:
				#Restart recursive function with new character and refresh searched tiles
				#If starting recursive calls, set global_restart as true to go into this case.
				self.global_restart = False
				self.global_searched_tiles = set()
				global_character_new = copy.deepcopy(self.global_character)
				self.global_result += Utilities.recurse(self, gameMap, global_character_new, "stay")
			else:
				#Assuming that map was tested for 'winnability', this case should not occur.
				print("Algorithm failed to find path, game is unwinnable?")
				return None
	
	def distance_to_boss(gameMap,characterTile):
		'''
		Explanation:
		Given the index of character tile and boss tile, finds the distance in tiles between the character and the final boss.
		
		Runs in constant time, assuming that the numbers are relatively small.
		
		Returns: Distance between character and boss tile.
		'''
		#Travel vertically until on the same width
		#Travel horizontally until reach boss
		bossTile = gameMap.end
		mapWidth = gameMap.width
		if characterTile > bossTile:
			if characterTile % mapWidth < bossTile % mapWidth:
				tiles = (characterTile + mapWidth - bossTile) // mapWidth
			else:
				tiles = (characterTile - bossTile) // mapWidth
			tileOn = characterTile - (mapWidth * tiles)
		elif characterTile < bossTile:
			if characterTile % mapWidth > bossTile % mapWidth:
				tiles = (bossTile - characterTile + mapWidth) // mapWidth
			else:
				tiles = (bossTile - characterTile) // mapWidth
			tileOn = characterTile + (mapWidth * tiles)
		tiles += abs(tileOn - bossTile)
		return tiles
	
	def is_reachable(gameMap,character,turns):
		'''
		Explanation: With given turns and not accounting for hills or gates, checks if boss is reachable in time.
		
		Returns: True if boss is reachable, False if not.
		'''
		if turns < distance_to_boss(gameMap,character):
			return False
		return True
	
	def boss_direction(gameMap,characterTile):
		'''
		Explanation: Returns the boss's direction relative to the character. If boss direction is diagonal from character,
		include two directions.
		Runs in constant time, assuming that the numbers are small.
		
		Returns: A list containing directions towards the boss. 
		If len(list) == 2, first direction in list will always be horizontal.
		'''
		directions = list()
		bossTile = gameMap.end
		#Check horizontal first
		bossHoriz = bossTile % gameMap.width
		characterHoriz = characterTile % gameMap.width
		horizDiff = characterHoriz - bossHoriz
		if horizDiff < 0:
			directions.append("right")
		elif horizDiff > 0:
			directions.append("left")
	
		if characterTile - horizDiff != bossTile:
			#If not on same horizontal plane, check vertical.
			if bossTile > characterTile:
				directions.append("down")
			else:
				directions.append("up")
		return directions
	
	def tile_xp(character, tile):
		'''Explanation: Quick redundant calculation that calculates the XP acquired on a tile.
		Returns: XP acquired on a tile.
		'''
		return tile.speed + math.ceil(tile.mob/(character.charAtk+character.weaponAtk))
	
	def priorities(gameMap, character):
		'''
		Explanation: Finds tile requirement of boss tile, then requirement of tiles beside it.
		Ignore tile side that character is unlikely to step on.
		
		Returns: List containing "Climbing Gear" and/or "Gate Key". Will omit one if character starts with
		the gear already.
		If len(list) == 2, the first element will be prioritized first.
		'''
		priorityList = list()
		directionSet = set(["stay","up","down","left","right"])
		for direction in Utilities.boss_direction(gameMap, character.tileOn.idx):
			directionSet.remove(direction)
		for direction in directionSet:
			if Game.Movement.getTileInDir(gameMap, character, direction) != None:
				if Game.Movement.getTileInDir(gameMap, character, direction).requirement == "hill" and character.gear[0] == None:
					if "Climbing Gear" not in priorityList:
						priorityList.append("Climbing Gear")
				elif Game.Movement.getTileInDir(gameMap, character, direction).requirement == "gate" and character.gear[1] == None:
					if "Gate Key" not in priorityList:
						priorityList.append("Gate Key")
		if "Climbing Gear" not in priorityList and character.gear[0]==None:
			priorityList.append("Climbing Gear")
		if "Gate Key" not in priorityList and character.gear[1]==None:
			priorityList.append("Gate Key")
		return priorityList
		
	def opposite_direction(direction):
		'''
		Explanation: Given a direction as a string, returns the opposite direction.
		Always constant running time.
		'''
		if direction == "left":
			return "right"
		elif direction == "right":
			return "left"
		elif direction == "up":
			return "down"
		elif direction == "down":
			return "up"
		elif direction == "stay":
			#Just return stay
			return "stay"
		else:
			print("Invalid direction entered.")
			return None
	
	def final_requirements(gameMap, character):
		'''
		Explanation: Assuming character is on final tile before boss, checks if they have the gear to go onto boss tile. 
		If not, find nearest tile with gear and then path back to tile.
		If entire map does not have needed gear, find nearest other gear first. After obtaining that gear,
		then search the entire map for needed gear again.
		
		After gear search, if character does not have weapon, find nearest tile with weapon. 
		If weapon cannot be found in all current accessible tiles, just fight the boss.
		
		Returns: A tuple containing XP needed to get gear and XP needed to get weapon.
		'''
		path = list()
		gear_xp = 0
		endTile = gameMap.map[gameMap.end]
		if endTile.requirement != "plains":
			#Check if already have requirements
			if endTile.requirement == "hill" and character.gear[0] == "Climbing Gear":
				pass
			elif endTile.requirement == "gate" and character.gear[1] == "Gate Key":
				pass
			else:
				while True:
					#Search for requirements until requirement found
					results = Utilities.search_for_req(gameMap, character,"obstacles")
					gear_xp += results[0]
					character = results[2]
					if endTile.requirement == "hill" and results[1] == "Climbing Gear":
						break
					elif endTile.requirement == "gate" and results[1] == "Gate Key":
						break
					
		
		#Look for weapon if character wields no weapon
		weapon_xp = 0
		if character.weaponAtk < 1:
			results = Utilities.search_for_req(gameMap, character,"weapon")
			if results != None:
				character = results[1]
				weapon_xp += results[0]
				
		return (gear_xp,weapon_xp)
	
	def search_for_req(gameMap, character, requirement):
		'''
		Explanation: Loop function that searches all tiles for requirements.
		Keeps all tiles searched in a set so search does not search a tile twice.
		Assigns a value to each tile based on the XP needed to get there; used to find XP gained when going back.
		
		Returns:
		If requirement == "obstacles", returns a tuple containing totalXP gained from path to requirementLoot and back, 
		the requirementLoot gained, and the updated character.
		If requirement == "weapon", returns the same except without the requirementLoot gained.
		'''
		#~ print("Searching for requirements: "+requirement)
		if requirement == "obstacles":
			#accessibleTile is a tuple that stores tile, character, current xp, and tile path
			accessibleTiles = [(Game.Movement.getTileInDir(gameMap, character, "up"),character,0,[character.tileOn]),
			(Game.Movement.getTileInDir(gameMap, character, "down"),character,0,[character.tileOn]),
			(Game.Movement.getTileInDir(gameMap, character, "left"),character,0,[character.tileOn]),
			(Game.Movement.getTileInDir(gameMap, character, "right"),character,0,[character.tileOn])]
			searchedTiles = set()
			current_xp = 0
			while accessibleTiles:
				accessedTile = accessibleTiles.pop(0)
				currChar = copy.deepcopy(accessedTile[1])
				currChar.tileOn = accessedTile[0]
				#Base Case: If tile already searched, skip
				if accessedTile[0] in searchedTiles:
					continue
				searchedTiles.add(accessedTile[0])
				#Base Case: Can't go on boss tile or None tile
				if accessedTile[0] == None or accessedTile[0] == gameMap.map[gameMap.end]:
					continue
				#Base Case: Can't go through tile where gear is required and character does not have
				if accessedTile[0].requirement == "hill" and currChar.gear[0] == None:
					continue
				if accessedTile[0].requirement == "gate" and currChar.gear[1] == None:
					continue
				tileXP = accessedTile[0].speed + math.ceil(accessedTile[0].mob/(currChar.charAtk+currChar.weaponAtk))
				current_xp = tileXP + accessedTile[2]
				totalGet = currChar.updateChar(tileXP,accessedTile[0].weaponLoot,None)
				if accessedTile[0].requirementLoot != None:
					#Make sure character does not already have gear.
					if (accessedTile[0].requirementLoot == "Climbing Gear") and (currChar.gear[0] == "Climbing Gear"):
						pass
					elif (accessedTile[0].requirementLoot == "Gate Key") and (currChar.gear[1] == "Gate Key"):
						pass
					else:
						#New gear found, calculate XP needed to return to end tile
						totalTileXP = 0
						while accessedTile[3]:
							previousTile = accessedTile[3].pop()
							tileXP = previousTile.speed + math.ceil(previousTile.mob/(currChar.charAtk+currChar.weaponAtk))
							currChar.updateChar(tileXP,(None, None),None)
							totalTileXP += tileXP
						currChar.updateChar(0,(None, None), accessedTile[0].requirementLoot)
						return (current_xp + totalTileXP, currChar.tileOn.requirementLoot,currChar)
				#If no gear found, add neighbours to accessibletiles
				accessibleTiles += [(Game.Movement.getTileInDir(gameMap, currChar, "up"),currChar,current_xp,accessedTile[3]+[currChar.tileOn]),
			(Game.Movement.getTileInDir(gameMap, currChar, "down"),currChar,current_xp,accessedTile[3]+[currChar.tileOn]),
			(Game.Movement.getTileInDir(gameMap, currChar, "left"),currChar,current_xp,accessedTile[3]+[currChar.tileOn]),
			(Game.Movement.getTileInDir(gameMap, currChar, "right"),currChar,current_xp,accessedTile[3]+[currChar.tileOn])]
			print("No gear found, gg kill yourself")
			return None
		elif requirement == "weapon":
			#accessibleTile is a tuple that stores tile, character, current xp, and tile path
			accessibleTiles = [(Game.Movement.getTileInDir(gameMap, character, "up"),character,0,[character.tileOn]),
			(Game.Movement.getTileInDir(gameMap, character, "down"),character,0,[character.tileOn]),
			(Game.Movement.getTileInDir(gameMap, character, "left"),character,0,[character.tileOn]),
			(Game.Movement.getTileInDir(gameMap, character, "right"),character,0,[character.tileOn])]
			searchedTiles = set()
			current_xp = 0
			while accessibleTiles:
				accessedTile = accessibleTiles.pop(0)
				currChar = copy.deepcopy(accessedTile[1])
				currChar.tileOn = accessedTile[0]
				#Base Case: If tile already searched, skip
				if accessedTile[0] in searchedTiles:
					continue
				searchedTiles.add(accessedTile[0])
				#Base Case: Can't go on boss tile or None tile
				if accessedTile[0] == None or accessedTile[0] == gameMap.map[gameMap.end]:
					continue
				#Base Case: Can't go through tile where gear is required and character does not have
				if accessedTile[0].requirement == "hill" and currChar.gear[0] == None:
					continue
				if accessedTile[0].requirement == "gate" and currChar.gear[1] == None:
					continue
				tileXP = accessedTile[0].speed + math.ceil(accessedTile[0].mob/(currChar.charAtk+currChar.weaponAtk))
				current_xp = tileXP + accessedTile[2]
				totalGet = currChar.updateChar(tileXP,accessedTile[0].weaponLoot,accessedTile[0].requirementLoot)
				if accessedTile[0].weaponLoot != (None,None):
					#Gear found, calculate XP needed to return to end tile
					totalTileXP = 0
					while accessedTile[3]:
						previousTile = accessedTile[3].pop()
						tileXP = previousTile.speed + math.ceil(previousTile.mob/(currChar.charAtk+currChar.weaponAtk))
						currChar.updateChar(tileXP,(None, None),None)
						totalTileXP += tileXP
					return (current_xp + totalTileXP,currChar)
				#If no gear found, add neighbours to accessibletiles
				accessibleTiles += [(Game.Movement.getTileInDir(gameMap, currChar, "up"),currChar,current_xp,accessedTile[3]+[currChar.tileOn]),
			(Game.Movement.getTileInDir(gameMap, currChar, "down"),currChar,current_xp,accessedTile[3]+[currChar.tileOn]),
			(Game.Movement.getTileInDir(gameMap, currChar, "left"),currChar,current_xp,accessedTile[3]+[currChar.tileOn]),
			(Game.Movement.getTileInDir(gameMap, currChar, "right"),currChar,current_xp,accessedTile[3]+[currChar.tileOn])]
			print("No weapon found, fight the boss anyway")
			return None
	def recurse(self, gameMap, character, lastDir):
		'''
		Explanation: Main function that uses all the above helper functions to calculate XP.
		Recursive function that creates recursive calls of a path from start to end.
		Once path is found, all recursive calls return an integer that is collected into global_result
		in the main function.
		Comments below outline how the algorithm functions (Warning: Alot of comments).
		
		Running time analysis: For one recursive call, is constant running time assuming all operations/functions
		run in constant running time.
		For total recursive calls, the running time is explained in __init()__.
		
		Returns: The sum of XP acquired on recurse()'s current tile and any further recursive calls.
		'''
		#~ print("I'm recursing: "+str(lastDir)+" and on "+str(character.tileOn))
		#Base Case: If solution already found, return an infinite number
		if self.global_finished or self.global_restart:
			return float('inf')
		if character.tileOn in self.global_searched_tiles:
			return float('inf')
		#Calculate tileXP. (Ignore if it's the first tile)
		if lastDir != "stay":
			curr_xp = Utilities.tile_xp(character, character.tileOn)
			dump = character.updateChar(curr_xp, character.tileOn.weaponLoot, None)
		else:
			curr_xp = 0
		#After all important base cases are conducted, add tile to 'searched'
		self.global_searched_tiles.add(character.tileOn)
		#Base Case: Item found on current tile that character doesn't have, 
		#restart recursive call and remove gear as a priority.
		if character.gear[0] == None and character.tileOn.requirementLoot == "Climbing Gear":
			#NOTE: Becareful of finalRequirements algorithm
			self.global_restart = True
			character.gear[0] = "Climbing Gear"
			if "Climbing Gear" in self.global_priority:
				self.global_priority.remove("Climbing Gear")
			self.global_character = copy.deepcopy(character)
			return curr_xp
		elif character.gear[1] == None and character.tileOn.requirementLoot == "Gate Key":
			self.global_restart = True
			character.gear[1] = "Gate Key"
			if "Gate Key" in self.global_priority:
				self.global_priority.remove("Gate Key")
			self.global_character = copy.deepcopy(character)
			return curr_xp
		#Make a copy of old character
		oldCharacter = copy.deepcopy(character)
		#Base Case: Is beside final boss tile, run last requirements.
		if Utilities.distance_to_boss(gameMap,character.tileOn.idx) == 1:
			#Guranteed to fight boss, just use a return.
			xpResults = Utilities.final_requirements(gameMap, character)
			#Compare XP needed to get weapon then fight boss and straight up fighting the boss
			#Take the smaller value
			boss = 1000
			newXP = xpResults[1] + math.ceil(boss/(character.charAtk+character.weaponAtk))
			oldXP = math.ceil(boss/(oldCharacter.charAtk+oldCharacter.weaponAtk))
			if newXP < oldXP:
				betterXP = newXP
			else:
				betterXP = oldXP
			#End recursive calls, and return boss_xp
			self.global_finished = True
			return xpResults[0] + curr_xp + betterXP 
		
		#Recursive Case: Move to next possible tile
		directions = Utilities.boss_direction(gameMap, character.tileOn.idx)
		old_directions = Utilities.boss_direction(gameMap, character.tileOn.idx) #Used incase after analysis, len(directions) == 0
		currTile = character.tileOn
		#Filters directions that are obstructed by obstacles. All filtered directions are initially toward boss.
		#Also filters direction if direction is tile that is came from.
		for direction in old_directions:
			if direction == Utilities.opposite_direction(lastDir):
				directions.remove(direction)
				continue
			tile = Game.Movement.getTileInDir(gameMap, character, direction)
			if tile != None:
				if character.gear[1] == None and tile.requirement == "gate":
					directions.remove(direction)
				if character.gear[0] == None and tile.requirement == "hill":
					directions.remove(direction)
			else:
				directions.remove(direction)
		#Figure out which direction to go, can be maximum of 2 directions
		if len(directions) == 2:
			#Directions is 2, both directions are walkable. Choose one with lowest xp.
			#However, if one of them has a key, prioritize key. (Include climbing gear)
			tile1 = Game.Movement.getTileInDir(gameMap, character, directions[0])
			tile2 = Game.Movement.getTileInDir(gameMap, character, directions[1])
			#Compare XPs. If equal, move in arbitrary direction.
			if Utilities.tile_xp(character, tile1) > Utilities.tile_xp(character, tile2):
				character.tileOn = tile2
				moving_direction = directions[1]
			else: #tile_xp(character, tile1) <= tile_xp(character, tile2)
				character.tileOn = tile1
				moving_direction = directions[0]
			#Check for weapon priorities (only if character has no weapon).
			if character.weaponAtk == 0:
				#Check if tiles have weapon
				if tile1.weaponLoot != (None,None):
					#Check if tile 2 has a weapon, and if its better
					if tile2.weaponLoot != (None, None) and tile2.weaponLoot[1] > tile1.weaponLoot[1]:
						character.tileOn = tile2
						moving_direction = directions[1]
					else:
						character.tileOn = tile1
						moving_direction = directions[0]
				elif tile2.weaponLoot != (None,None):
					character.tileOn = tile2
					moving_direction = directions[1]
			#Check for priorities (gear to pass gates/hills).
			#Prioritize items the most!
			if len(self.global_priority) > 0:
				for priority in self.global_priority:
					#If tile1 contains priority loot, go to tile1
					if priority == tile1.requirementLoot:
						if tile1.requirementLoot == tile2.requirementLoot:
							#If tiles have the same loot, ignore priority
							break
						character.tileOn = tile1
						moving_direction = directions[0]
						break
					#If tile2 contains priority loot, go to tile2
					elif priority == tile2.requirementLoot:
						character.tileOn = tile2
						moving_direction = directions[1]
						break
			#Finally after all the decision-making, call recursive function
			result = curr_xp + Utilities.recurse(self, gameMap, character, moving_direction)
			if result >= float('inf'):
				#If recommended direction doesn't work, use other direction
				character = copy.deepcopy(oldCharacter)
				if moving_direction == directions[0]:
					moving_direction = directions[1]
				else:
					moving_direction = direction[0]
				result = curr_xp + Utilities.recurse(self, gameMap, character, moving_direction)
			else:
				return result
		elif len(directions) == 1:
			#Only one way to move, therefore move there.
			character.tileOn = Game.Movement.getTileInDir(gameMap, character, directions[0])
			result = curr_xp + Utilities.recurse(self, gameMap, character, directions[0])
		#If len(directions) is not greater than 0, then dead end is reached!
		elif len(directions) == 0:
			result = float('inf')
		else:
			print("Unknown case! Terminate!")
		#Check if results result in a dead end
		if result >= float('inf'):
			#Attempt to use directions never tried before. If no directions work, return infinite.
			#Reset tile to initial tile
			#Possible improvement: Apply priorities here
			character.tileOn = currTile
			allDirections = set(["up","down","left","right"])
			#Omit direction that character came from until all paths have been tried.
			for direction in old_directions:
				allDirections.remove(direction)
			#For cases where dead end is not found on initial tile, remove direction whereas user came from.
			if lastDir != "stay":
				if Utilities.opposite_direction(lastDir) in allDirections:
					allDirections.remove(Utilities.opposite_direction(lastDir))
			#Now with all directions not tried yet, try them.
			for direction in allDirections:
				if Game.Movement.getTileInDir(gameMap,oldCharacter,direction) != None:
					character = copy.deepcopy(oldCharacter)
					character.tileOn = Game.Movement.getTileInDir(gameMap, character, direction)
					result = curr_xp + Utilities.recurse(self, gameMap, character,direction)
					if result < float('inf'):
						return result
				character.tileOn = currTile
			#If none of the other directions work, return dead end.
			return float('inf')
		else:
			return result

class Winnable():
	''' A class that checks if a map is winnable and the path expected.

	Methods: getPoint(), getLabel(), getMob(), getSpeed(), getRequirement(), getWeaponLoot(), 
	getWeapAsLoot(), getRequirementLoot(), getReqAsLoot()'''

	def isWinnable(gameMap):
		'''A function that checks if it can reach the end tile.'''

		character = Game.Character(gameMap)
		acquiredRequirements = set(character.gear)
		accessibleTiles = set()
		searchTiles = set([character.tileOn])
		specSearch = set()

		while searchTiles:
			tileTerm = searchTiles.pop()
			#Base cases
			if tileTerm in accessibleTiles: #Check if tile already checked
				continue
			if tileTerm.requirement == "gate": #Check if requirements contain gate key
				if "Gate Key" not in acquiredRequirements:
					specSearch.add(tileTerm)
					continue
			if tileTerm.requirement == "hill": #Check if requirements contain gear
				if "Climbing Gear" not in acquiredRequirements:
					specSearch.add(tileTerm)
					continue

			accessibleTiles.add(tileTerm) #Tile is accessible add to list of accessible tiles (accessibleTiles)

			if tileTerm.requirementLoot == "Gate Key" or tileTerm.requirementLoot == "Climbing Gear":
				if tileTerm.requirementLoot not in acquiredRequirements:
					acquiredRequirements.add(tileTerm.requirementLoot)
					if tileTerm.requirementLoot == "Gate Key":
						for term in specSearch:
							if term.requirement == "gate":
								searchTiles.add(term)
					elif tileTerm.requirementLoot == "Climbing Gear":
						for term in specSearch:
							if term.requirement == "hill":
								searchTiles.add(term)

			if tileTerm.label == "end": #if tile is end, game is winnable
				return True

			character.tileOn = tileTerm
			for direction in ["up","right","left","down"]:
				tile = Game.Movement.getTileInDir(gameMap, character, direction)
				if tile != None:
					searchTiles.add(tile)
		return False #checked all accessible tiles and not are end, game is not winnable

	def makeGraph(gameMap):
		'''A function that turns the list that is the games map into a graph represented by a dictionary'''

		graphAsDict = {}
		character = Game.Character(gameMap)
		for tile in gameMap.map:
			character.tileOn = tile
			neighborTileList = set()
			for direction in ["up","right","left","down", "stay"]:
				neighborTile = Game.Movement.getTileInDir(gameMap, character, direction)
				if neighborTile != None:
					neighborTileList.add(neighborTile)
			graphAsDict[tile] = neighborTileList

		return (graphAsDict)

	def drawPath(minPath, gameMap):
		'''A function that prints the path the AI took'''

		for index in range(gameMap.width*gameMap.length):
			tile = gameMap.map[index]
			if tile == gameMap.map[gameMap.start]:
				print('S',end='')

			elif tile == gameMap.map[gameMap.end]: #Decision for Boss tile
				print('E',end='')

			elif tile in minPath: #AI was on that tile
				print('*', end='')

			else: #DEFAULT TILE
				print('-',end='')

			print(" ",end='') #new line if at edge
			if (index+1)%gameMap.width==0:
				print("")

	def minExp(pathsFound, gameMap):
		'''A function that traces and calculates the exp of each path returning the minimum of the paths in terms of exp.'''

		pathsFoundExp = list()
		printed = False

		for aMinPath in pathsFound:
			character = Game.Character(gameMap)
			for step in aMinPath:
				canMoveBool = Game.Movement.canMove(character, step)
				if canMoveBool[0] and canMoveBool[1]:
					if step == gameMap.map[gameMap.end]:
						if printed is False:
							print("Game is winnable.")
							printed = True
		
						dump = character.updateChar(math.ceil(1000/(character.charAtk + character.weaponAtk)), Game.Gen.getWeapAsLoot(character), Game.Gen.getReqAsLoot(character))
						pathsFoundExp.append(( ( (character.level, character.exp),(len(aMinPath)) ),(aMinPath) ))
					else:
						Game.Movement.goToTile(character, step)
				else:
					break

		pathsFoundExpToMin = [i[0] for i in pathsFoundExp]
		minIdx = pathsFoundExpToMin.index(min(pathsFoundExpToMin))
		print("min exp path index:", minIdx)
		print("min exp", pathsFoundExp[minIdx][0][0]) #THIS IS THE (LVL, EXP)
		print("min path", pathsFoundExp[minIdx][1], end="\n\n") #THIS IS THE [PATH]
		print("Path taken by AI, not including any stays.")
		Winnable.drawPath(pathsFoundExp[minIdx][1], gameMap)
		print()
		return pathsFoundExp[minIdx][0][0]

	def minExpBrute(gameMap, turns):
		'''A function that finds ALL possible paths to the end.'''

		graph = Winnable.makeGraph(gameMap)
		start, end = gameMap.map[gameMap.start], gameMap.map[gameMap.end]
		q = deque([[start]])
		pathsFound = set()

		while q:
			tmpPath = q.popleft()
			lastNode = tmpPath[len(tmpPath)-1]

			if lastNode == end:
				pathsFound.add(tuple(tmpPath)[1:])
				#print("POSSIBLE PATH: ", tmpPath[1:])
			elif len(tmpPath) < (turns+1):
				for linkNode in graph[lastNode]:
					newPath = tmpPath + [linkNode]
					q.append(newPath)

		if len(pathsFound) == 0:
			return False, None
		else:
			return True, Winnable.minExp(pathsFound, gameMap)

def howWinnable(gameMap):
	'''A function that checks if the game is winnable,
	and print the expected minimum character level and exp requiered.
	Brute Force if less than 12 tiles: 100% accurate.
	Heuristics if larger than 12 tiles: accurate, but assumptions made.
	Returns if beatable or not.'''
	
	sys.setrecursionlimit(10000)
	numTiles = (gameMap.width * gameMap.length)
	if numTiles > 12:
		if Winnable.isWinnable(gameMap):
			print("Game is winnable... ")
			utility = Utilities(gameMap)
			win_exp = utility.global_result
			character = Game.Character(gameMap)
			character.updateChar(win_exp, (None,None), None)
			character.level
			print("min exp ",end="")
			print((character.level,character.exp))
			return True,(character.level, character.exp)
		else:
			print("Game is not winnable, making new map.")
			return False, None
	else:
		win_exp = Winnable.minExpBrute(gameMap, numTiles)
		if win_exp[0]:
			return win_exp
		else:
			print("Game is not winnable, making new map.")
			return False, None

if __name__ == "__main__":
	howWinnable(Game.Map(False))
