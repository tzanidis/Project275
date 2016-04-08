import Game
import math
from collections import deque

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
			if tileTerm.requirement == "hills": #Check if requirements contain gear
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
							if term.requirement == "hills":
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

	numTiles = (gameMap.width * gameMap.length)
	if numTiles > 12:
		if Winnable.isWinnable(gameMap):
			print("Game is winnable... ")
			Winnable.minPath(gameMap)
			return True
		else:
			print("Game is not winnable, making new map.")
			return False
	else:
		win_exp = Winnable.minExpBrute(gameMap, numTiles)
		if win_exp[0]:
			return win_exp
		else:
			print("Game is not winnable, making new map.")
			return False, None

if __name__ == "__main__":
	howWinnable(Game.Map(False))
