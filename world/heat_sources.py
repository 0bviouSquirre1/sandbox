from evennia import DefaultObject

class HeatSource(DefaultObject):
    """
    Typeclass for heat sources.
    """
    def at_object_creation(self):
        self.db.fuel = 100  # Initial fuel level (adjust as needed)
        self.db.is_hot = False  # Check if the heat source is hot

    def burn_fuel(self, amount):
        """
        Burn fuel from the heat source.
        """
        if self.db.fuel >= amount:
            self.db.fuel -= amount
            return True
        return False

    def heat_up(self):
        """
        Heat up the heat source.
        """
        self.db.is_hot = True

    def cool_down(self):
        """
        Cool down the heat source.
        """
        self.db.is_hot = False
