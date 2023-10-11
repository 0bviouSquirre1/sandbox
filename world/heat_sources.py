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
        if self.fuel >= amount:
            self.fuel -= amount
            return True
        return False

    def at_object_receive(self, item, source_location):
        if not self.tags.has("hot"):
            return
        
        if not item.tags.has("heat-resistant"):
            for obj in item.contents:
                obj.home = self
            item.delete()
            return
        
        if not isinstance(item, LiquidContainer) or item.fill_level == 0 or not item.liquid == "water":
            # item is heat-resistant but not a liquid container
            # or has no liquid in it
            # or has something other than water in it
            item.tags.add("hot")
            return
        
        for obj in item.contents:
            if obj.tags.has("potent"):
                leaf = obj
                return
            
        # make decoction
        if leaf:
            item.liquid == f"{leaf} decoction"
            return
        else:
            # boil water
            return