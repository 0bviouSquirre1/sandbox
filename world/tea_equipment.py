from evennia import DefaultObject

class TeaEquipment(DefaultObject):
    """
    Typeclass for tea-making equipment.
    """
    def at_object_creation(self):
        self.db.equipment_type = "generic"  # Equipment type (e.g., "teapot", "teacup", etc.)

    def use(self, caller):
        """
        Method to handle using the equipment.
        """
        caller.msg(f"You use the {self.key}.")
