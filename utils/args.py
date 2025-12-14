import argparse
from tabulate import tabulate

from config import cfg


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run AMoD simulation with SUMO and TraCI"
    )

    parser.add_argument(
        "--sumo-config",
        "-c",
        type=str,
        default=cfg.sumo_config,
        help="Path to the SUMO configuration file (.sumocfg or .sumocfg.xml)"
    )

    parser.add_argument(
        "--end",
        "-e",
        type=int,
        default=cfg.end,
        help="Simulation end time (seconds)"
    )

    args = parser.parse_args()
    table = tabulate(
        vars(args).items(),
        headers=["Argument", "Value"],
        tablefmt="fancy_grid",
        showindex=False
    )
    print(table)
    return args