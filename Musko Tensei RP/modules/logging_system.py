import logging
import os
from datetime import datetime

def setup_logger():
    """Configure et retourne un logger pour le jeu"""
    # Créer le dossier logs s'il n'existe pas
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Nom de fichier avec date/heure
    log_filename = f"logs/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configuration du logger
    logger = logging.getLogger("musko_tensei")
    logger.setLevel(logging.INFO)
    
    # Handler pour fichier
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Format des messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Ajouter les handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
game_logger = setup_logger()