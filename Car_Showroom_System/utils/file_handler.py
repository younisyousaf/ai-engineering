"""Save and load showroom inventory using JSON and context managers."""

import json
import os

# Default path relative to the project root (Car_Showroom_System/)
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "inventory.json")


def save_inventory(showroom, filepath=None):
    """Write cars and sales to a JSON file using `with open`."""
    # Local import avoids circular import with models.car
    from models.car import Car

    path = filepath or DEFAULT_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)

    payload = {
        "showroom_name": showroom.name,
        "cars": [car.to_dict() for car in showroom.cars],
        "sales": {str(k): v for k, v in showroom.sales.items()},
        "next_id": Car._next_id,
    }

    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
    except OSError as error:
        raise OSError(f"Could not save inventory to {path}: {error}") from error
    else:
        return path


def load_inventory(showroom, filepath=None):
    """
    Read inventory from JSON into an existing Showroom.

    Uses try / except / else / finally like exceptions.ipynb.
    Raises FileNotFoundError if the file does not exist.
    """
    # Local import avoids circular import with models.car
    from models.car import Car

    path = filepath or DEFAULT_PATH
    loaded = False

    try:
        with open(path, "r", encoding="utf-8") as file:
            payload = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"No inventory file found at '{path}'. Save first, then load."
        )
    except json.JSONDecodeError as error:
        raise ValueError(f"Inventory file is not valid JSON: {error}") from error
    else:
        showroom.name = payload.get("showroom_name", showroom.name)
        showroom.cars = [Car.from_dict(item) for item in payload.get("cars", [])]
        # JSON keys are always strings — convert back to int car ids
        raw_sales = payload.get("sales", {})
        showroom.sales = {int(k): v for k, v in raw_sales.items()}
        Car._next_id = payload.get("next_id", Car._next_id)
        loaded = True
        return path
    finally:
        # Always runs — mirrors try/except/else/finally from exceptions.ipynb
        if loaded:
            pass
