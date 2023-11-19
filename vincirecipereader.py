import xml.etree.ElementTree as ET

class Recipe():
    def __init__(self,path):
        self.name= XMLReader.ReadRecipeName(path)
        self.path = path 
        self.steps=[]
    def AddSteps(self,steps):
        self.steps = steps

class XMLReader:
    def __init__(self):
        pass
    @staticmethod
    def ReadRecipeName(xmlFile):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        return root.find("ScriptName").text

    @staticmethod
    def ReadRecipe(xmlFile):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        recipe = Recipe(xmlFile)
        steps = []
        for neighbor in root.iter('CollecStep'):
            dic=neighbor.attrib
            for child in neighbor:
                dic[child.tag]=child.text
            steps.append(dic)
        recipe.AddSteps(steps)
        return recipe

    




