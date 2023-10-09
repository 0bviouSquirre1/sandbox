from evennia import DefaultObject

class TeaIngredient(DefaultObject):
    """
    Typeclass for tea ingredients.
    """
    def at_object_creation(self):
        self.db.tea_type = "generic"  # Tea type (e.g., "green", "black", "water", etc.)
        self.db.is_wet = False