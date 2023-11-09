from evennia import TagProperty, AttributeProperty
from typeclasses.objects import Object

class Ingredient(Object):
    """
    Typeclass for tea ingredients.
    """
    
    power = AttributeProperty(default="default")
    potent = TagProperty()