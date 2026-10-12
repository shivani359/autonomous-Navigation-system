import unittest

from autonav.grid import GridMap
from autonav.planner import astar, manhattan_distance


class AStarTests(unittest.TestCase):
    def test_returns_shortest_route_around_wall(self):
        grid = GridMap(5, 5, frozenset({(2, 1), (2, 2), (2, 3)}))
        path = astar(grid, (0, 2), (4, 2))

        self.assertIsNotNone(path)
        assert path is not None
        self.assertEqual(path[0], (0, 2))
        self.assertEqual(path[-1], (4, 2))
        self.assertEqual(len(path) - 1, 8)
        self.assertTrue(all(grid.is_free(cell) for cell in path))
        self.assertTrue(all(manhattan_distance(a, b) == 1 for a, b in zip(path, path[1:])))

    def test_returns_none_when_goal_is_isolated(self):
        grid = GridMap(3, 3, frozenset({(1, 0), (0, 1), (2, 1), (1, 2)}))
        self.assertIsNone(astar(grid, (0, 0), (1, 1)))

    def test_same_start_and_goal_is_one_cell_path(self):
        grid = GridMap(3, 3, frozenset())
        self.assertEqual(astar(grid, (1, 1), (1, 1)), [(1, 1)])

    def test_rejects_blocked_or_out_of_bounds_endpoints(self):
        grid = GridMap(3, 3, frozenset({(1, 1)}))
        with self.assertRaises(ValueError):
            astar(grid, (1, 1), (2, 2))
        with self.assertRaises(ValueError):
            astar(grid, (0, 0), (3, 3))


if __name__ == "__main__":
    unittest.main()
