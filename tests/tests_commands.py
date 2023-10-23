from evennia.utils.test_resources import EvenniaCommandTest
from commands.interaction_commands import CmdPut, CmdGet
from commands.liquid_commands import CmdFill, CmdEmpty
from evennia import create_object
from typeclasses.objects import Object
from world.containers import LiquidContainer

class TestCmdPut(EvenniaCommandTest):
    def test_put_no_args(self):
        # Arrange
        input = ""
        expected_output = "Usage: PUT <object> (ON/IN) <object>"

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

class TestCmdFill(EvenniaCommandTest):
    def test_fill_no_args(self):
        # Arrange
        input = ""
        expected_output = "Usage: FILL <container> FROM <another container>"

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_fill_unfillable_object(self):
        # Arrange
        self.obj1.location = self.char1
        input = f"{self.obj1}"
        expected_output = "You can't fill that!"

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_fill_fill_object_from_nothing(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        input = f"{container}"
        expected_output = f"Where do you want to fill the {container} from?"

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_fill_fill_object_from_not_liquid_container(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        input = f"{container} from {self.obj2}"
        expected_output = f"The {self.obj2} does not hold liquids."

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_fill_fill_object_from_empty_liquid_container(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        container2 = create_object(LiquidContainer, key="container2", location=self.room1)
        input = f"{container} from {container2}"
        expected_output = f"The {container2} is empty!"

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_fill_fill_object_from_liquid_container_emptied(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        container2 = create_object(LiquidContainer, key="container2", location=self.room1)

        container.fill_level = 2
        container2.fill_level = 4

        input = f"{container} from {container2}"
        expected_output = f"You empty the {container2} into the {container}."

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(container.fill_level, 6)
        self.assertEqual(container2.fill_level, 0)
        self.assertEqual(received_output, expected_output)

    def test_fill_fill_object_from_liquid_container_not_emptied(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        container2 = create_object(LiquidContainer, key="container2", location=self.room1)

        container.capacity = 3
        container.fill_level = 2
        container2.fill_level = 4

        input = f"{container} from {container2}"
        expected_output = f"You fill the {container} from the {container2}."

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(container.fill_level, 3)
        self.assertEqual(container2.fill_level, 3)
        self.assertEqual(received_output, expected_output)

    def test_fill_fill_object_from_liquid_container_not_enough(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        container2 = create_object(LiquidContainer, key="container2", location=self.room1)

        container.capacity = 3
        container.fill_level = 0
        container2.fill_level = 2

        input = f"{container} from {container2}"
        expected_output = f"You empty the {container2} into the {container}."

        # Act
        received_output = self.call(CmdFill(), input)

        # Assert
        self.assertEqual(container.fill_level, 2)
        self.assertEqual(container2.fill_level, 0)
        self.assertEqual(received_output, expected_output)

class TestCmdEmpty(EvenniaCommandTest):
    def test_empty_no_args(self):
        # Arrange
        input = ""
        expected_output = "Usage: EMPTY <container> (INTO <another container>)"

        # Act
        received_output = self.call(CmdEmpty(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_empty_object(self):
        # Arrange
        self.obj1.location = self.char1
        input = f"{self.obj1}"
        expected_output = f"You can't empty that!"

        # Act
        received_output = self.call(CmdEmpty(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_empty_empty_container(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        input = f"{container}"
        expected_output = f"The {container} is already empty!"

        # Act
        received_output = self.call(CmdEmpty(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_empty_full_container(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        container.fill_level = 10
        input = f"{container}"
        expected_output = f"You empty the {container} out on the ground."

        # Act
        received_output = self.call(CmdEmpty(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_empty_into_not_container(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        
        container.fill_level = 10
        input = f"{container} into {self.obj1}"
        expected_output = f"You cannot pour {container.liquid} into the {self.obj1}."

        # Act
        received_output = self.call(CmdEmpty(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_empty_into_empty_liquid_container(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        container2 = create_object(LiquidContainer, key="container2", location=self.char1)
        
        container.fill_level = 10
        container2.fill_level = 0

        input = f"{container} into {container2}"
        expected_output = f"You empty the {container} into the {container2}."

        # Act
        received_output = self.call(CmdEmpty(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

    def test_empty_into_liquid_container(self):
        # Arrange
        container = create_object(LiquidContainer, key="container", location=self.char1)
        container2 = create_object(LiquidContainer, key="container2", location=self.char1)
        
        container.fill_level = 10
        container2.fill_level = 5

        input = f"{container} into {container2}"
        expected_output = f"You empty the {container} into the {container2}.\nThe rest of the {container.liquid} splashes all over the ground."

        # Act
        received_output = self.call(CmdEmpty(), input)

        # Assert
        self.assertEqual(received_output, expected_output)

class TestCmdGet(EvenniaCommandTest):
    def test_get_no_args(self):
        # Arrange
        input = ""
        expected_output = "Usage: GET <object> (FROM <object>)"

        # Act
        received_output = self.call(CmdGet(), input)

        # Assert
        self.assertEqual(received_output, expected_output)
    
    def test_get_obj_in_room(self):
        # Arrange
        input = f"{self.obj1}"
        expected_output = f"You pick up the {self.obj1}."

        # Act
        received_output = self.call(CmdGet(), input)

        # Assert
        self.assertEqual(received_output, expected_output)
        self.assertEqual(self.obj1.location, self.char1)
    
    def test_get_missing_obj(self):
        # Arrange
        self.obj1.location = self.room2
        self.obj2.location = self.room2
        input = f"{self.obj1}"
        expected_output = f"Could not find '{self.obj1}'."

        # Act
        received_output = self.call(CmdGet(), input)

        # Assert
        self.assertEqual(received_output, expected_output)
        self.assertNotEqual(self.obj1.location, self.char1)

    def test_get_obj_in_obj(self):
        # Arrange
        self.obj2.location = self.char1.location
        self.obj1.location = self.obj2
        input = f"{self.obj1} from {self.obj2}"
        expected_output = f"You retrieve the {self.obj1} from the {self.obj2}."

        # Act
        received_output = self.call(CmdGet(), input)

        # Assert
        self.assertEqual(received_output, expected_output)
        self.assertEqual(self.obj1.location, self.char1)