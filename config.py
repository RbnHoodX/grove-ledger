"""Configuration and constants for the grove-ledger system."""

# Default plot kinds
PLOT_KINDS = ("bed", "reservoir", "channel", "pond", "raised")

# Water measurement units
UNITS = {
    "liters": 1.0,
    "gallons": 3.78541,
    "cubic_meters": 1000.0,
}

# Default irrigation parameters
DEFAULT_FLOW_RATE = 10  # liters per minute
MAX_IRRIGATION_DURATION = 120  # minutes
MIN_WATER_LEVEL = 0

# Seasonal multipliers for water consumption
SEASONAL_FACTORS = {
    "spring": 0.8,
    "summer": 1.5,
    "autumn": 0.6,
    "winter": 0.3,
}

# Soil moisture retention by plot kind
MOISTURE_RETENTION = {
    "bed": 0.7,
    "reservoir": 1.0,
    "channel": 0.3,
    "pond": 0.95,
    "raised": 0.6,
}

# Report formatting
REPORT_DATE_FORMAT = "%Y-%m-%d %H:%M"
REPORT_SEPARATOR = "-" * 60
REPORT_HEADER_WIDTH = 60
