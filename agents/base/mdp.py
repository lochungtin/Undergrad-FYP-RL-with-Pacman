from copy import deepcopy
from random import Random
from typing import List, Tuple, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from game.game import Game

from ai.deepq.neuralnet import NeuralNet
from ai.neat.genome import Genome
from data.config import BOARD, POS
from data.data import GHOST_MODE
from game.components.component import Component
from game.utils.cell import Cell
from game.utils.pathfinder import PathFinder
from utils.coordinate import CPair
from utils.direction import DIR