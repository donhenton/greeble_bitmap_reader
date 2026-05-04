"""
Configuration values for the reader.
"""

PANEL_WIDTH = 10.0
PANEL_HEIGHT = 5.0
PANEL_THICKNESS = 0.16

# Overlay sits just above the panel top. This makes the diagnostic map
# visibly slice/overlay the placed objects near their base.
OVERLAY_CLEARANCE = 0.012

GRID_COLUMNS = 3
GRID_ROWS = 2
GRID_SPACING_X = 12.0
GRID_SPACING_Y = 7.0

COLLECTION_BY_TYPE = {
    "large": "Greeble_Large",
    "medium": "Greeble_Medium",
    "small": "Greeble_Small",
}

COUNTS_BY_TYPE = {
    "large": (1, 1),
    "medium": (2, 3),
    "small": (3, 4),
}

MIN_DISTANCE_BY_TYPE = {
    "large": 0.55,
    "medium": 0.35,
    "small": 0.22,
}

INSET_BY_TYPE = {
    "large": 0.00,
    "medium": 0.00,
    "small": 0.00,
}

SCALE_RANGE_BY_TYPE = {
    "large": (0.95, 1.25),
    "medium": (0.80, 1.10),
    "small": (0.65, 0.95),
}

MINIMUM_REQUIRED_BY_TYPE = {
    "large": 1,
    "medium": 2,
    "small": 3,
}


# reader11:
# Placement no longer scatters multiple objects inside a region.
# Each region rectangle is treated as one centered placement anchor.
