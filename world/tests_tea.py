from evennia.utils.test_resources import EvenniaTest, EvenniaCommandTest
from evennia.utils import create
from world.containers import LiquidContainer
from world.tea_ingredient import TeaIngredient
from world.heat_sources import HeatSource

class TestHeatSource(EvenniaTest):
    def setUp(self):
        super.setUp()
        self.heat_source = create.create_object(HeatSource, key="heat_source")

    def test_create_heat_source(self):
        # Arrange
        heat_source = self.heat_source

        # Act
        
        # Assert
        self.assertEqual(heat_source.fuel, 100)
        self.assertFalse(heat_source.tags.has("hot"))

    def test_burn_fuel(self):
        # Arrange
        heat_source = self.heat_source

        # Act
        prefuel = heat_source.fuel
        heat_source.burn_fuel(10)

        # Assert
        self.assertEqual(heat_source.fuel, prefuel-10)
        self.assertFalse(heat_source.burn_fuel(110))  # Not enough fuel