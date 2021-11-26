from dataclasses import dataclass
from serde import serialize, deserialize


@deserialize
@serialize
@dataclass
class SizeEntity:
    id: int
    length: int
    width: int
    height: int
    lbs: int
