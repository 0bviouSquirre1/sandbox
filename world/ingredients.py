from evennia import TagProperty
from typeclasses.objects import Object

class Ingredient(Object):
    """
    Typeclass for tea ingredients.
    """
    
    potent = TagProperty()