from evennia.utils.test_resources import EvenniaTest

class TestSkills(EvenniaTest):
    def test_char_has_skills(self):
        # Arrange

        # Act

        # Assert
        self.assertEqual(self.char1.gardening, 0)
        self.assertEqual(self.char1.divining, 0)
        self.assertEqual(self.char1.housekeeping, 0)

    def test_increase_gardening(self):
        # Arrange

        # Act
        self.char1.garden_increase(2)

        # Assert
        self.assertEqual(self.char1.gardening, 2)

    def test_increase_divining(self):
        # Arrange

        # Act
        self.char1.divining_increase(2)

        # Assert
        self.assertEqual(self.char1.divining, 2)

    def test_increase_housekeeping(self):
        # Arrange

        # Act
        self.char1.housekeep_increase(2)

        # Assert
        self.assertEqual(self.char1.housekeeping, 2)