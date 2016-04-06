import Game

class Winnable():

	def isWinnable(gameMap):
		character = Game.Character(gameMap)
		requirementsGotten = set(character.gear)
		accessibleTiles = set()
		searchTiles = set([character.tileOn])
		specSearch = set()

		while searchTiles:
			tileTerm = searchTiles.pop()
			#Base cases
			if tileTerm in accessibleTiles: #Check if tile already checked
				continue
			if tileTerm.requirement == "gate": #Check if requirements contain gate key
				if "Gate Key" not in requirementsGotten:
					specSearch.add(tileTerm)
					continue
			if tileTerm.requirement == "hills": #Check if requirements contain gear
				if "Climbing Gear" not in requirementsGotten:
					specSearch.add(tileTerm)
					continue

			accessibleTiles.add(tileTerm) #Tile is accessible add to list of accessible tiles (accessibleTiles)

			if tileTerm.requirementLoot == "Gate Key" or tileTerm.requirementLoot == "Climbing Gear":
				if tileTerm.requirementLoot not in requirementsGotten:
					requirementsGotten.add(tileTerm.requirementLoot)
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
	
	#def minExp(gameMap):
		'''
		Ideas:
		Brute force every path. O(5^n) if n = map tiles
		Two 'AI's' (heuretics needed):
		1) Low level and find a weapon, then path to boss (path around locations based on movement)
		2) High level then path to boss on last turn/or until boss is defeated efficiently
		Final) Get high attack and then path to boss. Path to boss when attack is efficiently high at killing boss.


		'''

	#def minTurns(gameMap):
		#lol easy


def howWinnable(gameMap):
	if Winnable.isWinnable(gameMap):
		print("Game is winnable... ")
		#Winnable.minExp(gameMap)
		#Winnable.minTurns(gameMap)?
		return True

	else:
		print("Game is not winnable, making new map.")
		return False

if __name__ == "__main__":
	howWinnable(Game.Map(False))
