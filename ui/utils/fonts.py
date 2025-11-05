# ui/utils/fonts.py

import pygame
from pathlib import Path

pygame.font.init()

# Caminho padrão (usa o do sistema se não tiver fonte própria)
ASSETS_FONT_PATH = Path("assets/fonts")
DEFAULT_FONT_PATH = next(ASSETS_FONT_PATH.glob("*.ttf"), None) if ASSETS_FONT_PATH.exists() else None


# Dicionário-cache de fontes carregadas
_FONTS_CACHE = {}


def _get_font(size: int, bold=False, italic=False, name=None):
    """
    Retorna (e guarda em cache) uma fonte com as propriedades pedidas.
    Se 'name' for dado, o resultado é guardado em FONTS com esse nome.
    """
    key = name or f"{size}_{'b' if bold else ''}{'i' if italic else ''}"
    if key not in _FONTS_CACHE:
        font = pygame.font.Font(DEFAULT_FONT_PATH, size, bold=bold, italic=italic)
        font.set_bold(bold)
        font.set_italic(italic)
        _FONTS_CACHE[key] = font
    return _FONTS_CACHE[key]


# --- Predefinições ---
SMALL = _get_font(16, name="small")
MEDIUM = _get_font(24, name="medium")
LARGE = _get_font(32, name="large")

SMALL_BOLD = _get_font(16, bold=True, name="small_bold")
MEDIUM_BOLD = _get_font(24, bold=True, name="medium_bold")
LARGE_BOLD = _get_font(32, bold=True, name="large_bold")

SMALL_ITALIC = _get_font(16, italic=True, name="small_italic")
MEDIUM_ITALIC = _get_font(24, italic=True, name="medium_italic")
LARGE_ITALIC = _get_font(32, italic=True, name="large_italic")

# Dicionário público de acesso
FONTS = _FONTS_CACHE


def get_font(name_or_size, **kwargs):
    """
    Uso flexível:
      - get("medium_bold") → devolve a fonte guardada
      - get(24, bold=True, italic=True) → cria e guarda nova
    """
    if isinstance(name_or_size, str):
        key = name_or_size.lower()
        if key not in FONTS:
            raise ValueError(f"Font '{key}' not found. Available: {', '.join(FONTS)}")
        return FONTS[key]
    elif isinstance(name_or_size, int):
        return _get_font(name_or_size, **kwargs)
    else:
        raise TypeError("Use a font name (str) or a size (int).")
