from evennia import Command, GLOBAL_SCRIPTS
from evennia.utils import create, search

class CmdBrew(Command):
    """
    Brew a cup of tea.
    """
    key = "brew"

    def func(self):
        caller = self.caller
        location = caller.location  # Get the location of the caller

        # Check if the caller has a kettle/teapot and a heat source in the same location
        heat_source = search.search_typeclass(typeclass="world.heat_sources.HeatSource")[0]
        kettle = caller.search("kettle", location=location, typeclass="world.tea_equipment.TeaEquipment")

        if not (kettle and heat_source):
            caller.msg("You need a kettle and a heat source in the same location to brew tea.")
            return

        # Check if the heat source is hot and has enough fuel
        if not (heat_source.is_hot and heat_source.fuel > 0):
            caller.msg(f"The {heat_source.key} in this location is not hot or has run out of fuel.")
            return

        # Check if the kettle contains water and tea leaves
        water = kettle.search("water") if kettle else None
        tea_leaves = kettle.search("tea leaves") if kettle else None

        if not (water and tea_leaves):
            caller.msg(f"The {kettle.key} needs water and tea leaves to brew tea.")
            return

        # advance time
        delta = 3
        clock = GLOBAL_SCRIPTS.world_clock
        if clock:
            clock.advance(delta)
        else:
            caller.msg("Where is the clock")

        # wet the leaves
        tea_leaves.is_wet = True

        # Burn fuel from the heat source (adjust the fuel consumption)
        if heat_source.burn_fuel(10):  # Adjust the fuel consumption as needed
            caller.msg(f"You start heating the water in the {kettle.key}.")

            # Simulate boiling time (e.g., 5 seconds)
            caller.msg("You wait for a moment as the water begins to boil.")

            # Notify the player of successful tea brewing
            caller.msg("You've successfully brewed a cup of tea.")

            # Remove water and replace with tea
            water.delete()

            # Optionally, create a new Tea object for the brewed tea
            brewed_tea = create.create_object(key=f"{tea_leaves.tea_type} tea", location=kettle)
            brewed_tea.tea_type = tea_leaves.tea_type  # Customize the tea type

        else:
            caller.msg("The heat source doesn't have enough fuel to continue heating.")

class CmdLight(Command):
    """
    Light the heat source.
    Usage:
      light
    This command lights the heat source, making it hot.
    """

    key = "light"
    aliases = ["ignite"]
    help_category = "General"

    def func(self):
        caller = self.caller

        # Check if the caller has a heat source in the current location
        heat_sources = search.search_typeclass(typeclass="world.heat_sources.HeatSource")
        for source in heat_sources:
            if source.location == caller.location:
                heat_source = source

        if not heat_source:
            caller.msg("There is no heat source in this location to light.")
            return

        # Check if the heat source is already hot
        if heat_source.db.is_hot:
            caller.msg("The heat source is already lit.")
            return

        # Light the heat source by changing the is_hot property
        heat_source.db.is_hot = True
        caller.msg("You successfully light the heat source.")