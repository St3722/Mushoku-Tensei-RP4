# modules/__init__.py
from modules.save_manager import SaveManager
from .ai_manager import AIManager
from .character_progression import CharacterProgression
from .interface_cli import InterfaceCLI

# Pour s'assurer que ces modules sont disponibles lorsqu'on importe modules
__all__ = ['SaveManager', 'AIManager', 'CharacterProgression', 'InterfaceCLI']