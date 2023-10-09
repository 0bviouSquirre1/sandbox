from evennia import DefaultObject, AttributeProperty

class TeaIngredient(DefaultObject):
    """
    Typeclass for tea ingredients.
    """
    tea_type = AttributeProperty(default="black")
    is_wet = AttributeProperty(default=False)