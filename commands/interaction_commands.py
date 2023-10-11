from evennia.commands.default.muxcommand import MuxCommand
from evennia import CmdSet
from world.containers import LiquidContainer

class CmdPut(MuxCommand):
    """
    Place an object on a surface.

    Usage:
        PUT <object> ON <surface>
    """

    key = "put"
    rhs_split = [" on "]
    help_category = "Interaction"

    def func(self):
        caller = self.caller
        self.object = self.lhs
        self.surface = self.rhs

        # Explain how to use the command when entered with no arguments
        if not self.args:
            caller.msg("Usage: PUT <object> ON <surface>")
            return

        # Find the thing we're putting down
        object = caller.search(caller)
        if not object:
            # No message needed, standard error appears here
            return

        # Find the surface
        surface = caller.search(self.surface, quiet=True)
        if not surface:
            caller.msg(f"Where do you want to put the {object}?")
            return
        surface = surface[0]

        # Make sure the thing is a surface
        if not isinstance(surface, LiquidContainer): # tag check here
            caller.msg(f"The {surface} is not a surface.")
            return

        # Move the object to the surface's inventory here

        string = ""
        if leave and arrive:
            if surface.fill_level == 0:
                string += f"You empty the {surface} into the {surface}."
            else:
                string += f"You fill the {surface} from the {surface}."
        else:
            "Something went wrong."
        caller.msg(string)

class InteractionCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdPut)