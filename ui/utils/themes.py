from types import SimpleNamespace
from ui.utils import colors

_current_theme = None


_THEMES = {
    "dark": {
        "text": (255, 255, 255),
        "background": (30, 30, 30),
        "panel": (50, 50, 50),
        "highlight": (0, 180, 255),
        "button_bg": (60, 60, 60),
        "button_hover": (80, 80, 80),
        "button_text": (255, 255, 255),
        "warning": (255, 80, 80),
    },
    "light": {
        "text": (20, 20, 20),
        "background": (100, 150, 200),
        "panel": (200, 200, 200),
        "highlight": (0, 100, 200),
        "button_bg": (220, 220, 220),
        "button_hover": (180, 180, 180),
        "button_text": (0, 0, 0),
        "warning": (255, 0, 0),
    },
}


def _to_namespace(d):
    """Converte dicionário em SimpleNamespace (para acesso por atributo)."""
    return SimpleNamespace(**d)


def set_theme(name: str, overrides=None):
    """
    Define o tema ativo.
    Aplica ao módulo colors e retorna um objeto `theme` com acesso por atributo.
    """
    global _current_theme

    if name not in _THEMES:
        raise ValueError(f"Tema '{name}' não encontrado. Opções: {', '.join(_THEMES)}")

    # copia o tema e aplica overrides
    theme_data = _THEMES[name].copy()
    if overrides:
        theme_data.update(overrides)

    # aplica as cores globais
    colors.clear_colors()
    colors._COLORS.update(theme_data)

    # cria objeto acessível por atributo
    theme = _to_namespace(theme_data)
    _current_theme = theme
    return theme


def get_theme(name="dark"):
    """Retorna um objeto theme (não altera o tema global)."""
    if name not in _THEMES:
        raise KeyError(f"Tema '{name}' não encontrado.")
    return _to_namespace(_THEMES[name])


def current_theme():
    """Retorna o tema atualmente ativo (objeto)."""
    if _current_theme is None:
        raise RuntimeError("Nenhum tema foi definido ainda. Usa set_theme().")
    return _current_theme
