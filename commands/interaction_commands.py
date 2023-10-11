from evennia.commands.default.muxcommand import MuxCommand
from evennia import CmdSet

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
        self.item = self.lhs
        self.surface = self.rhs

        # Explain how to use the command when entered with no arguments
        if not self.args:
            caller.msg("Usage: PUT <object> ON <surface>")
            return

        # Find the thing we're putting down
        item = caller.search(self.item, location=caller)
        if not item:
            return

        # Find the surface
        surface = caller.search(self.surface, quiet=True)
        if not surface:
            caller.msg(f"Where do you want to put the {item}?")
            return
        surface = surface[0]

        # Make sure the thing is a surface
        if not surface.tags.has("surface"):
            caller.msg(f"The {surface} is not a surface.")
            return

        # Move the object to the surface's inventory here
        success = item.move_to(surface)

        # Report on how it went
        string = ""
        if success:
            string = f"You place the {item} on the {surface}"
        else:
            string = "Something went wrong."
        caller.msg(string)

class InteractionCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdPut)