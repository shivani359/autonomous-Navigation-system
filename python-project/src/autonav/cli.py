"""Command-line entry point for graphical and reproducible runs."""

from __future__ import annotations

import argparse
import json
import sys

from .scenarios import available_scenarios, scenario_by_key
from .simulator import Simulator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the autonomous navigation grid-world simulator."
    )
    parser.add_argument(
        "--scenario",
        default="warehouse",
        help="scenario filename stem (use --list-scenarios to see choices)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="run deterministically in the terminal without opening a window",
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="print available scenario names and descriptions",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        scenarios = available_scenarios()
        if args.list_scenarios:
            for key, scenario in scenarios.items():
                print(f"{key}: {scenario.name} — {scenario.description}")
            return 0

        scenario = scenario_by_key(args.scenario)
        if args.headless:
            simulation = Simulator(scenario)
            simulation.start()
            step_limit = scenario.width * scenario.height * 4
            for _ in range(step_limit):
                if simulation.status != "running":
                    break
                simulation.step()
            if simulation.status not in {"completed", "no_path"}:
                raise RuntimeError(f"Simulation stopped unexpectedly: {simulation.status}")
            print(json.dumps(simulation.metrics().as_dict(), indent=2))
            return 0 if simulation.status == "completed" else 2

        # Import pygame only when the visualizer is requested.
        from .visualizer import run_visualizer

        run_visualizer(scenario)
        return 0
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
