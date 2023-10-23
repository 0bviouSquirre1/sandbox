from evennia import TagProperty, AttributeProperty
from evennia.contrib.base_systems.components import ComponentHolderMixin
from typeclasses.objects import Object

class Ingredient(Object, ComponentHolderMixin):
    """
    Typeclass for tea ingredients.
    """
    
    power = AttributeProperty(default="default")
    potent = TagProperty()