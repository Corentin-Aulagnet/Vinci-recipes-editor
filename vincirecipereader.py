import xml.etree.ElementTree as ET
import copy

class Recipe():
    def __init__(self,path,_steps=[]):
        self.name= XMLReader.ReadRecipeName(path)
        self.path = path 
        self.steps=_steps
    
    @classmethod
    def from_foo(cls, class_instance):
        data = copy.deepcopy(class_instance) # if deepcopy is necessary
        return cls(data.path,data.steps)
    def AddSteps(self,steps):
        self.steps = steps
class Step():
    def __init__(self,_type='',_attr={}):
        self.type = _type
        self.attr = _attr
        
    @property
    def name(self):
        return self.type.split("CParamScript_")[1]
    @classmethod
    def from_foo(cls, class_instance):
        data = copy.deepcopy(class_instance) # if deepcopy is necessary
        return cls(data.type,data.attr)
    @classmethod
    def dummy(cls):
        return cls("CParamScript_")
    def Add_attr(self,key,value):
        self.attr[key]=value
    def clear(self):
        self.type=''
        self.attr = {}
class XMLReader:
    class ReadRecipeError(Exception):
        pass
    def __init__(self):
        pass
    @staticmethod
    def ReadRecipeName(xmlFile):
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        element = root.find("ScriptName")
        if(element != None):
            return element.text

    @staticmethod
    def ReadRecipe(xmlFile)->Recipe: 
        xsi='{http://www.w3.org/2001/XMLSchema-instance}'
        try:
            tree = ET.parse(xmlFile)
            root = tree.getroot()
            recipe = Recipe(xmlFile)
            steps = []
            for neighbor in root.iter('CollecStep'):
                if(xsi+'type' in neighbor.attrib.keys()):
                    #Is a real step
                    step = Step(neighbor.attrib[xsi+'type'],{})
                    for child in neighbor:
                        step.Add_attr(child.tag,child.text)
                    steps.append(step)
                elif 'subrecipe' in  neighbor.attrib.keys():
                    #Is a subrecipe
                    step = XMLReader.ReadRecipe(neighbor.attrib['subrecipe'])
                    steps.append(step)
            recipe.AddSteps(steps)
            return recipe
        except FileNotFoundError as e:
            raise XMLReader.ReadRecipeError()

    




