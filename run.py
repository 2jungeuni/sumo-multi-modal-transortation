import os
import sys
import csv
import random
import pickle
import numpy as np
from pathlib import Path
from tabulate import tabulate
from collections import deque
from datetime import datetime
from scipy.spatial import KDTree

import warnings

warnings.filterwarnings("ignore", category=UserWarning)

import config.cfg as cfg
from utils.args import parse_args

# SUMO / Traci
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

import traci
import sumolib
from traci import TraCIException


# Retrieves SUMO's end time. If infinite, just return 90,000 as a safe bound
def get_max_time() -> int:
    max_sim_time = traci.simulation.getEndTime()
    return 90000 if max_sim_time == -1 else max_sim_time

def run(
        end: int = None
):
    if end is None:
        end = get_max_time()

    timestep = traci.simulation.getTime()
    start_time = round(timestep)

    running = True
    while running:
        # Advance simulation by 1 second
        traci.simulationStep(timestep)

        timestep += 1
        if timestep > end:
            running = False

    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    args = parse_args()

    # Overwrite configuration values
    cfg.sumo_config = args.sumo_config
    cfg.end = args.end

    if cfg.no_gui:
        sumoBinary = sumolib.checkBinary("sumo")
    else:
        sumoBinary = sumolib.checkBinary("sumo-gui")

    traci.start([sumoBinary,
                 "--no-warnings",
                 "-c", cfg.sumo_config,
                 "--seed", "42"])

    run(
        end=cfg.end
    )