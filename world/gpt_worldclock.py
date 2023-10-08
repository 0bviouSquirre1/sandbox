from evennia import DefaultScript
from evennia.utils import gametime

# PLACEHOLDER SCRIPT developed by ChatGPT to hold ideas in place

class WorldClock(DefaultScript):
    """
    This script represents a world clock that advances time units when explicitly called.
    """

    def at_script_creation(self):
        """
        This is called when the script is first created.
        """
        self.key = "world_clock"
        self.desc = "A script for tracking the world clock."
        self.time_passed = 0

    def at_start(self):
        """
        This is called when the script is started.
        """
        self.time_passed = 0  # Initialize the time unit

    def advance(self, delta):
        """
        This is called when a command advances the clock.
        """
        self.time_passed += delta
        if self.time_passed % 24 == 0:
            # announce that a new day has dawned
            return
        else:
            # do nothing
            return
        
    def at_stop(self):
        """
        This is called when the script is stopped.
        """
        pass  # You can add cleanup logic here if needed
