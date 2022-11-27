""" Small Utility Functions """
import json
from typing import Any


def jdict(**kwargs: Any) -> str:
    """Dump arguments into a JSON-encoded string"""
    return json.dumps(dict(**kwargs))
