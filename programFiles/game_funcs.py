"""Save and load complete Luigi's Mansion game instances as JSON.

The public functions in this module are ``save_game`` and ``load_game``.
Unless a different path is supplied, both functions use ``game_saves.json``.
"""

import importlib
import json
import os
from pathlib import Path


SAVE_FILE = "game_saves.json"
SAVE_FORMAT = "luigis-mansion-game-save"
SAVE_VERSION = 1


# Only classes that belong to this game may be reconstructed from a save file.
# Add a new class here if a new kind of object is later stored in a Game.
_CLASS_LOCATIONS = {
    "game": ("game", "game"),
    "level": ("level", "level"),
    "room": ("room", "room"),
    "character": ("character", "character"),
    "luigi": ("luigi", "luigi"),
    "ghost": ("ghost", "ghost"),
    "goldGhost": ("goldGhost", "goldGhost"),
    "purplePuncher": ("purplePuncher", "purplePuncher"),
    "item": ("item", "item"),
    "smallHeart": ("smallHeart", "smallHeart"),
    "largeHeart": ("largeHeart", "largeHeart"),
    "smallArmor": ("smallArmor", "smallArmor"),
    "largeArmor": ("largeArmor", "largeArmor"),
}

_CLASS_CACHE = {}


def save_game(game_instance, file_name=SAVE_FILE):
    """Write ``game_instance`` and all of its current state to a JSON file.

    The save is written atomically: the old save remains untouched if writing
    the replacement fails. The returned ``Path`` identifies the save file.
    """
    if game_instance.__class__.__name__ != "game":
        raise TypeError("save_game expected an instance of the game class")

    save_path = Path(file_name)
    temporary_path = save_path.with_name(save_path.name + ".tmp")
    object_ids = {}

    save_data = {
        "format": SAVE_FORMAT,
        "version": SAVE_VERSION,
        "game": _to_json_value(game_instance, object_ids, set()),
    }

    try:
        with temporary_path.open("w", encoding="utf-8") as save_file:
            json.dump(save_data, save_file, indent=4, ensure_ascii=False)
            save_file.write("\n")
            save_file.flush()
            os.fsync(save_file.fileno())
        os.replace(temporary_path, save_path)
    except Exception:
        # Remove only this function's incomplete temporary file. Never remove
        # the caller's existing game_saves.json after a failed write.
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        raise

    return save_path


def load_game(file_name=SAVE_FILE):
    """Read a JSON save file and return the reconstructed game instance.

    Constructors are intentionally not called while loading. Calling them
    would create a new Luigi and randomly redistribute a level's entities,
    which would change the state that was saved.
    """
    save_path = Path(file_name)

    try:
        with save_path.open("r", encoding="utf-8") as save_file:
            save_data = json.load(save_file)
    except json.JSONDecodeError as error:
        raise ValueError(
            "The game save is not valid JSON: {0}".format(save_path)
        ) from error

    if not isinstance(save_data, dict):
        raise ValueError("The game save must contain a JSON object")
    if save_data.get("format") != SAVE_FORMAT:
        raise ValueError("The file is not a Luigi's Mansion game save")
    if save_data.get("version") != SAVE_VERSION:
        raise ValueError(
            "Unsupported game save version: {0}".format(save_data.get("version"))
        )
    if "game" not in save_data:
        raise ValueError("The game save does not contain game data")

    loaded_game = _from_json_value(save_data["game"], {})
    if loaded_game.__class__.__name__ != "game":
        raise ValueError("The game save's root object is not a game instance")

    return loaded_game


