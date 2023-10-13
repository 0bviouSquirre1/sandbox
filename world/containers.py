from evennia import AttributeProperty, search_tag
from typeclasses.objects import Object

class LiquidContainer(Object):
    """
    Typeclass for containers that hold liquids.

    """
    capacity = AttributeProperty(10)
    fill_level = AttributeProperty(0)
    liquid = AttributeProperty(None)

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

    def transfer(self, amount, liquid):
        """
        Updates the amount of liquid in the container.
        
        """
        # Add the new liquid to the container's liquid
        self.fill_level += amount

        # If you go over the amount the container can hold, fill to the brim
        if self.fill_level > self.capacity:
            self.fill_level = self.capacity

        # If removal results in a negative number, empty the container and remove the liquid
        if self.fill_level <= 0:
            self.fill_level = 0
            self.liquid = None
            self.tags.remove("potent")
        else:
            # If both containers have the same liquid, no problem
            if self.liquid == liquid:
                return
            # If not, it creates a useless mixture of liquids
            else:
                self.liquid == "mixture"