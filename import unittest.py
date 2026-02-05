import unittest

from delivery_simulator import euclidean_distance, nearest_agent, simulate_day


class DeliverySimulatorTests(unittest.TestCase):
    def test_euclidean_distance(self):
        self.assertAlmostEqual(euclidean_distance((0, 0), (3, 4)), 5.0)

    def test_nearest_agent_tie_breaker(self):
        agents = {"A2": (0, 0), "A1": (0, 0)}
        self.assertEqual(nearest_agent(agents, (1, 1)), "A1")

    def test_simulation_delivered_count_matches_packages(self):
        data = {
            "warehouses": {"W1": [0, 0], "W2": [10, 0]},
            "agents": {"A1": [0, 0], "A2": [10, 0]},
            "packages": [
                {"id": "P1", "warehouse": "W1", "destination": [1, 1]},
                {"id": "P2", "warehouse": "W2", "destination": [9, 2]},
                {"id": "P3", "warehouse": "W1", "destination": [2, 3]},
            ],
        }

        report, _ = simulate_day(data)
        delivered = sum(
            stats["packages_delivered"]
            for agent, stats in report.items()
            if agent != "best_agent"
        )
        self.assertEqual(delivered, len(data["packages"]))

    def test_midday_join(self):
        data = {
            "warehouses": {"W1": [0, 0], "W2": [100, 0]},
            "agents": {"A1": [0, 0]},
            "packages": [
                {"id": "P1", "warehouse": "W2", "destination": [101, 0]},
                {"id": "P2", "warehouse": "W2", "destination": [102, 0]},
            ],
            "midday_agent_joins": [
                {"after_deliveries": 1, "id": "A2", "position": [100, 0]}
            ],
        }

        report, _ = simulate_day(data)
        self.assertEqual(report["A2"]["packages_delivered"], 1)


if __name__ == "__main__":
    unittest.main()
