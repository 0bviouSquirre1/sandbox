from evennia.utils.test_resources import EvenniaTest
from evennia.utils import create
from world.containers import LiquidContainer

class TestLiquidContainer(EvenniaTest):
    def setUp(self):
        super().setUp()

        self.container1 = create.create_object(LiquidContainer, key="container 1")
        self.container2 = create.create_object(LiquidContainer, key="container 2")
        self.container2.liquid = "water"
        self.container2.fill_level = 10

    def test_container_defaults(self):
        # Arrange

        # Act

        # Assert
        self.assertEqual(self.container1.capacity, 10)
        self.assertEqual(self.container1.fill_level, 0)
        self.assertEqual(self.container1.liquid, None)
    
    def test_transfer_less_than_full(self):
        # Arrange

        # Act
        self.container2.liquids.transfer_from(5, self.container1)

        # Assert
        self.assertEqual(self.container1.fill_level, 5)
        self.assertEqual(self.container1.liquid, "water")
        self.assertEqual(self.container2.fill_level, 5)
        self.assertEqual(self.container2.liquid, "water")

    def test_transfer_more_than_full(self):
        # Arrange

        # Act
        self.container2.liquids.transfer_from(15, self.container1)

        # Assert
        self.assertEqual(self.container1.fill_level, 10)
        self.assertEqual(self.container1.liquid, "water")
        self.assertEqual(self.container2.fill_level, 0)
        self.assertEqual(self.container2.liquid, None)

    def test_transfer_no_receiver(self):
        # Arrange

        # Act
        self.container2.liquids.transfer_from(10)

        # Assert
        self.assertEqual(self.container2.fill_level, 0)
        self.assertEqual(self.container2.liquid, None)

    def test_transfer_multiple_liquids(self):
        # Arrange
        self.container1.liquid = "tea"
        self.container1.fill_level = 3

        # Act
        self.container2.liquids.transfer_from(4, self.container1)

        # Assert
        self.assertEqual(self.container1.fill_level, 7)
        self.assertEqual(self.container1.liquid, "mixture")
        self.assertEqual(self.container2.fill_level, 6)
        self.assertEqual(self.container2.liquid, "water")