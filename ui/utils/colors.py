# ui/utils/colors.py

_COLORS = {}


def define_color(name, value):
    """
    Guarda uma cor com o nome dado.
    Aceita (r, g, b).
    """
    if not (isinstance(value, tuple) and len(value) == 3):
        raise ValueError("A cor deve ser um tuplo (r, g, b).")
    _COLORS[name.lower()] = value
    return value


def get_color(name, default=None):
    """
    Retorna a cor guardada pelo nome, ou o valor default (ou erro se não houver).
    """
    key = name.lower()
    if key not in _COLORS:
        if default is not None:
            return default
        raise KeyError(f"Color '{name}' not found. Available: {', '.join(_COLORS)}")
    return _COLORS[key]

def clear_colors():
    """Limpa todas as cores guardadas."""
    _COLORS.clear()
    
# Base
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 40)

# Interface
PRIMARY = (0, 120, 255)
SECONDARY = (100, 100, 255)
ACCENT = (255, 180, 0)

SUCCESS = (0, 200, 0)
WARNING = (255, 200, 0)
ERROR = (200, 0, 0)

# Backgrounds
BG_MAIN = (20, 20, 20)
BG_PANEL = (30, 30, 30)
BG_HIGHLIGHT = (50, 50, 50)
