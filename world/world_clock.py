from evennia import DefaultScript, AttributeProperty

class WorldClock(DefaultScript):
    """
    This script represents a world clock that advances time units when explicitly called.
    """
    time_passed = AttributeProperty(0) # Time units since game start

    def at_script_creation(self):
        """
        This is called when the script is first created.
        """
        self.key = "world_clock"
        self.desc = "A script for tracking the world clock."

    def advance(self, delta):
        """
        This is called when a command advances the clock.
        """
        self.time_passed += delta
        if self.time_passed % 288 == 0: # time units of 5 min in 24 hrs = 288 units
            # announce that a new day has dawned
            return
        else:
            # do nothing
            return