"""
Grid positioning for multiple examples.
"""

from .config import GRID_COLUMNS, GRID_SPACING_X, GRID_SPACING_Y


def grid_position(example_index):
    """
    Fill a 2 x 3 grid using the first 5 slots.
    One slot is naturally left missing.
    """
    col = example_index % GRID_COLUMNS
    row = example_index // GRID_COLUMNS

    x = (col - 1) * GRID_SPACING_X
    y = (0.5 - row) * GRID_SPACING_Y
    z = 0.0

    return (x, y, z)
