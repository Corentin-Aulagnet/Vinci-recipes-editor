import xml.etree.ElementTree as ET

class Recipe():
    def __init__(self,path):
        self.name= XMLReader.ReadRecipeName(path)
        self.path = path 
        self.steps=[]
    def AddSteps(self,steps):
        self.steps = steps
class Step():
    def __init__(self,_type):
        self.type = _type
        self.attr = {}
    def Add_attr(self,key,value):
        self.attr[key]=value
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
        xsi='{http://www.w3.org/2001/XMLSchema-instance}'
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        recipe = Recipe(xmlFile)
        steps = []
        for neighbor in root.iter('CollecStep'):
            step = Step(neighbor.attrib[xsi+'type'])
            for child in neighbor:
                step.Add_attr(child.tag,child.text)
            steps.append(step)
        recipe.AddSteps(steps)
        return recipe

    




