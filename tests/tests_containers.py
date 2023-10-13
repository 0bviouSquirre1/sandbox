from evennia.utils.test_resources import EvenniaTest
from evennia.utils import create
from world.containers import LiquidContainer

class TestLiquidContainer(EvenniaTest):
    def setUp(self):
        super().setUp()

        self.container1 = create.create_object(LiquidContainer, key="container 1")
        self.container2 = create.create_object(LiquidContainer, key="container 2")

    def test_container_defaults(self):
        # Arrange

        # Act

        # Assert
        self.assertEqual(self.container1.capacity, 10)
        self.assertEqual(self.container1.fill_level, 0)
        self.assertEqual(self.container1.liquid, None)
    
    def test_transfer_no_overflow(self):
        # Arrange
        self.container1.fill_level = 2
        self.container2.fill_level = 4

        # Act
        self.container1.transfer(-2, None)
        self.container2.transfer(2, None)

        # Assert
        self.assertEqual(self.container1.fill_level, 0)
        self.assertEqual(self.container2.fill_level, 6)

    def test_transfer_w_overflow(self):
        # Arrange
        self.container1.fill_level = 7
        self.container2.fill_level = 4

        # Act
        self.container1.transfer(-7, None)
        self.container2.transfer(7, None)

        # Assert
        self.assertEqual(self.container1.fill_level, 0)
        self.assertEqual(self.container2.fill_level, 10)

    def test_transfer_remove_potent(self):
        # Arrange
        self.container1.fill_level = 2
        self.container2.fill_level = 4
        self.container1.tags.add("potent")

        # Act
        self.container1.transfer(-2, None)
        self.container2.transfer(2, None)

        # Assert
        self.assertEqual(self.container1.fill_level, 0)
        self.assertFalse(self.container1.tags.has("potent"))