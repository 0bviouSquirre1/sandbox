from evennia import AttributeProperty, TagProperty
from typeclasses.objects import Object
from world.containers import LiquidContainer

class HeatSource(Object):
    """
    Typeclass for heat sources.
    """
    fuel = AttributeProperty(default=100) # Initial fuel level (adjust as needed)
    surface = TagProperty()

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
            return
        
        if not moved_obj.tags.has("heat-resistant"):
            moved_obj.tags.add("burnt")
            return
        
        if not isinstance(moved_obj, LiquidContainer):
            moved_obj.tags.add("hot")
            return
        
        if moved_obj.fill_level == 0:
            moved_obj.tags.add("hot")
            return
        
        if moved_obj.liquid != "water":
            moved_obj.tags.add("hot")
            moved_obj.liquid = f"hot {moved_obj.liquid}"
            return
        
        if moved_obj.contents == []:
            moved_obj.tags.add("hot")
            moved_obj.liquid = f"boiled {moved_obj.liquid}"
            return
        
        for obj in moved_obj.contents:
            if not obj.tags.has("potent"):
                moved_obj.tags.add("hot")
                obj.tags.add("hot")
                obj.tags.add("wet")
                moved_obj.liquid = f"boiled {moved_obj.liquid}"
            else:
                moved_obj.tags.add("hot")
                obj.tags.add("hot")
                obj.tags.add("wet")
                moved_obj.liquid = f"{obj} decoction"