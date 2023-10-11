from evennia.utils.test_resources import EvenniaTest, EvenniaCommandTest
from evennia.utils import create
from world.containers import LiquidContainer
from world.tea_ingredient import TeaIngredient
from world.heat_sources import HeatSource
from commands.tea_commands import CmdBrew
from commands.tea_commands import CmdLight

class TestTea(EvenniaTest):
    def test_create_tea_ingredient(self):
        # Create a tea ingredient
        tea_ingredient = create.create_object(TeaIngredient, key="test_tea_ingredient")

        # Check for default values
        self.assertEqual(tea_ingredient.tea_type, "black")
        self.assertFalse(tea_ingredient.is_wet)

    def test_create_tea_equipment(self):
        # Create tea equipment
        tea_equipment = create.create_object(LiquidContainer, key="test_tea_equipment")

        # Check for default values
        self.assertTrue(tea_equipment)

class TestHeatSource(EvenniaTest):
    def test_create_heat_source(self):
        # Create a heat source
        heat_source = create.create_object(HeatSource, key="test_heat_source")

        # Check for default values
        self.assertEqual(heat_source.fuel, 100)
        self.assertFalse(heat_source.is_hot)

    def test_burn_fuel(self):
        # Create a heat source
        heat_source = create.create_object(HeatSource, key="test_heat_source")

        # Burn some fuel
        prefuel = heat_source.fuel
        heat_source.burn_fuel(10)

        # Check that the fuel was depleted correctly
        self.assertEqual(heat_source.fuel, prefuel-10)

        # Check that we can't burn too much fuel
        self.assertFalse(heat_source.burn_fuel(110))  # Not enough fuel

    def test_heat_up_cool_down(self):
        # Create a heat source
        heat_source = create.create_object(HeatSource, key="test_heat_source")

        # Heat it up
        heat_source.heat_up()
        self.assertTrue(heat_source.is_hot)

        # Cool it down
        heat_source.cool_down()
        self.assertFalse(heat_source.is_hot)

class TestBrewCommand(EvenniaCommandTest):
    def setUp(self):
        super().setUp()

        self.location = self.room1
        self.water = create.create_object(TeaIngredient, key="water")
        self.tea_leaves = create.create_object(TeaIngredient, key="tea leaves")
        self.kettle = create.create_object(LiquidContainer, key="kettle")
        self.heat_source = create.create_object(HeatSource, key="test_heat_source_location")

    def test_brew_command(self):
        # Create a caller
        caller = self.char1

        # Add ingredients to the equipment
        self.kettle.location = caller.location
        self.water.location = self.kettle
        self.tea_leaves.location = self.kettle

        # Light kettle
        self.heat_source.heat_up()

        # Call the command
        self.call(
            CmdBrew(),
            "",
            "You start heating the water in the kettle.|You wait for a moment as the water begins to boil.|You've successfully brewed a cup of tea."
        )

    def test_brew_no_leaves(self):
        pass
    def test_brew_no_water(self):
        pass
    def test_brew_no_fuel(self):
        pass
    def test_brew_not_lit(self):
        pass

class TestLightCommand(EvenniaCommandTest):
    pass