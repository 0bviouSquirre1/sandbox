from evennia import AttributeProperty, search_tag
from evennia.utils.utils import lazy_property
from typeclasses.objects import Object

class LiquidHandler:
    def __init__(self, container):
        self.container = container

    def transfer_from(self, amount, to_container=None):
        if not to_container:
            self.container.fill_level -= amount

            if self.container.fill_level <= 0:
                self.container.fill_level = 0
                self.container.liquid = None
            return

        self.container.fill_level -= amount
        to_container.fill_level += amount

        if to_container.liquid == None:
            to_container.liquid = self.container.liquid
        elif to_container.liquid != self.container.liquid:
            to_container.liquid = "mixture"

        if self.container.fill_level <= 0:
            self.container.fill_level = 0
            self.container.liquid = None

        if to_container.fill_level > to_container.capacity:
            to_container.fill_level = to_container.capacity

class LiquidContainer(Object):
    """
    Typeclass for containers that hold liquids.

    """
    capacity = AttributeProperty(10)
    fill_level = AttributeProperty(0)
    liquid = AttributeProperty(None)

    @lazy_property
    def liquids(self):
        return LiquidHandler(self)

    def at_object_creation(self):
        # Blank out the object's description, just to be tidy
        self.db.desc = ""

    def return_appearance(self, looker, **kwargs):
        """
        Appends the amount and type of liquid in the container to the container's description.
        
        """
        # Capture the original output of the command, we still want it
        string = super().return_appearance(looker, **kwargs)

        # Report based on the current fill_level
        if self.fill_level == 0:
            status = f"\n\nThe {self} contains no liquid."
        else:
            status = f"\n\nThe {self} has {str(self.fill_level)} sips of {self.liquid} remaining."

        # Append our results to the original output above
        return string + status

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        if self.liquid != None:
            moved_obj.tags.add("wet")