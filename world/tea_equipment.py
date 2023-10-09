from evennia import DefaultObject, AttributeProperty

class TeaEquipment(DefaultObject):
    """
    Typeclass for tea-making equipment.
    """
    equipment_type = AttributeProperty(default="generic")

    def use(self, caller):
        """
        Method to handle using the equipment.
        """
        caller.msg(f"You use the {self.key}.")
