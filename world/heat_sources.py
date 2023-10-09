from evennia import DefaultObject, AttributeProperty

class HeatSource(DefaultObject):
    """
    Typeclass for heat sources.
    """
    fuel = AttributeProperty(default=100) # Initial fuel level (adjust as needed)
    is_hot = AttributeProperty(default=False)

    def burn_fuel(self, amount):
        """
        Burn fuel from the heat source.
        """
        if self.fuel >= amount:
            self.fuel -= amount
            return True
        return False

    def heat_up(self):
        """
        Heat up the heat source.
        """
        self.is_hot = True

    def cool_down(self):
        """
        Cool down the heat source.
        """
        self.is_hot = False