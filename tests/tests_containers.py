from evennia.utils.test_resources import EvenniaTest
from evennia.utils import create
from world.containers import LiquidContainer

class TestLiquidContainer(EvenniaTest):
    def setUp(self):
        super().setUp()


    def test_container_defaults(self):
        # Arrange
        container = create.create_object(LiquidContainer, key="container")

        # Act

        # Assert
        self.assertEqual(container.capacity, 10)
        self.assertEqual(container.fill_level, 0)
        self.assertEqual(container.liquid, None)
    
    def test_transfer_no_overflow(self):
        # Arrange
        container1 = create.create_object(LiquidContainer, key="container 1")
        container2 = create.create_object(LiquidContainer, key="container 2")
        container1.fill_level = 2
        container2.fill_level = 4

        # Act
        container1.transfer(-2, None)
        container2.transfer(2, None)

        # Assert
        self.assertEqual(container1.fill_level, 0)
        self.assertEqual(container2.fill_level, 6)

    def test_transfer_w_overflow(self):
        # Arrange
        container1 = create.create_object(LiquidContainer, key="container 1")
        container2 = create.create_object(LiquidContainer, key="container 2")
        container1.fill_level = 7
        container2.fill_level = 4

        # Act
        container1.transfer(-7, None)
        container2.transfer(7, None)

        # Assert
        self.assertEqual(container1.fill_level, 0)
        self.assertEqual(container2.fill_level, 10)