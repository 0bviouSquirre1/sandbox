from evennia.utils.test_resources import EvenniaCommandTest
from commands.interaction_commands import CmdPut
from evennia import create_object
from typeclasses.objects import Object

class TestCmdPut(EvenniaCommandTest):
    def test_put_no_input(self):
        # Arrange
        input = ""
        expected_output = "Usage: PUT <object> ON <surface>"

        # Act
        received_output = self.call(CmdPut(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_put_object(self):
        # Arrange
        self.obj1.location = self.char1
        input = f"{self.obj1}"
        expected_output = f"Where do you want to put the {self.obj1}?"

        # Act
        received_output = self.call(CmdPut(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_put_object_on_not_surface(self):
        # Arrange
        self.obj1.location = self.char1
        surface = create_object(Object, key="surface", location=self.room1)

        input = f"{self.obj1} on {surface}"
        expected_output = f"The {surface} is not a surface."

        # Act
        received_output = self.call(CmdPut(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_put_object_on_surface(self):
        # Arrange
        self.obj1.location = self.char1
        surface = create_object(Object, key="surface", location=self.room1)
        surface.tags.add("surface")

        input = f"{self.obj1} on {surface}"
        expected_output = f"You place the {self.obj1} on the {surface}."

        # Act
        received_output = self.call(CmdPut(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    