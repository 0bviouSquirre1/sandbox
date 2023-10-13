from evennia.utils.test_resources import EvenniaTest
from evennia import create_object
from world.ingredients import Ingredient

class TestIngredients(EvenniaTest):
    def test_ingredients(self):
        # Arrange
        leaf = create_object(Ingredient, key="leaf")

        # Act

        # Assert
        self.assertTrue(leaf.tags.has("potent"))
        self.assertTrue(leaf.power, "default")