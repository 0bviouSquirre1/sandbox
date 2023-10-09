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
        kettle_teapot = caller.search("kettle", location=location, typeclass="world.tea_equipment.TeaEquipment")

        if not (kettle_teapot and heat_source):
            caller.msg("You need a kettle/teapot and a heat source in the same location to brew tea.")
            return

        # Check if the heat source is hot and has enough fuel
        if not (heat_source.db.is_hot and heat_source.db.fuel > 0):
            caller.msg("The heat source in this location is not hot or has run out of fuel.")
            return

        # Check if the kettle/teapot contains water and tea leaves
        water = kettle_teapot.search("water") if kettle_teapot else None
        tea_leaves = kettle_teapot.search("tea leaves") if kettle_teapot else None

        if not (water and tea_leaves):
            caller.msg("The kettle/teapot needs water and tea leaves to brew tea.")
            return

        # advance time
        delta = 3
        clock = GLOBAL_SCRIPTS.world_clock
        if clock:
            clock.advance(delta)
        else:
            caller.msg("Where is the clock")

        # Burn fuel from the heat source (adjust the fuel consumption)
        if heat_source.burn_fuel(10):  # Adjust the fuel consumption as needed
            caller.msg("You start heating the water in the kettle/teapot.")

            # Simulate boiling time (e.g., 5 seconds)
            caller.msg("You wait for a moment as the water begins to boil.")

            # Optionally, add sweeteners or flavorings
            caller.msg("You can add sweeteners or flavorings if desired.")

            # Notify the player of successful tea brewing
            caller.msg("You've successfully brewed a cup of tea.")

            # Remove water and replace with tea
            water.delete()

            # Optionally, create a new TeaIngredient object for the brewed tea
            brewed_tea = create.create_object(key="brewed tea", location=kettle_teapot)
            brewed_tea.tea_type = "custom"  # Customize the tea type
            caller.execute_cmd("look kettle") # Display a description of the kettle/teapot

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
