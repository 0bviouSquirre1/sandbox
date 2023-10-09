from evennia.utils.test_resources import EvenniaTest
from evennia.utils import create
from world.tea_ingredient import TeaIngredient
from world.tea_equipment import TeaEquipment
from world.heat_sources import HeatSource
from commands.tea_commands import CmdBrew
from commands.tea_commands import CmdLight


class TestTea(EvenniaTest):
    def test_create_tea_ingredient(self):
        # Create a tea ingredient
        tea_ingredient = create.create_object(TeaIngredient, key="test_tea_ingredient")
        self.assertEqual(tea_ingredient.key, "test_tea_ingredient")

    def test_create_tea_equipment(self):
        # Create tea equipment
        tea_equipment = create.create_object(TeaEquipment, key="test_tea_equipment")
        self.assertEqual(tea_equipment.key, "test_tea_equipment")

    def test_create_heat_source(self):
        # Create a heat source
        heat_source = create.create_object(HeatSource, key="test_heat_source")
        self.assertEqual(heat_source.key, "test_heat_source")

    def test_burn_fuel(self):
        heat_source = create.create_object(HeatSource, key="test_heat_source")
        self.assertTrue(heat_source.burn_fuel(10))  # Burn fuel successfully
        self.assertFalse(heat_source.burn_fuel(110))  # Not enough fuel

    def test_heat_up_cool_down(self):
        heat_source = create.create_object(HeatSource, key="test_heat_source")
        heat_source.heat_up()
        self.assertTrue(heat_source.db.is_hot)
        heat_source.cool_down()
        self.assertFalse(heat_source.db.is_hot)

    def test_brew_command(self):
        # Create a mock caller (you may need to customize this)
        caller = create.create_object(TeaEquipment, key="caller")
        caller.location = create.create_object(HeatSource, key="test_heat_source_location")

        # Create tea ingredients and equipment
        water = create.create_object(TeaIngredient, key="water")
        tea_leaves = create.create_object(TeaIngredient, key="tea leaves")
        kettle_teapot = create.create_object(TeaEquipment, key="kettle_teapot")

        # Add ingredients to the equipment
        kettle_teapot.location = caller.location
        water.location = kettle_teapot
        tea_leaves.location = kettle_teapot

class TestLightHeatSource(EvenniaTest):
    def test_light_heat_source_success(self):
        # Create a mock caller
        caller = create.create_object(HeatSource, key="caller")

        # Create a heat source in the same location
        heat_source = create.create_object(HeatSource, key="heat source", location=caller)

        # Assert that the heat source is hot
        self.assertFalse(heat_source.db.is_hot)

    def test_light_heat_source_already_lit(self):
        # Create a mock caller
        caller = create.create_object(HeatSource, key="caller")

        # Create a heat source in the same location and make it hot
        heat_source = create.create_object(HeatSource, key="heat source", location=caller)
        heat_source.db.is_hot = True

        # Assert that the heat source is still hot
        self.assertTrue(heat_source.db.is_hot)