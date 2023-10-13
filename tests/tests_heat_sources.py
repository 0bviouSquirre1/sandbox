from evennia.utils.test_resources import EvenniaTest
from evennia.utils import create
from world.heat_sources import HeatSource
from world.containers import LiquidContainer
from sandbox.world.ingredients import Ingredient

class TestHeatSource(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.heat_source = create.create_object(HeatSource, key="heat_source")
        self.container = create.create_object(LiquidContainer, key="container")
        self.ingredient = create.create_object(Ingredient, key="ingredient")

        self.container.tags.add("heat-resistant")
        self.ingredient.tags.add("potent")

    def test_create_heat_source(self):
        # Arrange
        heat_source = self.heat_source

        # Act
        
        # Assert default fuel amount and that heat_source is cold
        self.assertEqual(heat_source.fuel, 100)
        self.assertFalse(heat_source.tags.has("hot"))

    def test_burn_fuel(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")

        # Act
        result = heat_source.burn_fuel(10)

        # Assert
        self.assertEqual(heat_source.fuel, 90)
        self.assertFalse(heat_source.burn_fuel(110))  # Not enough fuel
        self.assertTrue(result)
    
    def test_at_object_receive_is_cold(self):
        # Arrange
        heat_source = self.heat_source

        # Act
        self.obj1.move_to(heat_source)

        # Assert
        self.assertFalse(heat_source.tags.has("hot"))

    def test_at_object_receive_not_heat_resistant(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")

        # Act
        self.obj1.move_to(heat_source)

        # Assert
        self.assertTrue(self.obj1.tags.has("burnt"))

    def test_at_object_receive_not_liquid_container(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")
        self.obj1.tags.add("heat-resistant")

        # Act
        self.obj1.move_to(heat_source)

        # Assert
        self.assertTrue(self.obj1.tags.has("hot"))

    def test_at_object_receive_empty(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")

        # Act
        self.container.move_to(heat_source)

        # Assert
        self.assertEqual(self.container.fill_level, 0)
        self.assertTrue(self.container.tags.has("hot"))

    def test_at_object_receive_not_water(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")
        container = self.container
        container.liquid = "tea"
        container.fill_level = 10

        # Act
        container.move_to(heat_source)

        # Assert
        self.assertTrue(container.tags.has("hot"))
        self.assertEqual(container.liquid, f"hot {container.liquid}")

    def test_at_object_receive_water_no_stuff(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")
        container = self.container
        container.liquid = "water"
        container.fill_level = 10

        # Act
        container.move_to(heat_source)

        # Assert
        self.assertEqual(container.liquid, f"boiled {container.liquid}")
        self.assertTrue(container.tags.has("hot"))

    def test_at_object_receive_water_with_nontea_stuff(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")
        container = self.container
        container.liquid = "water"
        container.fill_level = 10
        self.obj1.location = container

        # Act
        container.move_to(heat_source)

        # Assert
        self.assertEqual(container.liquid, "boiled water")
        self.assertTrue(container.tags.has("hot"))
        self.assertTrue(self.obj1.tags.has("hot"))
        self.assertTrue(self.obj1.tags.has("wet"))

    def test_at_object_receive_water_with_nontea_stuff(self):
        # Arrange
        heat_source = self.heat_source
        heat_source.tags.add("hot")
        container = self.container
        container.liquid = "water"
        container.fill_level = 10
        self.ingredient.location = container

        # Act
        container.move_to(heat_source)

        # Assert
        self.assertEqual(container.liquid, f"{self.ingredient} decoction")
        self.assertTrue(container.tags.has("hot"))
        self.assertTrue(self.ingredient.tags.has("hot"))
        self.assertTrue(self.ingredient.tags.has("wet"))