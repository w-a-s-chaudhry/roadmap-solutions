# Author:      Wajid Ali Saleem Chaudhry
# Description: Pure-Python unit conversion classes (length and
#              temperature). No Flask here — just the maths.


# --- Length ---

# Converts lengths by routing every value through metres as a common
# base. Each entry in TO_METRES says how many metres one of that unit
# equals, so any pair-conversion is value * from_factor / to_factor.
class LengthConverter:
  TO_METRES = {
    "millimeters": 0.001,
    "centimeters": 0.01,
    "meters":      1.0,
    "kilometers":  1000.0,
    "inches":      0.0254,
    "feet":        0.3048,
    "yards":       0.9144,
    "miles":       1609.344,
  }

  # Convert `value` from `from_unit` to `to_unit`; raises ValueError
  # for any unit not in TO_METRES so app.py can return HTTP 400.
  def convert(self, value, from_unit, to_unit):
    if from_unit not in self.TO_METRES:
      raise ValueError(f"Unknown length unit: {from_unit}")
    if to_unit not in self.TO_METRES:
      raise ValueError(f"Unknown length unit: {to_unit}")
    in_metres = value * self.TO_METRES[from_unit]
    return in_metres / self.TO_METRES[to_unit]

  # List of supported unit names; exposed so app.py / the frontend
  # could later ask the converter what it accepts.
  @property
  def units(self):
    return list(self.TO_METRES.keys())


# --- Temperature ---

# Converts temperatures by routing through Celsius. Can't use a
# single multiplier table like LengthConverter because Fahrenheit
# has a 32-degree offset — the scales aren't proportional.
class TemperatureConverter:
  UNITS = ("celsius", "fahrenheit", "kelvin")

  # Convert `value` from `from_unit` to `to_unit` via Celsius as an
  # intermediate; raises ValueError for unknown units.
  def convert(self, value, from_unit, to_unit):
    if from_unit not in self.UNITS:
      raise ValueError(f"Unknown temperature unit: {from_unit}")
    if to_unit not in self.UNITS:
      raise ValueError(f"Unknown temperature unit: {to_unit}")

    # Step 1: anything in -> celsius
    if from_unit == "celsius":
      celsius = value
    elif from_unit == "fahrenheit":
      celsius = (value - 32) * 5 / 9
    else:  # kelvin
      celsius = value - 273.15

    # Step 2: celsius -> anything out
    if to_unit == "celsius":
      return celsius
    elif to_unit == "fahrenheit":
      return celsius * 9 / 5 + 32
    else:  # kelvin
      return celsius + 273.15

  @property
  def units(self):
    return list(self.UNITS)


# --- Weight ---

# Converts weights by routing every value through grams as a common
# base. Same trick as LengthConverter — one factor table, every
# pair-conversion is value * from_factor / to_factor.
class WeightConverter:
  TO_GRAMS = {
    "mg": 0.001,
    "g":  1.0,
    "kg": 1000.0,
    "oz": 28.349523125,
    "lb": 453.59237,
  }

  # Convert `value` from `from_unit` to `to_unit`; raises ValueError
  # for any unit not in TO_GRAMS so app.py can return HTTP 400.
  def convert(self, value, from_unit, to_unit):
    if from_unit not in self.TO_GRAMS:
      raise ValueError(f"Unknown weight unit: {from_unit}")
    if to_unit not in self.TO_GRAMS:
      raise ValueError(f"Unknown weight unit: {to_unit}")
    in_grams = value * self.TO_GRAMS[from_unit]
    return in_grams / self.TO_GRAMS[to_unit]

  @property
  def units(self):
    return list(self.TO_GRAMS.keys())