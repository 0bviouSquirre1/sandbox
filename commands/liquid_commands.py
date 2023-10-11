from evennia.commands.default.muxcommand import MuxCommand
from evennia import CmdSet
from world.containers import LiquidContainer

liquid_string = "world.containers.LiquidContainer"

class CmdFill(MuxCommand):
    """
    Fill a container from another container.

    Usage:
        FILL <container> FROM <another container>
    """

    key = "fill"
    rhs_split = [" from "]
    help_category = "Interaction"

    def func(self):
        caller = self.caller
        self.to_container = self.lhs
        self.from_container = self.rhs

        # Explain how to use the command when entered with no arguments
        if not self.args:
            caller.msg("Usage: FILL <container> FROM <another container>")
            return

        # Find the receiving container in the user's inventory
        to_container = caller.search(self.to_container)
        if not to_container:
            # No message needed, standard error appears here
            return
        
        # Make sure the thing you're filling can hold liquid
        if not isinstance(to_container, LiquidContainer):
            self.caller.msg("You can't fill that!")
            return

        # Find the giving container
        from_container = caller.search(self.from_container, quiet=True)
        if not from_container:
            caller.msg(f"Where do you want to fill the {to_container} from?")
            return
        from_container = from_container[0]

        # Make sure the container can provide liquids
        if not isinstance(from_container, LiquidContainer):
            caller.msg(f"The {from_container} does not hold liquids.")
            return
        
        # Make sure it's not empty
        if from_container.fill_level <= 0:
            caller.msg(f"The {from_container} is empty!")
            return

        # The number moved between containers should be the same
        transfer_amount = to_container.capacity - to_container.fill_level
        liquid = from_container.liquid

        leave = from_container.transfer(-transfer_amount, liquid)
        arrive = to_container.transfer(transfer_amount, liquid)

        string = ""
        if leave and arrive:
            if from_container.fill_level == 0:
                string += f"You empty the {from_container} into the {to_container}."
            else:
                string += f"You fill the {to_container} from the {from_container}."
        else:
            "Something went wrong."
        caller.msg(string)

class CmdEmpty(MuxCommand):
    """
    Empty a container, possibly into another container.
    If no other container is specified, the fill_level will
    be dumped on the ground.

    Usage:
        EMPTY <container> (INTO <another container>)
    """

    key = "empty"
    aliases = "pour"
    help_category = "Interaction"
    rhs_split = [" into "]

    def func(self):
        caller = self.caller
        self.to_container = self.rhs
        self.from_container = self.lhs

        if not self.args:
            caller.msg("Usage: EMPTY <container> (INTO <another container>)")
            return

        from_container = caller.search(self.from_container, location=caller, quiet=True)
        if not from_container:
            caller.msg(f"You aren't holding a {self.from_container}.")
            return
        from_container = from_container[0]
        
        if not isinstance(from_container, LiquidContainer):
            caller.msg("You can't empty that!")
            return

        transfer_amount = from_container.fill_level
        if transfer_amount == 0:
            caller.msg(f"The {from_container} is already empty!")
            return

        liquid = from_container.liquid
        from_container.transfer(-transfer_amount, liquid)

        to_container = caller.search(self.to_container, quiet=True)

        string = ""
        if len(to_container) == 1:
            to_container = to_container[0]
            if not isinstance(to_container, LiquidContainer):
                caller.msg(f"You cannot pour {liquid} into the {to_container}.")
                return
            
            empty = to_container.capacity - to_container.fill_level
            to_container.transfer(transfer_amount, liquid)

            if transfer_amount <= empty:
                string += f"You empty the {from_container} into the {to_container}."
            string += f"\nThe rest of the {liquid} splashes all over the ground."
        else:
            string += f"You empty the {from_container} out on the ground."

        caller.msg(string)

class CmdPut(MuxCommand):
    pass

# class CmdBoil(MuxCommand):
#     """
#     Put the kettle on to boil.
# 
#     Usage:
#         BOIL <container>
#     """
# 
#     key = "boil"
#     help_category = "Interaction"
# 
#     def func(self):
#         caller = self.caller
# 
#         if not self.args:
#             caller.msg("What do you want to boil?")
#             return
# 
#         container = self.caller.search(self.args)
#         if not container:
#             return
#         if not isinstance(container, BoilContainer):
#             caller.msg("You can't boil that!")
#             return
# 
#         caller.location.msg_contents(
#             container.boil(container),
#             from_obj=caller,
#             mapping={"boiler": container})


class LiquidCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdFill)
        self.add(CmdEmpty)
#       self.add(CmdBoil)