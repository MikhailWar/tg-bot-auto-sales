from dataclasses import dataclass


@dataclass
class Item(object):
    id: int
    name: str
    description: str
    price: int
    photo: str



