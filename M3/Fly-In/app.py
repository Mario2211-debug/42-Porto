import argparse
import sys

from parser import Parser
from pathfinder import Pathfinder
from view_terminal import print_sim_output, print_terminal_vis
from view_pygame import PygameView


def app() -> None:
    arg_parser = argparse.ArgumentParser(description="Fly-In Simulator")
    arg_parser.add_argument("map_file", help="Path to the map file")
    arg_parser.add_argument(
        "--visualize",
        action="store_true",
        help="Launch pygame visualization",
    )
    arg_parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Skip colored terminal summary on stderr",
    )
    args = arg_parser.parse_args()

    try:
        with open(args.map_file, "r") as file:
            config = Parser().parse(file)

        pathfinder = Pathfinder(config)
        paths = pathfinder.solve()

        print_sim_output(paths, use_color=sys.stdout.isatty())

        if not args.no_summary:
            print_terminal_vis(config, paths)

        if args.visualize:
            print("Launching pygame visualization...", file=sys.stderr)
            PygameView(config, paths).run()

    except FileNotFoundError:
        print(f"Error: File '{args.map_file}' not found.", file=sys.stderr)
        sys.exit(1)

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    app()
