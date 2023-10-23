from evennia.commands.default.muxcommand import MuxCommand
from evennia import CmdSet

class CmdPut(MuxCommand):
    """
    Place an object on a surface.

    Usage:
        PUT <object> (ON/IN) <object>
    """

    key = "put"
    rhs_split = [" on ", " in "]
    help_category = "Interaction"

    def func(self):
        caller = self.caller
        self.item = self.lhs
        self.storage = self.rhs

        # Explain how to use the command when entered with no arguments
        if not self.args:
            caller.msg("Usage: PUT <object> (ON/IN) <object>")
            return

        # Find the thing we're putting down
        item = caller.search(self.item, location=caller)
        if not item:
            return

        # caller.search returns a list
        # find it and take the first entry
        storage = caller.search(self.storage, quiet=True)
        if not storage:
            caller.msg(f"Where do you want to put the {item}?")
            return
        storage = storage[0]

        success = item.move_to(storage)

        # Report on how it went
        string = ""
        if success:
            string = f"You place the {item} on the {storage}."
        else:
            string = "Something went wrong."
        caller.msg(string)

class CmdGet(MuxCommand):
    """
    Retrieve an object from another object.

    Usage:
        GET <object> (FROM <object>)
    """

    key = "get"
    rhs_split = [" from "]
    help_category = "Interaction"

    def func(self):
        caller = self.caller
        self.item = self.lhs
        self.storage = self.rhs

        if not self.args:
            caller.msg("Usage: GET <object> (FROM <object>)")
            return
        
        string = ""
        if not self.storage:
            item = caller.search(self.item, location=caller.location)
            if not item:
                return
            string = f"You pick up the {item}."
        else:
            storage = caller.search(self.storage, quiet=True)
            storage = storage[0]
            item = caller.search(self.item, location=storage)
            if not item:
                return
            string = f"You retrieve the {item} from the {storage}."
        
        if not item.at_pre_get(caller):
            return

        success = item.move_to(caller, quiet=True, move_type="get")

        # Report on how it went
        if not success:
            string = "Something went wrong."
            return
        
        caller.msg(string)

class InteractionCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdPut)
        self.add(CmdGet)