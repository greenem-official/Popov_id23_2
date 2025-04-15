import json
import os.path

from Labs.Lab3 import DataStash
from Labs.Lab3.Planet import Planet


class Simulation:
    def __init__(self, data):
        self.data = data

        self.centerPlanets = []

    def safeDictGet(self, dict, key):
        if key in dict.keys():
            return dict[key]
        return None

    def createPlanet(self, planetData):
        planet = Planet(data=self.data, name=self.safeDictGet(planetData, "name"), size=self.safeDictGet(planetData, "size"), mass=self.safeDictGet(planetData, "mass"), speed=self.safeDictGet(planetData, "speed"), startAngle=self.safeDictGet(planetData, "startAngle"), distanceFromParent=self.safeDictGet(planetData, "distanceFromParent"))
        if 'center' in planetData.keys() and planetData['center']:
            self.centerPlanets.append(planet)
            if 'position' in planetData.keys():
                planet.position = (planetData['position'][0], planetData['position'][1])
            else:
                planet.position = (0, 0)
            # planet.isCenterPlanet = True
        if 'children' in planetData.keys():
            for childData in planetData['children']:
                planet.addChild(self.createPlanet(childData))
        return planet

    def loadPlanets(self):
        if not os.path.isfile('planets.json'):
            with open("planets.json", "w") as file:
                file.write(json.dumps(DataStash.planets_default, indent=4))

        with open('planets.json', 'r') as file:
            planetData = json.load(file)
            for centerPlanet in planetData['planets']:
                self.createPlanet(centerPlanet)

    def resetEverything(self):
        self.centerPlanets.clear()
        self.data.meteorManager.resetAllMeteors()
        self.loadPlanets()

    def __getAllPlanets(self, curPlanet):
        progress = []
        for childPlanet in curPlanet.children:
            progress.append(childPlanet)
            for childPlanetTwice in self.__getAllPlanets(childPlanet):
                progress.append(childPlanetTwice)

        return progress

    def getAllPlanets(self):
        progress = []

        for planet in self.centerPlanets:
            progress.append(planet)
            for childPlanet in self.__getAllPlanets(planet):
                progress.append(childPlanet)

        return progress


    def updatePhysics(self):
        for planet in self.centerPlanets:
            planet.updatePhysics()
        self.data.meteorManager.updatePhysics()

    def updateGraphics(self, painter):
        for planet in self.centerPlanets:
            planet.updateGraphics(painter)
        self.data.meteorManager.updateGraphics(painter)