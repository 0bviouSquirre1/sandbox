from evennia import AttributeProperty
from typeclasses.objects import Object
from world.containers import LiquidContainer

class HeatSource(Object):
    """
    Typeclass for heat sources.
    """
    fuel = AttributeProperty(default=100) # Initial fuel level (adjust as needed)

    def burn_fuel(self, amount):
        """
        Burn fuel from the heat source.
        """
        if self.fuel >= amount and self.tags.has("hot"):
            self.fuel -= amount
            return True
        return False

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        if not self.tags.has("hot"):
            self.tags.add("cold")
        
        # if not item.tags.has("heat-resistant"):
        #     item.tags.add("burnt")
        #     return False
        
        # if not isinstance(item, LiquidContainer):
        #     item.tags.add("hot")
        #     return False
        # else:
        #     return True