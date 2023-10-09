from evennia import Command

class CmdAdvance(Command):
    """
    Advance the world clock by a specified number of units.

    Usage:
      advance <units>

    Example:
      advance 10
    """

    key = "advance"
    help_category = "Time"

    def func(self):
        """
        Execute the command.
        """
        caller = self.caller

        # Check if the argument is a valid positive integer
        try:
            units = int(self.units)
            if units <= 0:
                caller.msg("You must specify a positive number of units.")
                return
        except ValueError:
            caller.msg("Invalid input. You must specify a positive number of units.")
            return

        # Trigger the world clock script to advance
        world_clock = caller.scripts.get("world_clock")
        if world_clock:
            world_clock.at_advance(caller, str(units))
            caller.msg(f"You advanced the world clock by {units} units.")
        else:
            caller.msg("The world clock script is not available here.")

# Add the command to the Time CommandSet
from evennia import create_command
create_command(CmdAdvance, key="advance", cmdset="Time")