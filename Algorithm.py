import Game

class Winnable():

	def getAccessTiles(gameMap, accessibleTiles = None):
		character = Game.Character(gameMap)
		requirementsGotten = list()
		if accessibleTiles == None:
			accessibleTiles = [character.tileOn]

		searchTiles = accessibleTiles
		specSearch = list()
		while searchTiles:
			tileTerm = searchTiles.pop()
			#Base cases
			if tileTerm in accessibleTiles:
				continue
			if tileTerm.requirement == "gate":
				#Check if requirements contain gate key or gear
				if "Gate Key" not in requirementsGotten:
					specSearch.append(tileTerm)
					continue
			if tileTerm.requirement == "hills":
				if "Climbing Gear" not in requirementsGotten:
					specSearch.append(tileTerm)
					continue
			accessibleTiles.append(tileTerm)
			if tileTerm.requirementLoot == "Gate Key" or tileTerm.requirementLoot == "Climbing Gear":
				if tileTerm.requirementLoot not in requirementsGotten:
					requirementsGotten.append(tileTerm.requirementLoot)
					if tileTerm.requirementLoot == "Gate Key":
						for term in specSearch:
							if term.requirement == "gate":
								searchTiles.append(term)
					elif tileTerm.requirementLoot == "Climbing Gear":
						for term in specSearch:
							if term.requirement == "hills":
								searchTiles.append(term)
			if tileTerm.label == "end":
				break
			character.TileOn = tileTerm
			for direction in ["up","right","left","down","stay"]:
				tile = Game.Movement.getTileInDir(gameMap, character, direction)
				if tile != None:
					searchTiles.append(tile)



def isWinnable(gameMap):
	#create accesible tiles list
	accessibleTiles = getAccessTiles(gameMap)
	if gameMap.map[gameMap.end] is in accessibleTiles: #access includes end tile
		return True
	else:
		return False


if __name__ == "__main__":
	isWinnable(Game.Map(False))
