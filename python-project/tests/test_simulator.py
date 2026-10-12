import unittest

from autonav.scenarios import available_scenarios
from autonav.simulator import Simulator


class SimulatorTests(unittest.TestCase):
    def test_every_example_scenario_reaches_goal_without_collision(self):
        for scenario in available_scenarios().values():
            with self.subTest(scenario=scenario.name):
                simulation = Simulator(scenario)
                simulation.start()
                limit = scenario.width * scenario.height * 4
                for _ in range(limit):
                    if simulation.status != "running":
                        break
                    simulation.step()

                self.assertEqual(simulation.status, "completed")
                self.assertEqual(simulation.robot, scenario.goal)
                self.assertEqual(simulation.collisions, 0)
                self.assertEqual(simulation.steps_taken, len(simulation.route or []) - 1)

    def test_pause_and_reset_preserve_map_but_clear_run_state(self):
        simulation = Simulator(available_scenarios()["warehouse"])
        simulation.start()
        self.assertTrue(simulation.step())
        simulation.pause()
        self.assertEqual(simulation.status, "paused")
        simulation.reset()
        self.assertEqual(simulation.status, "ready")
        self.assertEqual(simulation.robot, simulation.scenario.start)
        self.assertEqual(simulation.steps_taken, 0)
        self.assertEqual(simulation.collisions, 0)


if __name__ == "__main__":
    unittest.main()
