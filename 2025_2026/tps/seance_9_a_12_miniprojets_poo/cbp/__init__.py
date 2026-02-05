
import os
from pathlib import Path
CURRENT_FOLDER = Path(os.path.dirname(__file__))
DATA_FOLDER = CURRENT_FOLDER / '../../data/'

from cbp.data.datasets import load_dataset