from enum import Enum, auto


class Orientation(Enum):
    up = auto(),
    down = auto(),
    left = auto(),
    right = auto(),


string_to_orientation = {
    'up': Orientation.up,
    'down': Orientation.down,
    'left': Orientation.left,
    'right': Orientation.right,
}

orientation_to_vector = {
    Orientation.up: (0, 1),
    Orientation.down: (0, -1),
    Orientation.left: (-1, 0),
    Orientation.right: (1, 0),
}
