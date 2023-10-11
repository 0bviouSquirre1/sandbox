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

    def boil(self, container):
    # Put Container On Heat-Source
        if self.is_hot == True and container.tag == "heat_resistant":
            if container.fill_level != 0 and container.liquid == "water":
                # pass time (... don't remove container)
                # tag container with warm, then hot, then scalding
                if container has item labeled potent
                # create decoction (boil)
                    container.liquid = f"{leaf} decoction"
                    # add 1 expiration to the boilable matter
                else:
                    container.liquid = None
                    # set any objects in the container to dry (tag)
            else:
                container.liquid = container.liquid
                # set any objects in the container to dry (tag)