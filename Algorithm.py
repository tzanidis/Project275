import Game
import math
from collections import deque

class Winnable():

	def isWinnable(gameMap):
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

	def minExp(pathsFound, gameMap):
		pathsFoundExp = set()
		printed = False

		for aMinPath in pathsFound:
			character = Game.Character(gameMap)
			for step in aMinPath:
				canMoveBool = Game.Movement.canMove(character, step)
				if canMoveBool:
					if step == gameMap.map[gameMap.end]:
						if printed is False:
							print("Game is winnable.")
							printed = True
		
						dump = character.updateChar(math.ceil(1000/(character.charAtk + character.weaponAtk)), Game.Gen.getWeapAsLoot(character), Game.Gen.getReqAsLoot(character))
						pathsFoundExp.add((character.level, character.exp))
					else:
						Game.Movement.goToTile(character, step)
				else:
					break

		print(min(pathsFoundExp))
		return min(pathsFoundExp)

	def minExpBrute(gameMap, turns):
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

		return Winnable.minExp(pathsFound, gameMap)

def howWinnable(gameMap):
	numTiles = (gameMap.width * gameMap.length)
	if numTiles > 12:
		if Winnable.isWinnable(gameMap):
			print("Game is winnable... ")
			Winnable.minPath(gameMap) #Assumes you will accumulate adequate damage
			return True
		else:
			print("Game is not winnable, making new map.")
			return False
	else:
		if Winnable.minExpBrute(gameMap, numTiles):
			return True
		else:
			print("Game is not winnable, making new map.")
			return False

if __name__ == "__main__":
	howWinnable(Game.Map(False))
