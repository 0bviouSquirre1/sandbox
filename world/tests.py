from evennia import utils
from evennia.utils.test_resources import EvenniaTest
from world.gpt_worldclock import WorldClock

class TestWorldClock(EvenniaTest):
    """Testing the World Clock Script"""
    def test_world_clock_exists(self):
        clock_script = utils.create.create_script(WorldClock)

        self.assertEqual(clock_script.time_passed, 0)

        clock_script.advance(3)

        self.assertEqual(clock_script.time_passed, 3)

        clock_script.advance(3)

        self.assertEqual(clock_script.time_passed, 6)