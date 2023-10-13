from evennia.utils.test_resources import EvenniaCommandTest
from commands.interaction_commands import CmdPut

class TestCmdPut(EvenniaCommandTest):
    def test_put_no_input(self):
        # Arrange
        expected_output = ""

        # Act
        received_output = self.call(CmdPut)

        # Assert
        self.assertEqual(received_output, expected_output)