def _to_json_value(value, object_ids, active_containers):
    """Convert a supported Python value into a JSON-compatible value."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value

    if isinstance(value, list):
        return _sequence_to_json(value, "list", object_ids, active_containers)

    if isinstance(value, tuple):
        return _sequence_to_json(value, "tuple", object_ids, active_containers)

    if isinstance(value, dict):
        container_id = id(value)
        if container_id in active_containers:
            raise TypeError("The game contains a recursive dictionary")
        active_containers.add(container_id)
        try:
            items = {}
            for key, item in value.items():
                if not isinstance(key, str):
                    raise TypeError("Game dictionaries must use string keys")
                items[key] = _to_json_value(item, object_ids, active_containers)
            return {"__kind__": "dict", "items": items}
        finally:
            active_containers.remove(container_id)

    class_name = value.__class__.__name__
    if class_name not in _CLASS_LOCATIONS:
        raise TypeError(
            "Cannot save unsupported object type: {0}".format(class_name)
        )
    if not hasattr(value, "__dict__"):
        raise TypeError("Cannot save an object without instance attributes")

    python_id = id(value)
    if python_id in object_ids:
        return {"__kind__": "reference", "id": object_ids[python_id]}

    save_id = len(object_ids) + 1
    object_ids[python_id] = save_id
    _CLASS_CACHE[class_name] = value.__class__

    attributes = {
        name: _to_json_value(attribute, object_ids, active_containers)
        for name, attribute in vars(value).items()
    }
    return {
        "__kind__": "object",
        "id": save_id,
        "type": class_name,
        "attributes": attributes,
    }


def _sequence_to_json(container, kind, object_ids, active_containers):
    """Wrap a list or tuple and reject cycles that JSON cannot represent."""
    container_id = id(container)
    if container_id in active_containers:
        raise TypeError("The game contains a recursive {0}".format(kind))
    active_containers.add(container_id)
    try:
        # The wrapper keeps tuples distinguishable from lists in the JSON.
        return {
            "__kind__": kind,
            "items": [
                _to_json_value(item, object_ids, active_containers)
                for item in container
            ],
        }
    finally:
        active_containers.remove(container_id)


def _from_json_value(value, restored_objects):
    """Convert a saved JSON value back into its original Python value."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if not isinstance(value, dict):
        raise ValueError("Malformed value in game save")

    kind = value.get("__kind__")

    if kind == "list":
        items = _require_list(value, "items")
        return [_from_json_value(item, restored_objects) for item in items]

    if kind == "tuple":
        items = _require_list(value, "items")
        return tuple(_from_json_value(item, restored_objects) for item in items)

    if kind == "dict":
        items = value.get("items")
        if not isinstance(items, dict):
            raise ValueError("Malformed dictionary in game save")
        return {
            key: _from_json_value(item, restored_objects)
            for key, item in items.items()
        }

    if kind == "reference":
        save_id = value.get("id")
        if save_id not in restored_objects:
            raise ValueError("Game save contains an invalid object reference")
        return restored_objects[save_id]

    if kind == "object":
        save_id = value.get("id")
        class_name = value.get("type")
        attributes = value.get("attributes")

        if not isinstance(save_id, int) or save_id <= 0:
            raise ValueError("Game save contains an invalid object ID")
        if save_id in restored_objects:
            raise ValueError("Game save contains a duplicate object ID")
        if class_name not in _CLASS_LOCATIONS:
            raise ValueError(
                "Game save contains unsupported object type: {0}".format(class_name)
            )
        if not isinstance(attributes, dict):
            raise ValueError("Game save contains malformed object attributes")

        object_class = _resolve_class(class_name)
        restored_object = object.__new__(object_class)
        restored_objects[save_id] = restored_object

        for name, attribute in attributes.items():
            if not isinstance(name, str):
                raise ValueError("Game save contains an invalid attribute name")
            setattr(
                restored_object,
                name,
                _from_json_value(attribute, restored_objects),
            )
        return restored_object

    raise ValueError("Game save contains an unknown value type")


def _require_list(value, key):
    items = value.get(key)
    if not isinstance(items, list):
        raise ValueError("Malformed {0} in game save".format(value.get("__kind__")))
    return items


def _resolve_class(class_name):
    """Return a known game class without trusting module names from JSON."""
    if class_name in _CLASS_CACHE:
        return _CLASS_CACHE[class_name]

    module_name, attribute_name = _CLASS_LOCATIONS[class_name]
    module = importlib.import_module(module_name)
    object_class = getattr(module, attribute_name)

    if not isinstance(object_class, type):
        raise TypeError(
            "{0}.{1} is not a class".format(module_name, attribute_name)
        )

    _CLASS_CACHE[class_name] = object_class
    return object_class
