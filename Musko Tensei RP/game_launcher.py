# BLOC 1: Imports et Configuration Initiale
import sys
import os
import time
import json
import importlib
import random
import logging

# Configurer les chemins d'importation
project_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.join(project_path, "modules")
sys.path.insert(0, project_path)
sys.path.insert(0, modules_path)

# Configurer le système de logging
def setup_logger():
    """Configure et retourne un logger pour le jeu"""
    # Créer le dossier logs s'il n'existe pas
    logs_dir = os.path.join(project_path, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Nom de fichier avec date/heure
    from datetime import datetime
    log_filename = os.path.join(logs_dir, f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
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

# Initialiser le logger
logger = setup_logger()
logger.info("Démarrage du jeu Musko Tensei RP...")

# Nettoyer les répertoires __pycache__ pour éviter les problèmes d'importation
def clean_pycache():
    try:
        pycache_dir = os.path.join(modules_path, "__pycache__")
        if os.path.exists(pycache_dir):
            logger.info("Nettoyage des fichiers cache Python...")
            for file in os.listdir(pycache_dir):
                file_path = os.path.join(pycache_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        logger.debug(f"Fichier supprimé - {file_path}")
                except Exception as e:
                    logger.error(f"Erreur lors de la suppression de {file_path}: {e}")
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des caches: {e}")

# Nettoyer les caches Python
clean_pycache()

# Forcer le rechargement des modules s'ils sont déjà importés
if "save_manager" in sys.modules:
    logger.info("Rechargement du module save_manager...")
    importlib.reload(sys.modules["save_manager"])
if "character_progression" in sys.modules:
    logger.info("Rechargement du module character_progression...")
    importlib.reload(sys.modules["character_progression"])
if "interface_cli" in sys.modules:
    logger.info("Rechargement du module interface_cli...")
    importlib.reload(sys.modules["interface_cli"])
if "ai_manager" in sys.modules:
    logger.info("Rechargement du module ai_manager...")
    importlib.reload(sys.modules["ai_manager"])
# Fin BLOC 1: Imports et Configuration Initiale

# BLOC 2: Classes et Fonctions d'Importation
# Fonction pour importer un module avec gestion d'erreur avancée
def safe_import(module_name, class_name):
    logger.info(f"Importation de {class_name} depuis {module_name}...")
    try:
        # Essayer l'importation directe
        module = __import__(f"modules.{module_name}", fromlist=[class_name])
        cls = getattr(module, class_name)
        logger.info(f"  ✅ Import réussi!")
        return cls
    except (ImportError, AttributeError) as e:
        logger.error(f"  ❌ Erreur lors de l'importation standard: {e}")
        
        # Tentative alternative - importation directe du fichier
        try:
            logger.info(f"  Tentative d'importation alternative...")
            import importlib.util
            file_path = os.path.join(modules_path, f"{module_name}.py")
            
            if not os.path.exists(file_path):
                logger.error(f"  ❌ Le fichier {file_path} n'existe pas!")
                return None
                
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                logger.error(f"  ❌ Impossible de créer un spec pour {file_path}")
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, class_name):
                cls = getattr(module, class_name)
                logger.info(f"  ✅ Import alternatif réussi!")
                return cls
            else:
                logger.error(f"  ❌ La classe {class_name} n'existe pas dans {module_name}.py")
                logger.debug(f"  Classes disponibles: {[name for name in dir(module) if not name.startswith('_')]}")
                return None
        except Exception as e2:
            logger.error(f"  ❌ Échec de l'importation alternative: {e2}")
            return None

# Classes de remplacement (simplifiées)
class SaveManagerSimple:
    def __init__(self, game_instance=None):
        self.game = game_instance
        self.save_directory = "saves"
        os.makedirs(self.save_directory, exist_ok=True)
        logger.info("SaveManager simplifié initialisé!")
        
    def save_game(self, slot_name="default", save_name=None):
        save_path = os.path.join(self.save_directory, f"{slot_name}_{save_name}.json")
        logger.info(f"Jeu sauvegardé dans {save_path}")
        return {"success": True, "save_path": save_path}
        
    def load_game(self, save_path=None):
        logger.info(f"Chargement du jeu depuis {save_path}")
        return {"success": True}
        
    def auto_save(self):
        logger.info("Auto-sauvegarde effectuée")
        return {"success": True}
        
    def list_saves(self):
        return []

class AIManagerSimple:
    def __init__(self, game_instance=None):
        self.game = game_instance
        self.narrative_style = {
            "descriptive_detail": 0.8,
            "sensory_immersion": 0.7,
            "dialogue_quality": 0.9,
            "emotional_tone": "balanced"
        }
        self.available_races = [
            "Human Race", 
            "Elf Race",
            "High Elf Race", 
            "Dwarf Race", 
            "Halfling Race", 
            "Dragon Tribe", 
            "Migurd Race", 
            "Superd Race",
            "Immortal Demon Race",
            "Ogre Race",
            "Beast Race",
            "Heaven Race",
            "Sea Race",
            "Mixed-Blood Race",
            "Cursed Children",
            "Elemental Spirits",
            "Sylphs",
            "Ancient Races"
        ]
        self.race_descriptions = {
            "Human Race": "Race dominante du continent. Polyvalente et adaptable.",
            "Elf Race": "Les Elfes sont une race élégante à la longévité remarquable. Moins mystiques que leurs cousins Hauts Elfes, ils sont néanmoins gracieux et agiles. Leur affinité naturelle avec la nature et la magie en fait d'excellents archers et lanceurs de sorts. Leurs oreilles pointues et leur silhouette élancée les distinguent des humains. Ils vivent généralement dans des communautés forestières où ils vénèrent les forces naturelles."
        }
        logger.info("AIManager simplifié initialisé!")
        
    def generate_response(self, prompt, context):
        # Pour améliorer la qualité linguistique
        prompt = f"""
        {prompt}
        
        EXIGENCES FONDAMENTALES:
        1. ORTHOGRAPHE: Ton texte doit être TOTALEMENT exempt de fautes d'orthographe.
        2. GRAMMAIRE: Ta syntaxe doit être irréprochable avec des accords parfaits.
        3. COHÉRENCE: Respecte scrupuleusement les caractéristiques du personnage.
        4. ÉLÉGANCE: Privilégie un style littéraire fluide et captivant.
        
        Relis soigneusement ton texte pour éliminer toute erreur avant de le soumettre.
        """
        return f"[IA Simple] Réponse à: {prompt[:30]}..."
        
    def generate_description(self, location_id, time_of_day="day", weather="clear"):
        return f"[IA Simple] Description de {location_id} pendant {time_of_day} avec temps {weather}."
    
    def generate_npc_dialogue(self, character_id, dialogue_type, user_input, additional_context=None):
        return f"[IA Simple] Dialogue de PNJ {character_id} de type {dialogue_type}"
    
    def generate_combat_narrative(self, player_data, enemy_id, action, combat_state):
        return f"[IA Simple] Narration de combat contre {enemy_id} avec action {action}"

class CharacterProgressionSimple:
    def __init__(self, game_instance=None):
        self.game = game_instance
        logger.info("CharacterProgression simplifié initialisé!")
        
    def gain_experience(self, amount):
        logger.info(f"Gain d'expérience: {amount}")
        
    def level_up(self):
        logger.info("Niveau augmenté!")

class InterfaceCLISimple:
    def __init__(self, game_instance=None):
        self.game = game_instance
        logger.info("InterfaceCLI simplifié initialisé!")
        
    def display_message(self, message):
        print(message)
        
    def get_input(self, prompt):
        return input(prompt)

# Importer les modules réels de manière sécurisée
SaveManager = safe_import("save_manager", "SaveManager") or SaveManagerSimple
AIManager = safe_import("ai_manager", "AIManager") or AIManagerSimple
CharacterProgression = safe_import("character_progression", "CharacterProgression") or CharacterProgressionSimple
InterfaceCLI = safe_import("interface_cli", "InterfaceCLI") or InterfaceCLISimple
# Fin BLOC 2: Classes et Fonctions d'Importation

# BLOC 3: Classe principale MuskoTenseiRP - Initialisation
class MuskoTenseiRP:
    """Classe principale du jeu MUSKO TENSEI RP"""
    
    def __init__(self):
        self.version = "1.0.0"
        logger.info(f"Initialisation du jeu Musko Tensei RP...")
        
        # Initialiser les gestionnaires
        self.save_manager = SaveManager(self)
        self.ai_manager = AIManager(self)
        self.character_progression = CharacterProgression(self)
        self.interface = InterfaceCLI(self)
        
        # S'assurer que la liste des races inclut les Elfes normaux
        if "Elf Race" not in self.ai_manager.available_races:
            self.ai_manager.available_races.insert(1, "Elf Race")
        
        # Ajouter une description pour les Elfes normaux si non existante
        if "Elf Race" not in self.ai_manager.race_descriptions:
            self.ai_manager.race_descriptions["Elf Race"] = (
                "Les Elfes sont une race élégante à la longévité remarquable. Moins mystiques que "
                "leurs cousins Hauts Elfes, ils sont néanmoins gracieux et agiles. Leur affinité naturelle "
                "avec la nature et la magie en fait d'excellents archers et lanceurs de sorts. "
                "Leurs oreilles pointues et leur silhouette élancée les distinguent des humains. "
                "Ils vivent généralement dans des communautés forestières où ils vénèrent les forces naturelles."
            )
        
        # Initialiser les états par défaut
        self.player = {
            "name": "Aventurier",
            "level": 1,
            "exp": 0,
            "stats": {
                "force": 10,
                "intelligence": 10,
                "dexterite": 10,
                "constitution": 10,
                "sagesse": 10,
                "charisme": 10
            }
        }
        self.current_location = "village_depart"
        self.game_flags = {}
        self.player_inventory = {}
        self.game_time = {
            "day": 1,
            "hour": 8,
            "minute": 0,
            "weather": "clear"
        }
        
        # Initialiser les systèmes avancés
        self._initialize_advanced_systems()
        
        # Charger les données du jeu
        self.load_game_data()
        
        # Créer des fichiers de données par défaut si nécessaires
        self.ensure_data_files_exist()
        
        logger.info("Jeu initialisé avec succès!")
# Fin BLOC 3: Classe principale MuskoTenseiRP - Initialisation

# BLOC 4: Méthodes de gestion des données du jeu
    def ensure_data_files_exist(self):
        """Crée les fichiers de données de base s'ils n'existent pas"""
        data_dir = os.path.join(project_path, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Exemples de données minimales
        basic_data = {
            "locations.json": {
                "village_depart": {
                    "name": "Village de Burina",
                    "description": "Un paisible village niché entre montagnes et forêts",
                    "connections": ["foret_ouest", "route_marchande"],
                    "npcs": ["aubergiste", "forgeron"]
                },
                "foret_ouest": {
                    "name": "Forêt de Shirai",
                    "description": "Une forêt dense aux arbres immenses dont les cimes filtrent la lumière",
                    "connections": ["village_depart", "clairiere"],
                    "npcs": ["chasseur"]
                }
            },
            "npcs.json": {
                "aubergiste": {
                    "name": "Giles l'Aubergiste",
                    "personality": "Jovial et bavard, toujours prêt à partager les derniers potins",
                    "location": "village_depart"
                },
                "forgeron": {
                    "name": "Darun le Forgeron",
                    "personality": "Robuste et taciturne, mais expert dans son art",
                    "location": "village_depart"
                },
                "chasseur": {
                    "name": "Miriam la Chasseuse",
                    "personality": "Alerte et perspicace, connaît la forêt comme sa poche",
                    "location": "foret_ouest"
                }
            },
            "items.json": {
                "potion_soin": {
                    "name": "Potion de soin",
                    "description": "Un liquide rouge qui guérit les blessures",
                    "value": 50,
                    "effect": "heal"
                },
                "epee_acier": {
                    "name": "Épée en acier",
                    "description": "Une épée bien équilibrée au tranchant affûté",
                    "value": 200,
                    "damage": 15
                }
            }
        }
        
        # Créer chaque fichier s'il n'existe pas
        for filename, data in basic_data.items():
            file_path = os.path.join(data_dir, filename)
            if not os.path.exists(file_path):
                logger.info(f"Création du fichier de données {filename}...")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_game_data(self):
        """Charge les données du jeu depuis les fichiers JSON avec gestion d'erreur robuste"""
        try:
            data_dir = os.path.join(project_path, "data")
            
            # Créer le dossier data s'il n'existe pas
            if not os.path.exists(data_dir):
                logger.info("Création du dossier data...")
                os.makedirs(data_dir)
            
            # Liste des fichiers de données à charger
            data_files = [
                "locations.json", 
                "npcs.json", 
                "items.json", 
                "skills.json",
                "quests.json", 
                "combat.json",
                "interactions.json",
                "events.json",
                "progression.json",
                "mature.json"
            ]
            
            # Charger chaque fichier
            for filename in data_files:
                file_path = os.path.join(data_dir, filename)
                name = filename.split(".")[0]  # Enlève l'extension
                
                if not os.path.exists(file_path):
                    logger.warning(f"⚠️ Le fichier {filename} n'existe pas.")
                    setattr(self, f"{name}_data", {})
                    continue
                
                try:
                    # Vérifier le contenu du fichier
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        
                    if not content:
                        logger.warning(f"⚠️ Le fichier {filename} est vide.")
                        setattr(self, f"{name}_data", {})
                        continue
                        
                    # Parser le JSON avec gestion d'erreur
                    try:
                        data = json.loads(content)
                        setattr(self, f"{name}_data", data)
                        logger.info(f"✅ Données {name} chargées.")
                    except json.JSONDecodeError as e:
                        logger.error(f"❌ Erreur JSON dans {filename}: {e}")
                        logger.debug(f"   Début du fichier: {repr(content[:50])}")
                        # Créer un dictionnaire vide pour éviter les erreurs plus tard
                        setattr(self, f"{name}_data", {})
                        
                except Exception as e:
                    logger.error(f"❌ Erreur lors du chargement de {filename}: {e}")
                    setattr(self, f"{name}_data", {})
            
            logger.info("Chargement des données terminé.")
        except Exception as e:
            logger.error(f"❌ Erreur générale lors du chargement des données: {e}")
# Fin BLOC 4: Méthodes de gestion des données du jeu

# BLOC 5: Menu Principal et Navigation
    def start(self):
        """Démarre le jeu"""
        self._display_welcome()
        self.main_menu()
    
    def _display_welcome(self):
        """Affiche le message de bienvenue"""
        print("\n" + "="*30)
        print("===== MUSKO TENSEI RP =====")
        print(f"Version: {self.version}")
        print("="*30 + "\n")
        time.sleep(0.5)
    
    def main_menu(self):
        """Affiche le menu principal"""
        while True:
            print("\n" + "-"*15 + " MENU " + "-"*15)
            print("1. Nouvelle partie")
            print("2. Charger une partie")
            print("3. Options")
            print("4. Quitter")
            print("-"*36)
            
            choice = input("\nVotre choix: ")
            
            if choice == "1":
                self.new_game()
                return  # Quitte le menu après avoir démarré une nouvelle partie
            elif choice == "2":
                self.load_saved_game()
            elif choice == "3":
                self.show_options()
            elif choice == "4":
                self.quit_game()
                return  # Quitte le menu après avoir choisi de quitter
            else:
                print("Choix invalide. Veuillez réessayer.")
    
    def new_game(self):
        """Démarre une nouvelle partie avec une expérience narrative immersive"""
        logger.info("\nDémarrage d'une nouvelle partie...")
        
        try:
            # Demander le nom du joueur
            name = input("\nComment vous appelez-vous, aventurier? ")
            self.player["name"] = name if name.strip() else "Aventurier"
            
            print(f"\nBienvenue, {self.player['name']}!")
            
            # Personnalisation avancée du personnage
            self._character_customization()
            
            # Générer une introduction narrative avec l'IA
            try:
                introduction_context = {
                    "interaction_type": "introduction",
                    "player_name": self.player["name"],
                    "player_class": self.player.get("class", "aventurier"),
                    "player_race": self.player.get("race", "humain"),
                    "player_background": self.player.get("background", "mystérieux"),
                    "world_setting": "Musko Tensei",
                    "narrative_style": self.ai_manager.narrative_style
                }
                
                introduction_prompt = (
                    f"Crée une introduction épique et immersive pour {self.player['name']}, "
                    f"un {self.player.get('race', 'humain')} {self.player.get('class', 'aventurier')} "
                    f"au passé {self.player.get('background', 'mystérieux')} "
                    f"débutant son voyage dans le monde magique de Musko Tensei. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower() if 'hair' in self.player['appearance'] else 'peu ou pas de cheveux'}, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
                
                print("\nCréation de votre histoire personnalisée...")
                # Appel à l'IA pour générer l'introduction
                introduction_text = self.ai_manager.generate_response(introduction_prompt, introduction_context)
                
                # Afficher l'introduction générée par l'IA
                print("\n" + "="*70)
                print(introduction_text)
                print("="*70 + "\n")
                
                # Pause dramatique
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Erreur lors de la génération de l'introduction: {e}")
                print("\nVotre aventure commence maintenant...\n")
            
            # Démarrage du jeu
            self.game_loop()
            
        except Exception as e:
            logger.error(f"\n❌ Erreur lors du démarrage de la partie: {e}")
            import traceback
            traceback.print_exc()
            input("Appuyez sur Entrée pour continuer...")
    
    def show_options(self):
        """Affiche le menu des options"""
        while True:
            print("\n" + "-"*15 + " OPTIONS " + "-"*15)
            print("1. Réglages d'affichage")
            print("2. Options de jeu")
            print("3. Style narratif")
            print("4. Retour au menu principal")
            print("-"*40)
            
            choice = input("\nVotre choix: ")
            
            if choice == "1":
                print("\nFonctionnalité en développement.")
            elif choice == "2":
                print("\nFonctionnalité en développement.")
            elif choice == "3":
                self._adjust_narrative_style()
            elif choice == "4":
                return
            else:
                print("Choix invalide. Veuillez réessayer.")
                
    def _adjust_narrative_style(self):
        """Permet d'ajuster le style narratif de l'IA"""
        print("\nAjustement du style narratif de l'IA...")
        
        try:
            current_style = self.ai_manager.narrative_style
            
            print("\nStyle narratif actuel:")
            for key, value in current_style.items():
                if isinstance(value, float):
                    print(f"{key}: {value:.1f} (0.0-1.0)")
                else:
                    print(f"{key}: {value}")
            
            print("\nChoisissez l'élément à ajuster:")
            print("1. Niveau de détail descriptif")
            print("2. Immersion sensorielle")
            print("3. Qualité des dialogues")
            print("4. Ton émotionnel")
            print("5. Retour")
            
            choice = input("\nVotre choix: ")
            
            if choice == "1":
                value = self._get_float_input("Niveau de détail (0.0-1.0): ", 0.0, 1.0)
                self.ai_manager.narrative_style["descriptive_detail"] = value
            elif choice == "2":
                value = self._get_float_input("Niveau d'immersion sensorielle (0.0-1.0): ", 0.0, 1.0)
                self.ai_manager.narrative_style["sensory_immersion"] = value
            elif choice == "3":
                value = self._get_float_input("Qualité des dialogues (0.0-1.0): ", 0.0, 1.0)
                self.ai_manager.narrative_style["dialogue_quality"] = value
            elif choice == "4":
                print("\nChoisissez le ton émotionnel:")
                tones = ["balanced", "positive", "negative", "intense", "gentle", "mysterious"]
                for i, tone in enumerate(tones):
                    print(f"{i+1}. {tone}")
                
                tone_choice = self._get_numeric_choice(1, len(tones)) - 1
                self.ai_manager.narrative_style["emotional_tone"] = tones[tone_choice]
            elif choice == "5":
                return
            else:
                print("Choix invalide.")
                
            logger.info("\nStyle narratif mis à jour.")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajustement du style narratif: {e}")
# Fin BLOC 5: Menu Principal et Navigation

# BLOC 6: Création de Personnage - Partie 1 (Apparence)
    def _character_customization(self):
        """Système de personnalisation avancée et adaptative"""
        print("\n" + "="*60)
        print("CRÉATION DE PERSONNAGE".center(60))
        print("="*60)
        
        try:
            # Au lieu d'utiliser l'IA pour présenter le système, utiliser un texte prédéfini
            intro_text = (
                "Bienvenue dans le système de création de personnage de MUSKO TENSEI RP.\n"
                "Vous allez pouvoir créer un personnage qui évoluera naturellement au fil de son aventure.\n"
                "Choisissez un point de départ, et votre personnage se développera en fonction de vos actions.\n"
                "À tout moment, vous pouvez choisir l'option '0' pour une sélection aléatoire.\n"
            )
            print(f"\n{intro_text}\n")
            
            # --- APPARENCE PHYSIQUE ET ÂGE ---
            print("\n" + "-"*60)
            print("APPARENCE PHYSIQUE ET ÂGE".center(60))
            print("-"*60)
            
            self.player["appearance"] = {}
            
            # Corriger l'affichage des noms de races
            correct_race_names = {
                "Human Race": "Humain",
                "Elf Race": "Elfe",
                "High Elf Race": "Haut Elfe",
                "Dwarf Race": "Nain",
                "Halfling Race": "Halfelin",
                "Dragon Tribe": "Dragon",
                "Migurd Race": "Migurd",
                "Superd Race": "Superd",
                "Immortal Demon Race": "Démon Immortel",
                "Ogre Race": "Ogre",
                "Beast Race": "Bête",
                "Heaven Race": "Céleste",
                "Sea Race": "Marin",
                "Mixed-Blood Race": "Sang-Mêlé",
                "Cursed Children": "Enfant Maudit",
                "Elemental Spirits": "Esprit Élémentaire",
                "Sylphs": "Sylphe",
                "Ancient Races": "Ancien"
            }
            
            # Utiliser les races de l'AI Manager avec les noms corrects
            races = self.ai_manager.available_races
            print("\nChoisissez votre race:")
            print("0. Aléatoire")
            for i, race in enumerate(races):
                display_name = correct_race_names.get(race, race)
                print(f"{i+1}. {display_name}")
            
            race_choice = self._get_numeric_choice(0, len(races))
            if race_choice == 0:
                chosen_race = random.choice(races)
                self.player["race"] = chosen_race
                display_name = correct_race_names.get(chosen_race, chosen_race)
                print(f"Race choisie aléatoirement: {display_name}")
            else:
                self.player["race"] = races[race_choice-1]
                display_name = correct_race_names.get(self.player["race"], self.player["race"])
                print(f"Race choisie: {display_name}")
            
            # Description de la race
            if self.player["race"] in self.ai_manager.race_descriptions:
                race_description = self.ai_manager.race_descriptions[self.player["race"]]
                print(f"\n{race_description}")
            else:
                print(f"\nLa race {correct_race_names.get(self.player['race'], self.player['race'])} est une race fascinante du monde de Musko Tensei.")
            
            # Système d'âge adaptatif
            ages = ["Aléatoire", "Nourrisson (0-2 ans)", "Enfant (3-12 ans)", "Adolescent (13-17 ans)", 
                    "Jeune adulte (18-25 ans)", "Adulte (26-40 ans)", "Mûr (41-60 ans)", "Ancien (61+ ans)"]
            print("\nChoisissez votre âge de départ:")
            for i, age in enumerate(ages):
                print(f"{i}. {age}")
            
            age_choice = self._get_numeric_choice(0, 7)
            if age_choice == 0:
                age_choice = random.randint(1, 7)
                print(f"Catégorie d'âge choisie aléatoirement: {ages[age_choice]}")
            
            # Définir l'âge numérique en fonction du choix
            age_ranges = [(0, 2), (3, 12), (13, 17), (18, 25), (26, 40), (41, 60), (61, 90)]
            age_range = age_ranges[age_choice-1]
            
            # Permettre à l'utilisateur de choisir un âge spécifique dans la plage
            print(f"\nVous avez choisi la catégorie: {ages[age_choice]}")

            # Cas spécial pour les nourrissons (0-2 ans)
            if age_range == (0, 2):
                print(f"Vous pouvez maintenant choisir un âge spécifique entre {age_range[0]} et {age_range[1]} ans.")
                print("Entrez l'âge souhaité, ou 3 pour un âge aléatoire dans cette plage:")
                specific_age_choice = self._get_numeric_choice(0, 3)
                if specific_age_choice == 3:
                    actual_age = random.randint(age_range[0], age_range[1])
                    print(f"Âge choisi aléatoirement: {actual_age} ans")
                else:
                    actual_age = specific_age_choice
                    print(f"Âge spécifique: {actual_age} ans")
            else:
                print(f"Vous pouvez maintenant choisir un âge spécifique entre {age_range[0]} et {age_range[1]} ans.")
                print("Entrez l'âge souhaité, ou 0 pour un âge aléatoire dans cette plage:")
                specific_age_choice = self._get_numeric_choice(0, 999)
                if specific_age_choice == 0:
                    actual_age = random.randint(age_range[0], age_range[1])
                    print(f"Âge choisi aléatoirement: {actual_age} ans")
                elif specific_age_choice < age_range[0] or specific_age_choice > age_range[1]:
                    print(f"L'âge choisi est en dehors de la plage recommandée. Ajustement à un âge valide...")
                    actual_age = max(age_range[0], min(specific_age_choice, age_range[1]))
                    print(f"Âge ajusté: {actual_age} ans")
                else:
                    actual_age = specific_age_choice
                    print(f"Âge spécifique: {actual_age} ans")
            
            self.player["age"] = actual_age
            self.player["age_category"] = age_choice
            
            # Genre avec option aléatoire
            genders = ["Aléatoire", "Homme", "Femme", "Autre"]
            print("\nChoisissez votre genre:")
            for i, gender in enumerate(genders):
                print(f"{i}. {gender}")
                
            gender_choice = self._get_numeric_choice(0, 3)
            if gender_choice == 0:
                gender_choice = random.randint(1, 3)
                print(f"Genre choisi aléatoirement: {genders[gender_choice]}")
                
            self.player["appearance"]["gender"] = genders[gender_choice]
            
            # Adapter la taille selon l'âge et la race
            height_by_age_race = self._get_height_by_age_race(actual_age, self.player["race"], self.player["appearance"]["gender"])
            
            height_base = height_by_age_race["base"]
            height_min = height_by_age_race["min"]
            height_max = height_by_age_race["max"]
            
            print(f"\nTaille moyenne pour votre âge, race et genre: {height_base}cm (entre {height_min}cm et {height_max}cm)")
            print("Entrez votre taille en cm (ou 0 pour aléatoire):")
            
            height_choice = self._get_numeric_choice(0, 300)
            if height_choice == 0:
                height_choice = random.randint(height_min, height_max)
                print(f"Taille choisie aléatoirement: {height_choice}cm")
            elif height_choice < height_min or height_choice > height_max:
                print(f"La taille choisie n'est pas typique pour votre race et âge. Elle pourrait être exceptionnelle.")
                
            self.player["appearance"]["height"] = f"{height_choice}cm"
# Fin BLOC 6: Création de Personnage - Partie 1 (Apparence)

# BLOC 7: Création de Personnage - Partie 2 (Apparence suite)
            # Corpulence avec option aléatoire
            builds = ["Aléatoire", "Mince", "Athlétique", "Robuste", "Trapu", "Corpulent"]
            if self.player["age"] < 3:
                # Pour les nourrissons, limiter les options
                builds = ["Aléatoire", "Petit", "Normal", "Potelé"]
            elif self.player["age"] < 13:
                # Pour les enfants, adapter les options
                builds = ["Aléatoire", "Mince", "Normal", "Robuste", "Potelé"]
            
            print("\nChoisissez votre corpulence:")
            for i, build in enumerate(builds):
                print(f"{i}. {build}")
            
            build_choice = self._get_numeric_choice(0, len(builds)-1)
            if build_choice == 0:
                build_choice = random.randint(1, len(builds)-1)
                print(f"Corpulence choisie aléatoirement: {builds[build_choice]}")
                
            self.player["appearance"]["build"] = builds[build_choice]
            
            # Couleur de peau adaptée à la race
            skin_colors = self._get_skin_colors_by_race(self.player["race"])
            print("\nChoisissez votre couleur de peau:")
            print("0. Aléatoire")
            for i, color in enumerate(skin_colors):
                print(f"{i+1}. {color}")
                
            skin_choice = self._get_numeric_choice(0, len(skin_colors))
            if skin_choice == 0:
                skin_choice = random.randint(1, len(skin_colors))
                print(f"Couleur de peau choisie aléatoirement: {skin_colors[skin_choice-1]}")
                
            self.player["appearance"]["skin"] = skin_colors[skin_choice-1] if skin_choice > 0 else random.choice(skin_colors)
            
            # Cheveux adaptés à l'âge et la race
            if self.player["age"] < 1:
                # Pour les bébés, moins d'options
                hair_options = "Peu ou pas de cheveux"
                self.player["appearance"]["hair"] = hair_options
                print(f"\nCheveux: {hair_options} (typique pour un nourrisson)")
            else:
                hair_colors = self._get_hair_colors_by_race(self.player["race"])
                print("\nChoisissez votre couleur de cheveux:")
                print("0. Aléatoire")
                for i, color in enumerate(hair_colors):
                    print(f"{i+1}. {color}")
                    
                hair_color_choice = self._get_numeric_choice(0, len(hair_colors))
                if hair_color_choice == 0:
                    hair_color_choice = random.randint(1, len(hair_colors))
                    print(f"Couleur de cheveux choisie aléatoirement: {hair_colors[hair_color_choice-1]}")
                    
                hair_color = hair_colors[hair_color_choice-1] if hair_color_choice > 0 else random.choice(hair_colors)
                
                hair_styles = ["courts", "mi-longs", "longs", "ondulés", "bouclés", "tressés", "rasés sur les côtés"]
                print("\nChoisissez votre style de cheveux:")
                print("0. Aléatoire")
                for i, style in enumerate(hair_styles):
                    print(f"{i+1}. {style}")
                    
                hair_style_choice = self._get_numeric_choice(0, len(hair_styles))
                if hair_style_choice == 0:
                    hair_style_choice = random.randint(1, len(hair_styles))
                    print(f"Style de cheveux choisi aléatoirement: {hair_styles[hair_style_choice-1]}")
                    
                hair_style = hair_styles[hair_style_choice-1] if hair_style_choice > 0 else random.choice(hair_styles)
                
                self.player["appearance"]["hair"] = f"{hair_color}, {hair_style}"
            
            # Yeux adaptés à la race
            eye_colors = self._get_eye_colors_by_race(self.player["race"])
            print("\nChoisissez votre couleur d'yeux:")
            print("0. Aléatoire")
            for i, color in enumerate(eye_colors):
                print(f"{i+1}. {color}")
                
            eye_choice = self._get_numeric_choice(0, len(eye_colors))
            if eye_choice == 0:
                eye_choice = random.randint(1, len(eye_colors))
                print(f"Couleur d'yeux choisie aléatoirement: {eye_colors[eye_choice-1]}")
                
            self.player["appearance"]["eyes"] = eye_colors[eye_choice-1] if eye_choice > 0 else random.choice(eye_colors)
            
            # Signes distinctifs (optionnel)
            distinctive_marks = ["Aucun", "Cicatrice au visage", "Taches de rousseur", "Grain de beauté", "Tatouage discret", 
                                "Marque de naissance", "Hétérochromie", "Tache de vin", "Mèche de couleur distinctive"]
            print("\nChoisissez un signe distinctif (ou 0 pour aléatoire):")
            print("0. Aléatoire")
            for i, mark in enumerate(distinctive_marks):
                print(f"{i+1}. {mark}")
                
            mark_choice = self._get_numeric_choice(0, len(distinctive_marks))
            if mark_choice == 0:
                mark_choice = random.randint(1, len(distinctive_marks))
                print(f"Signe distinctif choisi aléatoirement: {distinctive_marks[mark_choice-1]}")
                
            self.player["appearance"]["distinctive"] = distinctive_marks[mark_choice-1] if mark_choice > 0 else random.choice(distinctive_marks)
# Fin BLOC 7: Création de Personnage - Partie 2 (Apparence suite)

# BLOC 8: Création de Personnage - Partie 3 (Description et Origine)
            # Génération d'une description physique basée sur les choix
            race_display_name = correct_race_names.get(self.player["race"], self.player["race"])
            
            if self.player["age"] < 3:
                appearance_text = (
                    f"Vous êtes {self.player['name']}, un {race_display_name} {self.player['appearance']['gender']} "
                    f"de {self.player['age']} an{'s' if self.player['age'] > 1 else ''}. Un nourrisson {self.player['appearance']['build'].lower()} "
                    f"avec des yeux {self.player['appearance']['eyes'].lower()}. "
                    f"Votre peau est {self.player['appearance']['skin'].lower()}"
                    f"{', et vous avez ' + self.player['appearance']['distinctive'].lower() if self.player['appearance']['distinctive'] != 'Aucun' else '.'}"
                )
            else:
                appearance_text = (
                    f"Vous êtes {self.player['name']}, un {race_display_name} {self.player['appearance']['gender']} "
                    f"de {self.player['age']} ans. Avec votre silhouette {self.player['appearance']['build'].lower()} "
                    f"de {self.player['appearance']['height']}, votre peau {self.player['appearance']['skin'].lower()}, "
                    f"vos yeux {self.player['appearance']['eyes'].lower()} et vos cheveux {self.player['appearance']['hair'].lower()}, "
                    f"vous vous distinguez par {self.player['appearance']['distinctive'].lower()}."
                )
            
            print(f"\nVotre apparence: {appearance_text}")
            self.player["appearance_description"] = appearance_text
            
            # --- ORIGINE ET FAMILLE ---
            if self.player["age"] < 18:
                print("\n" + "-"*60)
                print("ORIGINE ET FAMILLE".center(60))
                print("-"*60)
                
                family_backgrounds = [
                    "Aléatoire",
                    "Famille noble",
                    "Famille marchande",
                    "Famille paysanne",
                    "Famille artisane",
                    "Famille de guerriers",
                    "Famille de mages",
                    "Famille nomade",
                    "Orphelin",
                    "Adopté",
                    "Famille religieuse",
                    "Famille de serviteurs"
                ]
                
                print("\nDans quelle famille êtes-vous né?")
                for i, bg in enumerate(family_backgrounds):
                    print(f"{i}. {bg}")
                
                bg_choice = self._get_numeric_choice(0, len(family_backgrounds)-1)
                if bg_choice == 0:
                    bg_choice = random.randint(1, len(family_backgrounds)-1)
                    print(f"Origine familiale choisie aléatoirement: {family_backgrounds[bg_choice]}")
                
                self.player["family_background"] = family_backgrounds[bg_choice]
                
                # Talents naturels pour les jeunes personnages
                print("\nChoisissez vos talents naturels (choisissez-en jusqu'à 3, ou 0 pour aléatoire):")
                natural_talents = [
                    "Affinité magique", "Force physique", "Agilité naturelle", "Mémoire exceptionnelle", 
                    "Charisme naturel", "Résistance accrue", "Sens aiguisés", "Intelligence vive",
                    "Instinct de survie", "Adresse manuelle", "Voix mélodieuse", "Sang royal"
                ]
                
                print("0. Aléatoire")
                for i, talent in enumerate(natural_talents):
                    print(f"{i+1}. {talent}")
                
                talents_selected = []
                talent_choice = self._get_numeric_choice(0, len(natural_talents))
                
                if talent_choice == 0:
                    # Sélection aléatoire de 1-3 talents
                    num_talents = random.randint(1, 3)
                    talents_selected = random.sample(natural_talents, num_talents)
                    print(f"Talents choisis aléatoirement: {', '.join(talents_selected)}")
                else:
                    talents_selected.append(natural_talents[talent_choice-1])
                    
                    # Option pour choisir jusqu'à 2 talents supplémentaires
                    for i in range(2):
                        print(f"\nSouhaitez-vous sélectionner un {i+2}e talent? (0: Non, 1-{len(natural_talents)}: Oui)")
                        talent_choice = self._get_numeric_choice(0, len(natural_talents))
                        if talent_choice == 0:
                            break
                        talents_selected.append(natural_talents[talent_choice-1])
                
                self.player["natural_talents"] = talents_selected
# Fin BLOC 8: Création de Personnage - Partie 3 (Description et Origine)

# BLOC 9: Création de Personnage - Partie 4 (Capacités et Orientation)
            # --- CAPACITÉS ET ORIENTATION ---
            # Adapté selon l'âge - pour les très jeunes, pas de classe fixe
            if self.player["age"] >= 12:
                print("\n" + "-"*60)
                print("CAPACITÉS ET ORIENTATION".center(60))
                print("-"*60)
                
                # Classes disponibles - maintenant avec plus d'options
                classes = [
                    "Aléatoire",
                    "Sans classe (développement libre)",
                    "Guerrier",
                    "Mage",
                    "Rôdeur",
                    "Clerc",
                    "Assassin",
                    "Barde",
                    "Alchimiste",
                    "Samouraï",
                    "Moine",
                    "Invocateur",
                    "Paladin",
                    "Druide",
                    "Nécromancien",
                    "Artificier",
                    "Mystique",
                    "Chevalier Dragon",
                    "Voleur",
                    "Maître d'armes",
                    "Érudit"
                ]
                
                print("\nChoisissez votre orientation (non définitive):")
                for i, class_option in enumerate(classes):
                    print(f"{i}. {class_option}")
                
                class_choice = self._get_numeric_choice(0, len(classes)-1)
                if class_choice == 0:
                    class_choice = random.randint(1, len(classes)-1)
                    print(f"Orientation choisie aléatoirement: {classes[class_choice]}")
                    
                self.player["class"] = classes[class_choice]
                
                # Compétences initiales - Permettre plusieurs choix sans restrictions de spécialisation
                if self.player["class"] != "Sans classe (développement libre)":
                    print("\nVous commencez avec quelques compétences de base liées à votre orientation.")
                    print("Par la suite, vous pourrez apprendre des compétences de toutes les orientations.")
                    
                    initial_skills = self._get_initial_skills(self.player["class"], self.player["race"])
                    
                    print("\nCompétences initiales:")
                    for skill in initial_skills:
                        print(f"- {skill}")
                    
                    self.player["skills"] = initial_skills
                else:
                    print("\nVous avez choisi de ne pas vous spécialiser pour l'instant.")
                    print("Vous pourrez développer librement vos compétences au fil de l'aventure.")
                    self.player["skills"] = ["Survie basique", "Communication", "Observation", "Gestion du mana", "Récupération"]
            else:
                # Pour les très jeunes, pas de classe fixe mais des prédispositions
                print("\nEn raison de votre jeune âge, vous n'avez pas encore d'orientation définie.")
                print("Vous développerez vos talents et compétences au fil de l'aventure.")
                
                self.player["class"] = "Enfant"
                self.player["skills"] = ["Curiosité", "Jeux", "Observation basique", "Récupération naturelle"]
                
                if self.player["age"] >= 6:
                    self.player["skills"].append("Apprentissage")
                    if "Affinité magique" in self.player.get("natural_talents", []):
                        self.player["skills"].append("Étincelles magiques")
# Fin BLOC 9: Création de Personnage - Partie 4 (Capacités et Orientation)

# BLOC 10: Création de Personnage - Partie 5 (Attributs)
            # --- ATTRIBUTS ET COMPÉTENCES ---
            print("\n" + "-"*60)
            print("ATTRIBUTS DE BASE".center(60))
            print("-"*60)
            
            # Présenter toutes les statistiques avant leur attribution
            print("\nVoici les statistiques sur lesquelles vous allez répartir vos points:")
            print("- Force: Détermine votre puissance physique, capacité à porter des objets lourds et dégâts au corps à corps")
            print("- Intelligence: Détermine votre capacité à apprendre, puissance magique et compréhension du monde")
            print("- Dextérité: Détermine votre agilité, précision, vitesse et capacité à éviter les attaques")
            print("- Constitution: Détermine votre santé, endurance et résistance aux maladies et poisons")
            print("- Sagesse: Détermine votre intuition, perception et connexion avec le monde spirituel")
            print("- Charisme: Détermine votre capacité à influencer les autres et à résister aux influences sociales")
            print("- Mana: Détermine votre réserve d'énergie magique (sera calculée en fonction de l'Intelligence et de la Sagesse)")
            print("- Endurance: Détermine votre capacité à effectuer des actions physiques (sera calculée en fonction de la Constitution)")
            print("- Chance: Détermine la probabilité d'événements favorables (sera partiellement aléatoire)")
            
            # Points d'attributs adaptés selon l'âge
            # Formule : 10 points de base + âge/2 points supplémentaires (plafonné à 40)
            attribute_points = min(40, 10 + int(self.player["age"]/2))
            
            self.player["stats"] = {}
            print(f"\nDistribuez vos points de caractéristiques (total: {attribute_points} points):")
            print("Ces valeurs représentent votre potentiel et vos prédispositions naturelles.")
            attributes = ["Force", "Intelligence", "Dextérité", "Constitution", "Sagesse", "Charisme"]
            
            # Appliquer des modificateurs selon l'âge
            age_modifiers = self._get_age_attribute_modifiers(self.player["age"])
            race_modifiers = self._get_race_attribute_modifiers(self.player["race"])
            
            print("\nModificateurs d'attributs liés à votre âge:")
            for attr, mod in age_modifiers.items():
                mod_text = f"+{mod}" if mod >= 0 else str(mod)
                print(f"{attr}: {mod_text}")
                
            print("\nModificateurs d'attributs liés à votre race:")
            for attr, mod in race_modifiers.items():
                mod_text = f"+{mod}" if mod >= 0 else str(mod)
                print(f"{attr}: {mod_text}")
            
            # Distribution automatique des points pour les très jeunes
            if self.player["age"] < 6:
                print("\nEn raison de votre très jeune âge, vos attributs sont définis automatiquement.")
                
                # Attributs de base pour les très jeunes
                base_stats = {
                    "force": 3,
                    "intelligence": 3,
                    "dexterite": 3,
                    "constitution": 4,
                    "sagesse": 2,
                    "charisme": 5  # Les bébés sont mignons!
                }
                
                # Appliquer les modificateurs
                for attr, value in base_stats.items():
                    attr_cap = attr.capitalize()
                    total = value + age_modifiers.get(attr_cap, 0) + race_modifiers.get(attr_cap, 0)
                    self.player["stats"][attr] = max(1, total)  # Minimum 1
                    print(f"{attr_cap}: {self.player['stats'][attr]}")
                    
            else:
                remaining_points = attribute_points
                for attr in attributes:
                    attr_lower = attr.lower()
                    
                    # Points minimums et maximums adaptés à l'âge
                    min_points = 1
                    max_points = min(15, self.player["age"])
                    
                    print(f"\n{attr} (entre {min_points} et {max_points}, {remaining_points} points restants)")
                    print("0. Attribuer automatiquement les points restants")
                    
                    attr_choice = self._get_numeric_choice(0, max_points)
                    
                    if attr_choice == 0:
                        # Distribuer les points restants automatiquement entre les attributs
                        remaining_attrs = len(attributes) - attributes.index(attr)
                        points_per_attr = max(1, remaining_points // remaining_attrs)
                        
                        for remaining_attr in attributes[attributes.index(attr):]:
                            remaining_attr_lower = remaining_attr.lower()
                            points = min(points_per_attr, remaining_points)
                            
                            # Appliquer les modificateurs
                            total = points + age_modifiers.get(remaining_attr, 0) + race_modifiers.get(remaining_attr, 0)
                            self.player["stats"][remaining_attr_lower] = max(1, total)  # Minimum 1
                            
                            print(f"{remaining_attr}: {self.player['stats'][remaining_attr_lower]}")
                            remaining_points -= points
                        
                        break
                    else:
                        # Appliquer les modificateurs
                        total = attr_choice + age_modifiers.get(attr, 0) + race_modifiers.get(attr, 0)
                        self.player["stats"][attr_lower] = max(1, total)  # Minimum 1
                        remaining_points -= attr_choice
                    
                    if remaining_points <= 0:
                        break
# Fin BLOC 10: Création de Personnage - Partie 5 (Attributs)

# BLOC 11: Création de Personnage - Partie 6 (Statistiques dérivées et résumé)
            # Calculer les statistiques dérivées
            # Mana = (Intelligence x 5) + (Sagesse x 3) + modificateur racial
            intelligence = self.player["stats"].get("intelligence", 3)
            sagesse = self.player["stats"].get("sagesse", 3)
            race_mana_bonus = 0
            
            # Bonus de mana raciaux
            if self.player["race"] in ["High Elf Race", "Elf Race", "Migurd Race", "Heaven Race", "Elemental Spirits"]:
                race_mana_bonus = 20
            elif self.player["race"] in ["Human Race", "Mixed-Blood Race"]:
                race_mana_bonus = 10
                
            self.player["stats"]["mana"] = (intelligence * 5) + (sagesse * 3) + race_mana_bonus
            
            # Endurance = Constitution x 10 + modificateur racial
            constitution = self.player["stats"].get("constitution", 3)
            race_endurance_bonus = 0
            
            # Bonus d'endurance raciaux
            if self.player["race"] in ["Dwarf Race", "Ogre Race", "Superd Race"]:
                race_endurance_bonus = 20
            elif self.player["race"] in ["Beast Race", "Immortal Demon Race"]:
                race_endurance_bonus = 15
                
            self.player["stats"]["endurance"] = (constitution * 10) + race_endurance_bonus
            
            # Chance = Base aléatoire (3-18) + modificateur racial
            base_chance = random.randint(3, 18)
            race_chance_bonus = 0
            
            # Bonus de chance raciaux
            if self.player["race"] in ["Halfling Race", "Sylphs"]:
                race_chance_bonus = 5
                
            self.player["stats"]["chance"] = base_chance + race_chance_bonus
            
            # Afficher les statistiques dérivées
            print("\nStatistiques dérivées calculées automatiquement:")
            print(f"Mana: {self.player['stats']['mana']} points")
            print(f"Endurance: {self.player['stats']['endurance']} points")
            print(f"Chance: {self.player['stats']['chance']} (partiellement aléatoire)")
            
            # --- RÉSUMÉ FINAL PAR L'IA ---
            print("\nCréation de votre résumé de personnage...")
            
            # Obtenir le nom d'affichage de la race
            race_display_name = correct_race_names.get(self.player["race"], self.player["race"])
            
            summary_context = {
                "interaction_type": "character_summary",
                "player_data": self.player
            }
            
            # Adapte le prompt selon l'âge du personnage
            if self.player["age"] < 3:
                summary_prompt = (
                    f"Crée un résumé immersif et captivant d'un nourrisson nommé {self.player['name']}, "
                    f"un {race_display_name} âgé de {self.player['age']} an{'s' if self.player['age'] > 1 else ''}. "
                    f"Il est né dans une {self.player.get('family_background', 'famille ordinaire')}. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance'].get('hair', 'peu ou pas de cheveux').lower() if 'hair' in self.player['appearance'] else 'peu ou pas de cheveux'}, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"Le résumé doit être écrit à la deuxième personne du singulier, s'adressant au joueur comme si "
                    f"c'était un nouveau-né qui commence sa vie dans le monde fascinant de Musko Tensei. "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
            elif self.player["age"] < 13:
                summary_prompt = (
                    f"Crée un résumé immersif et captivant d'un enfant nommé {self.player['name']}, "
                    f"un {race_display_name} de {self.player['age']} ans issu d'une {self.player.get('family_background', 'famille ordinaire')}. "
                    f"Intègre son apparence physique enfantine et ses traits de caractère en développement. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower() if 'hair' in self.player['appearance'] else 'peu ou pas de cheveux'}, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"Évoque ses talents naturels ({', '.join(self.player.get('natural_talents', ['curiosité']))}) et son environnement familial. "
                    f"Le résumé doit être écrit à la deuxième personne du singulier, s'adressant au joueur comme si "
                    f"c'était un enfant qui découvre le monde fascinant de Musko Tensei. "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
            elif self.player["age"] < 18:
                summary_prompt = (
                    f"Crée un résumé immersif et captivant d'un adolescent nommé {self.player['name']}, "
                    f"un {race_display_name} de {self.player['age']} ans issu d'une {self.player.get('family_background', 'famille ordinaire')}, "
                    f"qui commence à s'intéresser à la voie du {self.player.get('class', 'voyageur')}. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower() if 'hair' in self.player['appearance'] else 'peu ou pas de cheveux'}, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"Intègre son apparence physique, ses talents naturels ({', '.join(self.player.get('natural_talents', ['détermination']))}) "
                    f"et ses premières compétences ({', '.join(self.player.get('skills', ['débrouillardise']))}). "
                    f"Le résumé doit être écrit à la deuxième personne du singulier, s'adressant directement au joueur. "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
            else:
                summary_prompt = (
                    f"Crée un résumé immersif et captivant du personnage {self.player['name']}, "
                    f"un {race_display_name} de {self.player['age']} ans qui suit la voie du {self.player.get('class', 'voyageur')}. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower() if 'hair' in self.player['appearance'] else 'peu ou pas de cheveux'}, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"Intègre son apparence physique, son passé ({self.player.get('family_background', 'diverses expériences')}), "
                    f"et ses compétences principales ({', '.join(self.player.get('skills', ['voyageur']))}). "
                    f"Le résumé doit être écrit à la deuxième personne du singulier, s'adressant directement au joueur. "
                    f"Mentionne aussi ses statistiques principales (Mana: {self.player['stats'].get('mana')}, "
                    f"Force: {self.player['stats'].get('force')}, Intelligence: {self.player['stats'].get('intelligence')}, "
                    f"Constitution: {self.player['stats'].get('constitution')}). "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
            
            character_summary = self.ai_manager.generate_response(summary_prompt, summary_context)
            
            print("\n" + "="*70)
            print("VOTRE PERSONNAGE".center(70))
            print("="*70)
            print(character_summary)
            print("="*70)
            
            self.player["character_summary"] = character_summary
            
            input("\nAppuyez sur Entrée pour commencer votre aventure...")
            return True
            
        except Exception as e:
            logger.error(f"\n❌ Erreur lors de la création de personnage: {e}")
            import traceback
            traceback.print_exc()
            
            # Créer un personnage par défaut en cas d'erreur
            print("\nCréation d'un personnage par défaut...")
            self.player["race"] = "Human Race"
            self.player["class"] = "Aventurier"
            self.player["age"] = 20
            self.player["stats"] = {"force": 10, "intelligence": 10, "dexterite": 10, "constitution": 10, "sagesse": 10, "charisme": 10}
            return False
# Fin BLOC 11: Création de Personnage - Partie 6 (Statistiques dérivées et résumé)

# BLOC 12: Méthodes Utilitaires pour la Création de Personnage
    def _get_numeric_choice(self, min_value, max_value):
        """Obtient une entrée numérique avec validation"""
        while True:
            try:
                choice = input("Votre choix: ")
                choice_num = int(choice)
                if min_value <= choice_num <= max_value:
                    return choice_num
                else:
                    print(f"Veuillez entrer un nombre entre {min_value} et {max_value}.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
    
    def _get_float_input(self, prompt, min_value, max_value):
        """Obtient une entrée à virgule flottante avec validation"""
        while True:
            try:
                value = float(input(prompt))
                if min_value <= value <= max_value:
                    return value
                else:
                    print(f"Veuillez entrer une valeur entre {min_value} et {max_value}.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
    
    def _get_height_by_age_race(self, age, race, gender):
        """Détermine les plages de taille en fonction de l'âge, la race et le genre"""
        # Taille de base pour un humain adulte
        base_height = 170 if gender == "Homme" else 160
        
        # Modificateurs raciaux
        race_modifiers = {
            "Human Race": 0,
            "Elf Race": 15,  # Plus grands
            "High Elf Race": 20,  # Encore plus grands
            "Dwarf Race": -40,  # Plus petits
            "Halfling Race": -60,  # Très petits
            "Dragon Tribe": 20,
            "Migurd Race": -30,
            "Superd Race": 30,  # Très grands
            "Ogre Race": 50,  # Énormes
            "Beast Race": -10,
            "Heaven Race": 10,
            "Sea Race": 0,
            "Mixed-Blood Race": 0,  # Variable
            "Cursed Children": -5,
            "Elemental Spirits": 0,  # Variable
            "Sylphs": -20,
            "Ancient Races": 10
        }
        
        # Appliquer le modificateur racial
        race_mod = race_modifiers.get(race, 0)
        base_height += race_mod
        
        # Calculer la taille en fonction de l'âge
        if age < 1:  # Nourrisson
            height_base = int(50 + (age * 20))
            min_height = height_base - 5
            max_height = height_base + 5
        elif age < 3:  # Tout-petit
            height_base = int(70 + ((age - 1) * 15))
            min_height = height_base - 7
            max_height = height_base + 7
        elif age < 13:  # Enfant
            height_base = int(85 + ((age - 3) * 8))
            min_height = height_base - 10
            max_height = height_base + 10
        elif age < 18:  # Adolescent
            # Croissance progressive vers la taille adulte
            growth_percentage = (age - 13) / 5.0  # 0 à 1
            height_base = int(135 + ((base_height - 135) * growth_percentage))
            min_height = height_base - 15
            max_height = height_base + 15
        else:  # Adulte
            height_base = base_height
            min_height = int(base_height * 0.9)
            max_height = int(base_height * 1.1)
            
            # Ajustement pour les personnes âgées
            if age > 70:
                height_base -= 5  # Légère diminution de taille
                min_height -= 5
                max_height -= 5
                
        return {
            "base": height_base,
            "min": min_height,
            "max": max_height
        }
    
    def _get_skin_colors_by_race(self, race):
        """Obtient les couleurs de peau appropriées pour une race"""
        # Couleurs de peau par défaut
        default_skin_colors = ["claire", "beige", "hâlée", "mate", "brune", "foncée"]
        
        # Couleurs spécifiques par race
        race_skin_colors = {
            "Human Race": ["claire", "beige", "hâlée", "mate", "brune", "foncée"],
            "Elf Race": ["claire", "ivoire", "olive pâle", "dorée"],
            "High Elf Race": ["ivoire", "albâtre", "nacrée", "argentée"],
            "Dwarf Race": ["claire", "rougeâtre", "bronzée", "terreuse"],
            "Halfling Race": ["beige", "hâlée", "mate"],
            "Dragon Tribe": ["écailleuse rouge", "écailleuse bleue", "écailleuse verte", "écailleuse noire", "écailleuse dorée"],
            "Ogre Race": ["grise", "verdâtre", "brune", "rougeâtre"],
            "Beast Race": ["fourrure blonde", "fourrure brune", "fourrure rousse", "fourrure grise", "fourrure noire", "fourrure tachetée"],
            "Heaven Race": ["dorée", "nacrée", "lumineuse", "argentée"],
            "Sea Race": ["bleutée", "verdâtre", "nacrée", "écailleuse"],
            "Elemental Spirits": ["translucide", "lumineuse", "éthérée", "colorée"]
        }
        
        return race_skin_colors.get(race, default_skin_colors)
    
    def _get_hair_colors_by_race(self, race):
        """Obtient les couleurs de cheveux appropriées pour une race"""
        # Couleurs de cheveux par défaut
        default_hair_colors = ["blonds", "bruns", "noirs", "roux", "châtains"]
        
        # Couleurs spécifiques par race
        race_hair_colors = {
            "Human Race": ["blonds", "bruns", "noirs", "roux", "châtains"],
            "Elf Race": ["blonds", "argentés", "dorés", "cuivrés", "bruns", "noirs"],
            "High Elf Race": ["argentés", "blonds platine", "blancs", "dorés"],
            "Dwarf Race": ["roux", "bruns", "noirs", "gris"],
            "Halfling Race": ["bruns", "roux", "châtains", "blonds"],
            "Dragon Tribe": ["rouges", "bleus", "verts", "dorés", "noirs"],
            "Ogre Race": ["noirs", "gris", "bruns"],
            "Beast Race": ["fourrure colorée"],
            "Heaven Race": ["dorés", "argentés", "blancs", "lumineux"],
            "Sea Race": ["bleus", "verts", "turquoise"],
            "Elemental Spirits": ["flamboyants", "iridescents", "lumineux", "cristallins"]
        }
        
        return race_hair_colors.get(race, default_hair_colors)
    
    def _get_eye_colors_by_race(self, race):
        """Obtient les couleurs d'yeux appropriées pour une race"""
        # Couleurs d'yeux par défaut
        default_eye_colors = ["bleus", "verts", "marron", "noisette", "gris"]
        
        # Couleurs spécifiques par race
        race_eye_colors = {
            "Human Race": ["bleus", "verts", "marron", "noisette", "gris"],
            "Elf Race": ["bleus", "verts", "violets", "dorés", "argentés"],
            "High Elf Race": ["argentés", "bleus cristal", "violets", "dorés"],
            "Dwarf Race": ["marron", "noirs", "gris", "bleus"],
            "Halfling Race": ["marron", "verts", "bleus"],
            "Dragon Tribe": ["dorés", "rouges", "ambrés", "fendus"],
            "Ogre Race": ["rouges", "noirs", "jaunes"],
            "Beast Race": ["dorés", "verts", "ambrés", "fendus"],
            "Heaven Race": ["argentés", "dorés", "blancs", "cristallins"],
            "Sea Race": ["bleus profonds", "verts océan", "turquoise"],
            "Elemental Spirits": ["lumineux", "iridescents", "sans pupille"]
        }
        
        return race_eye_colors.get(race, default_eye_colors)
# Fin BLOC 12: Méthodes Utilitaires pour la Création de Personnage

# BLOC 13: Plus de Méthodes Utilitaires et Initialisation des Systèmes Avancés
    def _get_age_attribute_modifiers(self, age):
        """Obtient les modificateurs d'attributs en fonction de l'âge"""
        if age < 1:  # Nourrisson
            return {
                "Force": -7,
                "Intelligence": -7,
                "Dextérité": -7,
                "Constitution": -5,
                "Sagesse": -7,
                "Charisme": 2  # Les bébés sont mignons
            }
        elif age < 3:  # Tout-petit
            return {
                "Force": -6,
                "Intelligence": -5,
                "Dextérité": -5,
                "Constitution": -4,
                "Sagesse": -5,
                "Charisme": 2
            }
        elif age < 13:  # Enfant
            return {
                "Force": -4,
                "Intelligence": -2,
                "Dextérité": 0,  # Les enfants sont agiles
                "Constitution": -2,
                "Sagesse": -3,
                "Charisme": 1
            }
        elif age < 18:  # Adolescent
            return {
                "Force": -1,
                "Intelligence": 0,
                "Dextérité": 1,
                "Constitution": 0,
                "Sagesse": -1,
                "Charisme": 0
            }
        elif age < 30:  # Jeune adulte
            return {
                "Force": 0,
                "Intelligence": 0,
                "Dextérité": 0,
                "Constitution": 0,
                "Sagesse": 0,
                "Charisme": 0
            }
        elif age < 50:  # Adulte mûr
            return {
                "Force": 0,
                "Intelligence": 1,
                "Dextérité": -1,
                "Constitution": -1,
                "Sagesse": 2,
                "Charisme": 1
            }
        elif age < 70:  # Aîné
            return {
                "Force": -2,
                "Intelligence": 1,
                "Dextérité": -2,
                "Constitution": -2,
                "Sagesse": 3,
                "Charisme": 1
            }
        else:  # Ancien
            return {
                "Force": -3,
                "Intelligence": 1,
                "Dextérité": -3,
                "Constitution": -3,
                "Sagesse": 4,
                "Charisme": 0
            }
    
    def _get_race_attribute_modifiers(self, race):
        """Obtient les modificateurs d'attributs en fonction de la race"""
        race_modifiers = {
            "Human Race": {
                "Force": 0,
                "Intelligence": 0,
                "Dextérité": 0,
                "Constitution": 0,
                "Sagesse": 0,
                "Charisme": 1  # Polyvalence humaine
            },
            "Elf Race": {
                "Force": -1,
                "Intelligence": 1,
                "Dextérité": 2,
                "Constitution": -1,
                "Sagesse": 1,
                "Charisme": 0
            },
            "High Elf Race": {
                "Force": -1,
                "Intelligence": 2,
                "Dextérité": 1,
                "Constitution": -1,
                "Sagesse": 1,
                "Charisme": 1
            },
            "Dwarf Race": {
                "Force": 1,
                "Intelligence": 0,
                "Dextérité": -1,
                "Constitution": 3,
                "Sagesse": 0,
                "Charisme": -1
            },
            "Halfling Race": {
                "Force": -2,
                "Intelligence": 0,
                "Dextérité": 2,
                "Constitution": 0,
                "Sagesse": 0,
                "Charisme": 2
            },
            "Dragon Tribe": {
                "Force": 2,
                "Intelligence": 1,
                "Dextérité": 0,
                "Constitution": 2,
                "Sagesse": 0,
                "Charisme": 1
            },
            "Ogre Race": {
                "Force": 3,
                "Intelligence": -2,
                "Dextérité": -1,
                "Constitution": 3,
                "Sagesse": -2,
                "Charisme": -2
            },
            "Beast Race": {
                "Force": 1,
                "Intelligence": -1,
                "Dextérité": 2,
                "Constitution": 1,
                "Sagesse": 0,
                "Charisme": -1
            }
        }
        
        return race_modifiers.get(race, {
            "Force": 0,
            "Intelligence": 0,
            "Dextérité": 0,
            "Constitution": 0,
            "Sagesse": 0,
            "Charisme": 0
        })
    
    def _get_initial_skills(self, player_class, race):
        """Obtient les compétences initiales en fonction de la classe et de la race"""
        class_skills = {
            "Guerrier": ["Combat à l'épée", "Tactique de combat", "Endurance", "Intimidation"],
            "Mage": ["Canalisation de mana", "Connaissance arcanique", "Concentration", "Détection magique"],
            "Rôdeur": ["Pistage", "Survie", "Archerie", "Connaissance de la nature"],
            "Clerc": ["Prière", "Premiers soins", "Connaissance divine", "Persuasion"],
            "Assassin": ["Discrétion", "Poisons", "Attaque sournoise", "Acrobatie"],
            "Barde": ["Performance", "Charme", "Connaissance", "Inspiration"],
            "Alchimiste": ["Préparation de potions", "Analyse", "Herbologie", "Médecine"],
            "Samouraï": ["Voie du sabre", "Méditation", "Honneur", "Perception"],
            "Moine": ["Arts martiaux", "Méditation profonde", "Endurance corporelle", "Vitesse"],
            "Invocateur": ["Invocation mineure", "Lien spirituel", "Négociation", "Rituel"],
            "Paladin": ["Combat sacré", "Bouclier de foi", "Guérison basique", "Protection"],
            "Druide": ["Communion naturelle", "Forme animale mineure", "Connaissance des plantes", "Apaisement"],
            "Nécromancien": ["Sens des morts", "Énergie noire", "Résistance occulte", "Connaissance interdite"],
            "Artificier": ["Fabrication d'objets", "Compréhension mécanique", "Innovation", "Réparation"],
            "Mystique": ["Vision spirituelle", "Perception extrasensorielle", "Aura", "Méditation"],
            "Chevalier Dragon": ["Affinité draconique", "Combat monté", "Tactique", "Leadership"],
            "Voleur": ["Crochetage", "Discrétion", "Détection des pièges", "Évasion"],
            "Maître d'armes": ["Maîtrise des armes", "Polyvalence", "Style de combat", "Évaluation"],
            "Érudit": ["Connaissance encyclopédique", "Analyse", "Langues", "Concentration"]
        }
        
        # Compétences raciales
        race_skills = {
            "Human Race": ["Adaptabilité"],
            "Elf Race": ["Vision nocturne", "Connexion naturelle"],
            "High Elf Race": ["Affinité arcanique", "Vision nocturne"],
            "Dwarf Race": ["Résistance aux poisons", "Vision dans l'obscurité"],
            "Halfling Race": ["Chance", "Discrétion naturelle"],
            "Dragon Tribe": ["Souffle élémentaire", "Écailles protectrices"],
            "Ogre Race": ["Force brute", "Intimidation naturelle"],
            "Beast Race": ["Sens aiguisés", "Griffes naturelles"]
        }
        
        # Fusionner les compétences de classe et raciales
        skills = class_skills.get(player_class, ["Survie basique", "Communication", "Observation"])
        racial_ability = race_skills.get(race, ["Adaptabilité"])
        
        # Pour les classes "Sans classe", donner plus de compétences générales
        if player_class == "Sans classe (développement libre)":
            return ["Survie", "Communication", "Observation", "Débrouillardise", "Premiers soins", racial_ability[0]]
        
        return skills + racial_ability
    
    def _initialize_advanced_systems(self):
        """Initialise tous les systèmes avancés"""
        # Système de mémoire narrative
        self._initialize_memory_system()
        
        # Système de personnalité
        self._initialize_personality_system()
        
        # Système de progression de compétences
        self._initialize_skill_progression_system()
        
        # Système de santé et bien-être
        self._initialize_health_system()
        
        # Système d'inventaire avancé
        self._initialize_enhanced_inventory()
        
        # Système d'économie
        self._initialize_economy_system()
        
        # Système de relations
        self._initialize_relationship_system()
        
        # Système de destinée
        self._initialize_destiny_system()
        
        logger.info("Systèmes avancés initialisés.")
        
    def _initialize_enhanced_inventory(self):
        """Initialise le système d'inventaire avancé"""
        if "inventory" not in self.player:
            self.player["inventory"] = {
                "equipped": {},
                "backpack": [],
                "storage": [],
                "currency": {
                    "gold": 0,
                    "silver": 0,
                    "copper": 0
                },
                "capacity": {
                    "current": 0,
                    "maximum": 50  # Capacité de base
                }
            }
            
            # Ajouter des emplacements d'équipement selon l'âge
            if self.player.get("age", 0) < 6:
                # Les très jeunes n'ont pas vraiment d'équipement
                self.player["inventory"]["equipped"] = {
                    "vêtement": "vêtements d'enfant",
                    "jouet": "jouet préféré"
                }
            else:
                # Équipement standard pour les plus âgés
                self.player["inventory"]["equipped"] = {
                    "tête": None,
                    "torse": "vêtements simples",
                    "jambes": "pantalon simple",
                    "pieds": "chaussures",
                    "mains": None,
                    "accessoire1": None,
                    "accessoire2": None,
                    "arme_principale": None,
                    "arme_secondaire": None
                }
                
                # Ajouter quelques objets de base au sac à dos
                self.player["inventory"]["backpack"] = [
                    {"id": "potion_soin", "quantity": 1},
                    {"id": "ration", "quantity": 3}
                ]
        
        return True

    def _initialize_economy_system(self):
        """Initialise le système économique du joueur"""
        if "economy" not in self.player:
            self.player["economy"] = {
                "wealth_level": 0,  # -2:miséreux, -1:pauvre, 0:moyen, 1:aisé, 2:riche
                "income_sources": [],
                "expenses": [],
                "transactions": []
            }
            
            # Définir la richesse initiale en fonction de l'origine
            family_background = self.player.get("family_background", "")
            if "noble" in family_background.lower():
                self.player["economy"]["wealth_level"] = 2
                self.player["inventory"]["currency"]["gold"] = random.randint(10, 50)
            elif "marchande" in family_background.lower() or "artisan" in family_background.lower():
                self.player["economy"]["wealth_level"] = 1
                self.player["inventory"]["currency"]["gold"] = random.randint(2, 10)
                self.player["inventory"]["currency"]["silver"] = random.randint(10, 50)
            elif "paysan" in family_background.lower() or "serviteur" in family_background.lower():
                self.player["economy"]["wealth_level"] = -1
                self.player["inventory"]["currency"]["silver"] = random.randint(2, 10)
                self.player["inventory"]["currency"]["copper"] = random.randint(10, 30)
            elif "orphelin" in family_background.lower():
                self.player["economy"]["wealth_level"] = -2
                self.player["inventory"]["currency"]["copper"] = random.randint(5, 15)
            else:
                # Famille moyenne
                self.player["economy"]["wealth_level"] = 0
                self.player["inventory"]["currency"]["silver"] = random.randint(5, 15)
                self.player["inventory"]["currency"]["copper"] = random.randint(20, 50)
        
        return True
# Fin BLOC 13: Plus de Méthodes Utilitaires et Initialisation des Systèmes Avancés

# BLOC 14: Systèmes Avancés - Partie 1 (Mémoire et Personnalité)
    def _initialize_memory_system(self):
        """Initialise le système de mémoire narrative"""
        if "memories" not in self.player:
            self.player["memories"] = {
                "formative": [],   # Expériences qui ont formé le personnage
                "emotional": [],   # Connexions émotionnelles
                "traumatic": [],   # Événements traumatisants
                "joyful": [],      # Moments de bonheur
                "achievements": [] # Réussites importantes
            }
            
            # Journal de bord
            self.player["journal"] = []
            
            # Historique narratif
            self.player["narrative_history"] = []
        
        return True
        
    def _initialize_personality_system(self):
        """Initialise le système de personnalité évolutive"""
        if "personality" not in self.player:
            # Traits initiaux aléatoires mais légèrement biaisés selon la race/classe
            self.player["personality"] = {
                "extraversion": random.uniform(0.4, 0.6),    # 0-1: introverti-extraverti
                "agreeableness": random.uniform(0.4, 0.6),   # 0-1: antagoniste-aimable
                "conscientiousness": random.uniform(0.4, 0.6), # 0-1: impulsif-consciencieux
                "neuroticism": random.uniform(0.4, 0.6),     # 0-1: stable-névrosé
                "openness": random.uniform(0.4, 0.6),        # 0-1: traditionnel-ouvert
                "dominant_traits": [],
                "life_outlook": "neutre"  # positif, négatif, neutre...
            }
            
            # Ajuster selon l'âge - les bébés et enfants sont généralement plus extravertis et ouverts
            if self.player.get("age", 18) < 12:
                self.player["personality"]["extraversion"] = random.uniform(0.6, 0.8)
                self.player["personality"]["openness"] = random.uniform(0.6, 0.9)
            
            # Ajuster selon la race
            if self.player.get("race") == "Elf Race":
                self.player["personality"]["extraversion"] -= 0.1  # Plus réservés
                self.player["personality"]["openness"] += 0.1      # Plus ouverts
            elif self.player.get("race") == "Dwarf Race":
                self.player["personality"]["conscientiousness"] += 0.1  # Plus disciplinés
                self.player["personality"]["agreeableness"] -= 0.1      # Plus têtus
        
        return True
# Fin BLOC 14: Systèmes Avancés - Partie 1 (Mémoire et Personnalité)

# BLOC 15: Systèmes Avancés - Partie 2 (Compétences et Santé)
    def _initialize_skill_progression_system(self):
        """Initialise le système de progression des compétences"""
        if "skills" not in self.player:
            self.player["skills"] = []
        
        # Convertir les compétences simples en objets détaillés si nécessaire
        for i, skill in enumerate(self.player["skills"]):
            if isinstance(skill, str):
                self.player["skills"][i] = {
                    "name": skill,
                    "level": 1,
                    "exp": 0,
                    "category": self._guess_skill_category(skill)
                }
                
        # Initialiser l'expérience si non présente
        if "exp" not in self.player:
            self.player["exp"] = 0
            
        if "level" not in self.player:
            self.player["level"] = 1
            
        return True
    
    def _guess_skill_category(self, skill_name):
        """Devine la catégorie d'une compétence basée sur son nom"""
        
        skill_lower = skill_name.lower()
        
        if any(word in skill_lower for word in ["force", "agilité", "combat", "mouvement", "marche", "pas", "saut"]):
            return "Physique"
        elif any(word in skill_lower for word in ["parole", "mots", "communication", "charme", "sourire", "social"]):
            return "Social"
        elif any(word in skill_lower for word in ["lecture", "écriture", "apprentissage", "connaissance", "créativité"]):
            return "Mental"
        elif any(word in skill_lower for word in ["sourire", "gazouillis", "retourner", "asseoir", "ramper"]) and self.player.get("age", 0) <= 3:
            return "Développement"
        
        return "Spécial"
    
    def _improve_skill_by_use(self, skill_name, intensity=1.0):
        """
        Améliore une compétence spécifique par la pratique
        
        Parameters:
        - skill_name: Nom de la compétence
        - intensity: Intensité de l'activité (0.1 à 2.0)
        """
        
        # Initialiser la structure des compétences
        if "skills" not in self.player:
            self.player["skills"] = []
        
        # Vérifier l'âge du personnage pour déterminer la vitesse d'apprentissage
        player_age = self.player.get("age", 0)
        learning_factor = 1.0
        
        # Les enfants apprennent plus vite certaines compétences de base
        if player_age < 6:
            learning_factor = 1.5
        # Les adolescents apprennent vite
        elif player_age < 18:
            learning_factor = 1.2
        # Les adultes apprennent à vitesse normale
        else:
            learning_factor = 1.0
        
        # Chercher la compétence existante
        skill_found = False
        
        for i, skill in enumerate(self.player["skills"]):
            # Si la compétence est déjà un dictionnaire avec des détails
            if isinstance(skill, dict) and skill.get("name") == skill_name:
                skill_found = True
                
                # Augmenter l'expérience de la compétence
                if "exp" not in skill:
                    skill["exp"] = 0
                if "level" not in skill:
                    skill["level"] = 1
                    
                # Calculer l'expérience gagnée
                exp_gain = intensity * learning_factor
                skill["exp"] += exp_gain
                
                # Vérifier si la compétence peut monter de niveau
                # Formule: 10 * niveau actuel^1.5
                exp_needed = 10 * (skill["level"] ** 1.5)
                
                if skill["exp"] >= exp_needed:
                    # Monter de niveau la compétence
                    skill["level"] += 1
                    skill["exp"] -= exp_needed  # Garder l'excédent
                    
                    logger.info(f"\n✨ Votre compétence '{skill_name}' a atteint le niveau {skill['level']} !")
                    
                    # Ajouter un bonus aux statistiques appropriées en fonction de la compétence
                    self._apply_skill_stat_bonus(skill_name, skill["level"])
                break
                
            # Si la compétence est juste un nom de chaîne
            elif skill == skill_name:
                # Convertir en dictionnaire pour ajouter des détails
                self.player["skills"][i] = {
                    "name": skill_name,
                    "level": 1,
                    "exp": intensity * learning_factor,
                    "category": self._guess_skill_category(skill_name)
                }
                skill_found = True
                break
        
        # Si la compétence n'existe pas encore, l'ajouter
        if not skill_found:
            # Vérifier si la compétence est appropriée pour l'âge
            if not self._is_skill_appropriate_for_age(skill_name, player_age):
                # Si ce n'est pas approprié, ne pas ajouter mais ne pas signaler d'erreur
                return False
                
            self.player["skills"].append({
                "name": skill_name,
                "level": 1,
                "exp": intensity * learning_factor,
                "category": self._guess_skill_category(skill_name)
            })
            logger.info(f"\n🆕 Vous avez commencé à développer une nouvelle compétence: '{skill_name}' !")
        
        return True
    
    def _is_skill_appropriate_for_age(self, skill_name, age):
        """Vérifie si une compétence est appropriée pour l'âge du personnage"""
        
        skill_lower = skill_name.lower()
        
        # Compétences pour nouveau-nés (0-1 an)
        if age < 1:
            allowed_skills = ["gazouillis", "observ", "reconnaiss", "mouvement", "sourire", "regard", "attention", "réflexe"]
            return any(term in skill_lower for term in allowed_skills)
            
        # Compétences pour tout-petits (1-3 ans)
        elif age < 3:
            allowed_skills = ["march", "parl", "jeu", "ramper", "observ", "communic", "manip", "expressi", "émotio", "imitat", "curiosi"]
            if any(term in skill_lower for term in allowed_skills):
                return True
            # Vérifier si c'est une compétence de nouveau-né (toujours valide)
            return self._is_skill_appropriate_for_age(skill_name, 0.5)
            
        # Compétences pour enfants (3-12 ans)
        elif age < 12:
            disallowed_skills = ["combat avancé", "magie complexe", "alchimie", "forge", "compétence sexuelle"]
            return not any(term in skill_lower for term in disallowed_skills)
        
        # Les adolescents et adultes peuvent apprendre presque tout
        else:
            return True
    
    def _apply_skill_stat_bonus(self, skill_name, skill_level):
        """Applique des bonus aux statistiques en fonction des compétences améliorées"""
        
        if "stats" not in self.player:
            return
            
        skill_lower = skill_name.lower()
        bonus_amount = 0.5  # Petit bonus pour éviter une progression trop rapide
        
        # Compétences physiques
        if any(term in skill_lower for term in ["courir", "force", "endurance", "athlét", "combat", "saut"]):
            stat = "force" if "force" in skill_lower else "constitution"
            self.player["stats"][stat] += bonus_amount
            logger.info(f"↑ Votre {stat} a légèrement augmenté grâce à votre pratique !")
            
        # Compétences de dextérité
        elif any(term in skill_lower for term in ["agilit", "dextér", "précis", "main", "lancer", "esquive", "équilibre"]):
            self.player["stats"]["dexterite"] += bonus_amount
            logger.info(f"↑ Votre dextérité a légèrement augmenté grâce à votre pratique !")
            
        # Compétences mentales
        elif any(term in skill_lower for term in ["intellig", "étude", "connais", "analys", "lire", "écrire", "calcul"]):
            self.player["stats"]["intelligence"] += bonus_amount
            logger.info(f"↑ Votre intelligence a légèrement augmenté grâce à votre pratique !")
            
        # Compétences de sagesse
        elif any(term in skill_lower for term in ["sagesse", "percep", "médita", "observ", "intuit", "survi"]):
            self.player["stats"]["sagesse"] += bonus_amount
            logger.info(f"↑ Votre sagesse a légèrement augmenté grâce à votre pratique !")
            
        # Compétences sociales
        elif any(term in skill_lower for term in ["charm", "social", "persuad", "négocia", "intimi", "empathi"]):
            self.player["stats"]["charisme"] += bonus_amount
            logger.info(f"↑ Votre charisme a légèrement augmenté grâce à votre pratique !")
        
        return True
    
    def _initialize_health_system(self):
        """Initialise le système de santé et bien-être du personnage"""
        
        # Vérifier si le système existe déjà
        if "health" not in self.player:
            # Structure de base
            self.player["health"] = {
                "physical": {
                    "overall": 100,  # 0-100
                    "conditions": [],  # Liste des problèmes de santé
                    "injuries": [],    # Blessures actuelles
                    "growth": None,    # Stade de développement physique
                    "immunity": 100    # Résistance aux maladies
                },
                "mental": {
                    "overall": 100,  # 0-100
                    "stress": 0,     # 0-100
                    "happiness": 80, # 0-100
                    "conditions": [] # Conditions mentales
                },
                "energy": 100,      # 0-100 (niveau d'énergie)
                "sleep_quality": {
                    "recent": 80,    # 0-100
                    "debt": 0        # Heures de sommeil manquantes
                },
                "nutrition": {
                    "status": "good", # starving, hungry, adequate, good, excellent
                    "recent_meals": [],
                    "last_meal_time": self.game_time.get("day", 0) * 24 + self.game_time.get("hour", 0)
                }
            }
            
            # Ajuster en fonction de l'âge
            player_age = self.player.get("age", 0)
            
            # Stade de développement physique selon l'âge
            if player_age < 1:
                self.player["health"]["physical"]["growth"] = "nouveau-né"
            elif player_age < 3:
                self.player["health"]["physical"]["growth"] = "tout-petit"
            elif player_age < 12:
                self.player["health"]["physical"]["growth"] = "enfant"
            elif player_age < 16:
                self.player["health"]["physical"]["growth"] = "adolescent"
            elif player_age < 30:
                self.player["health"]["physical"]["growth"] = "jeune_adulte"
            elif player_age < 60:
                self.player["health"]["physical"]["growth"] = "adulte"
            else:
                self.player["health"]["physical"]["growth"] = "senior"
        
        return True
# Fin BLOC 15: Systèmes Avancés - Partie 2 (Compétences et Santé)

# BLOC 16: Systèmes Avancés - Partie 3 (Relations et Destinée)
    def _initialize_relationship_system(self):
        """Initialise le système de relations avec les PNJs"""
        
        if "relationships" not in self.player:
            self.player["relationships"] = {}
            
        if "interaction_history" not in self.player:
            self.player["interaction_history"] = {}
            
        # Créer des relations familiales si le personnage est jeune
        player_age = self.player.get("age", 18)
        family_background = self.player.get("family_background", "")
        
        if player_age < 18 and family_background and family_background != "Orphelin" and "family_members" not in self.player:
            # Créer des membres de famille basiques
            self.player["family_members"] = []
            
            # Parents
            if family_background != "Orphelin":
                father = {
                    "id": "father_" + self.player["name"].lower(),
                    "name": self._generate_parent_name("père"),
                    "relation": "father",
                    "age": random.randint(player_age + 20, player_age + 40)
                }
                
                mother = {
                    "id": "mother_" + self.player["name"].lower(),
                    "name": self._generate_parent_name("mère"),
                    "relation": "mother",
                    "age": random.randint(player_age + 18, player_age + 38)
                }
                
                self.player["family_members"].extend([father, mother])
                
                # Initialiser les relations avec les parents
                for parent in [father, mother]:
                    if parent["id"] not in self.player["relationships"]:
                        self.player["relationships"][parent["id"]] = {
                            "affinity": 80,  # Amour parental élevé
                            "trust": 90,     # Confiance élevée
                            "familiarity": 100  # Très familier
                        }
                
                # Possibilité de frères et sœurs
                if random.random() < 0.7:  # 70% de chance d'avoir des frères et sœurs
                    siblings_count = random.randint(1, 3)
                    
                    for i in range(siblings_count):
                        sibling_age = max(1, random.randint(player_age - 10, player_age + 10))
                        gender = random.choice(["frère", "sœur"])
                        
                        sibling = {
                            "id": f"sibling_{i}_{self.player['name'].lower()}",
                            "name": self._generate_sibling_name(gender),
                            "relation": "brother" if gender == "frère" else "sister",
                            "age": sibling_age,
                            "gender": gender
                        }
                        
                        self.player["family_members"].append(sibling)
                        
                        # Initialiser la relation avec le frère/sœur
                        if sibling["id"] not in self.player["relationships"]:
                            # Relation variable, possibilité de rivalité ou complicité
                            affinity = random.randint(60, 90)
                            
                            self.player["relationships"][sibling["id"]] = {
                                "affinity": affinity,
                                "trust": min(affinity + 10, 100),
                                "familiarity": 90
                            }
            
        return True
    
    def _generate_parent_name(self, role):
        """Génère un nom pour un parent"""
        if role == "père":
            return random.choice([
                "Alden", "Garon", "Thorn", "Ethran", "Joren", "Marcus", "Darian",
                "Silas", "Rowan", "Terrin", "Dorian", "Hadrian", "Gareth", "Brennan"
            ])
        else:  # mère
            return random.choice([
                "Elara", "Lyria", "Seraphina", "Tessa", "Mira", "Liana", "Ariana",
                "Celeste", "Freya", "Meredith", "Helena", "Johanna", "Lydia", "Vivian"
            ])
    
    def _generate_sibling_name(self, gender):
        """Génère un nom pour un frère ou une sœur"""
        if gender == "frère":
            return random.choice([
                "Aiden", "Liam", "Evan", "Nathan", "Isaac", "Caleb", "Connor",
                "Felix", "Julian", "Owen", "Sebastian", "Tristan", "Xavier", "Zachary"
            ])
        else:  # sœur
            return random.choice([
                "Emma", "Sophia", "Olivia", "Ava", "Isabella", "Mia", "Charlotte",
                "Amelia", "Harper", "Evelyn", "Abigail", "Emily", "Lucy", "Chloe"
            ])
    
    def _update_relationship(self, npc_id, interaction_type):
        """Met à jour les relations avec les PNJs en fonction des interactions"""
        
        # Initialiser le système de relations s'il n'existe pas
        if "relationships" not in self.player:
            self.player["relationships"] = {}
        
        # Initialiser la relation avec ce PNJ si elle n'existe pas
        if npc_id not in self.player["relationships"]:
            self.player["relationships"][npc_id] = {
                "affinity": 50,  # 0-100
                "trust": 50,     # 0-100
                "familiarity": 10  # 0-100
            }
        
        relation = self.player["relationships"][npc_id]
        
        # Modifier la relation en fonction du type d'interaction
        if interaction_type == "positive":
            relation["affinity"] = min(100, relation["affinity"] + random.randint(3, 8))
            relation["trust"] = min(100, relation["trust"] + random.randint(2, 5))
        elif interaction_type == "negative":
            relation["affinity"] = max(0, relation["affinity"] - random.randint(5, 10))
            relation["trust"] = max(0, relation["trust"] - random.randint(3, 8))
        
        # La familiarité augmente toujours avec chaque interaction
        relation["familiarity"] = min(100, relation["familiarity"] + random.randint(1, 3))
        
        # Retourner la relation mise à jour
        return relation
    
    def _initialize_destiny_system(self):
        """Initialise le système de potentiel et destinée du personnage"""
        
        if "destiny" not in self.player:
            # Structure de base
            self.player["destiny"] = {
                "potential_areas": [],
                "affinities": {},
                "discovered_paths": [],
                "active_path": None,
                "prophecies": [],
                "significant_events": []
            }
            
            # Générer des potentiels basés sur les traits existants
            self._generate_initial_potential()
        
        return True
    
    def _generate_initial_potential(self):
        """Génère le potentiel initial du personnage basé sur ses attributs"""
        
        destiny = self.player["destiny"]
        stats = self.player.get("stats", {})
        skills = self.player.get("skills", [])
        
        # Découvrir des affinités innées
        if stats:
            # Trouver les deux statistiques les plus élevées
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            top_stats = sorted_stats[:2]
            
            for stat, value in top_stats:
                # Convertir la stat en affinité
                if stat == "force":
                    destiny["affinities"]["physique"] = min(100, value * 1.2)
                elif stat == "intelligence":
                    destiny["affinities"]["arcane"] = min(100, value * 1.2)
                elif stat == "sagesse":
                    destiny["affinities"]["spirituel"] = min(100, value * 1.2)
                elif stat == "dexterite":
                    destiny["affinities"]["précision"] = min(100, value * 1.2)
                elif stat == "charisme":
                    destiny["affinities"]["influence"] = min(100, value * 1.2)
        
        # Découvrir des domaines de potentiel
        skill_names = [s["name"] if isinstance(s, dict) else s for s in skills]
        
        if any("combat" in s.lower() or "épée" in s.lower() or "force" in s.lower() for s in skill_names):
            destiny["potential_areas"].append({
                "name": "Voie du guerrier",
                "description": "Vous avez un talent naturel pour le combat et pourriez exceller dans les arts martiaux.",
                "discovery_age": self.player.get("age", 0),
                "strength": random.randint(60, 80)
            })
        
        if any("magie" in s.lower() or "arcane" in s.lower() or "sort" in s.lower() for s in skill_names):
            destiny["potential_areas"].append({
                "name": "Voie du mage",
                "description": "Les énergies magiques semblent vous répondre naturellement, révélant un potentiel arcanique.",
                "discovery_age": self.player.get("age", 0),
                "strength": random.randint(60, 80)
            })
        
        if any("nature" in s.lower() or "animal" in s.lower() or "survie" in s.lower() for s in skill_names):
            destiny["potential_areas"].append({
                "name": "Voie du protecteur de la nature",
                "description": "Vous avez une connexion spéciale avec le monde naturel et ses créatures.",
                "discovery_age": self.player.get("age", 0),
                "strength": random.randint(60, 80)
            })
        
        if any("parole" in s.lower() or "charme" in s.lower() or "influence" in s.lower() for s in skill_names):
            destiny["potential_areas"].append({
                "name": "Voie du meneur",
                "description": "Vous avez un charisme naturel qui inspire les autres à vous suivre.",
                "discovery_age": self.player.get("age", 0),
                "strength": random.randint(60, 80)
            })
        
        # Voie mystérieuse aléatoire
        mysterious_paths = [
            {
                "name": "Élu des étoiles",
                "description": "Une connexion mystérieuse avec les astres semble influencer votre destin.",
                "discovery_age": self.player.get("age", 0),
                "strength": random.randint(70, 90)
            },
            {
                "name": "Âme ancienne",
                "description": "Vous portez en vous des fragments de connaissances et souvenirs qui semblent venir d'un autre temps.",
                "discovery_age": self.player.get("age", 0),
                "strength": random.randint(70, 90)
            },
            {
                "name": "Marcheur entre les mondes",
                "description": "Parfois, vous percevez des échos d'autres réalités, comme si votre esprit pouvait voyager au-delà des limites.",
                "discovery_age": self.player.get("age", 0),
                "strength": random.randint(70, 90)
            }
        ]
        
        # 20% de chance d'avoir une voie mystérieuse
        if random.random() < 0.2:
            destiny["potential_areas"].append(random.choice(mysterious_paths))
        
        return True
# Fin BLOC 16: Systèmes Avancés - Partie 3 (Relations et Destinée)

# BLOC 17: Méthodes pour les actions du jeu et la boucle principale
    def load_saved_game(self):
        """Charge une partie sauvegardée"""
        logger.info("\nRecherche des sauvegardes disponibles...")
        
        try:
            # Listing des sauvegardes
            saves = self.save_manager.list_saves()
            
            if not saves:
                logger.info("Aucune sauvegarde trouvée.")
                return
            
            # Afficher la liste des sauvegardes
            print("\nSauvegardes disponibles:")
            for i, save in enumerate(saves):
                print(f"{i+1}. {save.get('name', 'Sauvegarde sans nom')}")
            print(f"{len(saves)+1}. Retour")
            
            # Choix de la sauvegarde
            try:
                choice = int(input("\nVotre choix: "))
                if 1 <= choice <= len(saves):
                    save = saves[choice-1]
                    result = self.save_manager.load_game(save.get("path", ""))
                    if result.get("success", False):
                        logger.info("Sauvegarde chargée avec succès.")
                        self.game_loop()
                    else:
                        logger.error("Erreur lors du chargement de la sauvegarde.")
                elif choice == len(saves) + 1:
                    return
                else:
                    print("Choix invalide.")
            except ValueError:
                print("Veuillez entrer un nombre.")
        except Exception as e:
            logger.error(f"\n❌ Erreur lors du chargement de la partie: {e}")
            input("Appuyez sur Entrée pour continuer...")
    
    def quit_game(self):
        """Quitte le jeu"""
        logger.info("\nMerci d'avoir joué à MUSKO TENSEI RP!")
        print("\nMerci d'avoir joué à MUSKO TENSEI RP!")
        print("À bientôt pour de nouvelles aventures!")
        time.sleep(1)
    
    def game_loop(self):
        """Boucle de jeu principale avec narration immersive, développement continuel et vie simulée"""
        try:
            print("\n" + "~"*60)
            print("DÉBUT DE L'AVENTURE".center(60))
            print("~"*60)
            
            # Initialisation comme avant
            # Génération de la description initiale adaptée à l'âge
            self._generate_initial_scene()
            
            # Boucle de jeu principale
            playing = True
            while playing:
                # Mise à jour de l'état du monde et du personnage
                self._update_player_state()
                current_environment = self._simulate_environment()
                
                # Si le personnage dort, générer un rêve et faire avancer le temps
                if self.player.get("states", {}).get("activité_actuelle") == "sommeil":
                    self._generate_dream()
                    # Avancer le temps (sommeil)
                    hours_slept = 8 if self.player.get("age", 0) > 3 else 12
                    self._advance_time_hours(hours_slept)
                    self.player["states"]["activité_actuelle"] = "éveillé"
                    self.player["states"]["fatigue"] = max(0, self.player["states"]["fatigue"] - 80)
                    print("\nVous vous réveillez, reposé et prêt à affronter une nouvelle journée.")
                
                # Vérifier les événements narratifs en cours
                active_arcs = self.player.get("narrative_arcs", {}).get("active", [])
                if active_arcs:
                    # 20% de chance de progression dans un arc narratif
                    if random.random() < 0.2:
                        self._progress_narrative_arc(random.choice(active_arcs))
                
                # Afficher les informations contextuelles
                self._display_contextual_information()
                
                # Générer et afficher les choix adaptés
                actions = self._generate_contextual_choices()
                
                # Afficher les choix
                print("\n" + "-"*60)
                print("Que souhaitez-vous faire?")
                
                # D'abord les actions contextuelles
                for i, action in enumerate(actions):
                    print(f"{i+1}. {action}")
                    
                # Ensuite les options spéciales
                special_options = [
                    "📊 Voir mes statistiques et compétences",
                    "♥ Voir mes relations",
                    "📖 Consulter mon journal",
                    "💾 Sauvegarder la partie",
                    "🔙 Retourner au menu principal"
                ]
                
                for i, option in enumerate(special_options):
                    print(f"{len(actions)+i+1}. {option}")
                
                # Traiter le choix du joueur
                try:
                    action_choice = int(input("\nVotre choix: "))
                    
                    # Traiter les choix contextuels
                    if 1 <= action_choice <= len(actions):
                        result = self._handle_player_action(action_choice-1, actions)
                        if result is False:  # Si l'action demande de quitter la boucle
                            playing = False
                    
                    # Traiter les options spéciales
                    elif len(actions) < action_choice <= len(actions) + len(special_options):
                        special_idx = action_choice - len(actions) - 1
                        
                        if special_idx == 0:  # Statistiques
                            self.show_character_stats()
                        elif special_idx == 1:  # Relations
                            self.show_relationships()
                        elif special_idx == 2:  # Journal
                            self.show_journal()
                        elif special_idx == 3:  # Sauvegarder
                            self.save_game()
                        elif special_idx == 4:  # Menu principal
                            playing = False
                            logger.info("\nRetour au menu principal...")
                    else:
                        print("Choix invalide. Veuillez réessayer.")
                except ValueError:
                    print("Veuillez entrer un nombre.")
                
                # Vérification des événements de développement après chaque action
                if self.player.get("age", 0) < 13:  # Pour les jeunes personnages
                    self._check_development_milestone()
                
                # Possibilité d'événement aléatoire entre les actions (10% de chance)
                if random.random() < 0.1:
                    self._generate_random_event()
                
        except Exception as e:
            logger.error(f"\n❌ Une erreur s'est produite dans la boucle de jeu: {e}")
            print("\nRetour au menu principal...")
            import traceback
            traceback.print_exc()
            input("\nAppuyez sur Entrée pour continuer...")
            return
    
    def save_game(self):
        """Sauvegarde la partie actuelle"""
        logger.info("\nSauvegarde de la partie...")
        try:
            save_name = input("Nom de la sauvegarde (ou Entrée pour utiliser la date actuelle): ")
            if not save_name:
                # Utiliser la date et l'heure actuelles comme nom de sauvegarde
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
                save_name = f"{self.player['name']}_{current_time}"
            
            result = self.save_manager.save_game("autosave", save_name)
            if result.get("success", False):
                logger.info(f"Partie sauvegardée avec succès sous '{save_name}'")
                print(f"Partie sauvegardée avec succès sous '{save_name}'")
            else:
                logger.error("Erreur lors de la sauvegarde.")
                print("Erreur lors de la sauvegarde.")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            print(f"❌ Erreur lors de la sauvegarde: {e}")
        
        input("\nAppuyez sur Entrée pour continuer...")
            
    def _get_display_race_name(self, race):
        """Retourne le nom d'affichage correct d'une race"""
        race_names = {
            "Human Race": "Humain",
            "Elf Race": "Elfe",
            "High Elf Race": "Haut Elfe",
            "Dwarf Race": "Nain",
            "Halfling Race": "Halfelin",
            "Dragon Tribe": "Dragon",
            "Migurd Race": "Migurd",
            "Superd Race": "Superd",
            "Immortal Demon Race": "Démon Immortel",
            "Ogre Race": "Ogre",
            "Beast Race": "Bête",
            "Heaven Race": "Céleste",
            "Sea Race": "Marin",
            "Mixed-Blood Race": "Sang-Mêlé",
            "Cursed Children": "Enfant Maudit",
            "Elemental Spirits": "Esprit Élémentaire",
            "Sylphs": "Sylphe",
            "Ancient Races": "Ancien"
        }
        return race_names.get(race, race)
    
    def _progress_narrative_arc(self, arc):
        """Fait progresser un arc narratif"""
        # Note: Cette méthode sera implémentée dans une version future
        return True
# Fin BLOC 17: Méthodes pour les actions du jeu et la boucle principale

# BLOC 18: Méthodes d'exploration et de scène initiale
    def _generate_initial_scene(self):
        """Génère une scène initiale adaptée à l'âge et au contexte du personnage"""
        player_age = self.player.get("age", 0)
        race_display_name = self._get_display_race_name(self.player["race"])
        
        try:
            # Adapte la scène selon l'âge
            if player_age < 1:  # Bébé
                scene_context = {
                    "player_data": self.player,
                    "scene_type": "début_bébé"
                }
                
                scene_prompt = (
                    f"Génère une description détaillée et immersive des premiers instants d'un bébé de {player_age} mois "
                    f"nommé {self.player['name']}, un {race_display_name}. Décris son environnement immédiat, ce qu'il peut "
                    f"percevoir avec ses sens limités (vue, ouïe, odorat, toucher), le confort de son berceau, "
                    f"et la présence rassurante de ses parents. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Peu ou pas de cheveux, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"Utilise un style qui capture l'innocence et la découverte du monde. "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
                
            elif player_age < 6:  # Jeune enfant
                scene_context = {
                    "player_data": self.player,
                    "scene_type": "début_enfant"
                }
                
                scene_prompt = (
                    f"Génère une description détaillée et immersive d'un enfant de {player_age} ans "
                    f"nommé {self.player['name']}, un {race_display_name}, qui se réveille dans sa chambre d'enfant. "
                    f"Décris son environnement familier, ses jouets préférés, les sons de la maison, et les premières "
                    f"pensées qui traversent son jeune esprit. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower()}, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"Utilise un style qui capture la curiosité et l'innocence de l'enfance. "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
                
            else:  # Adolescent ou adulte
                scene_context = {
                    "player_data": self.player,
                    "scene_type": "début_aventure"
                }
                
                location_id = self.current_location
                location_data = self.locations_data.get(location_id, {})
                location_name = location_data.get("name", "un endroit inconnu")
                
                scene_prompt = (
                    f"Génère une description détaillée et immersive de {self.player['name']}, "
                    f"un {race_display_name} de {player_age} ans, {self.player.get('class', 'aventurier')}, "
                    f"qui commence son aventure à {location_name}. "
                    f"Décris l'environnement, l'atmosphère, et les premières impressions du personnage. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower()}, "
                    f"Peau {self.player['appearance']['skin'].lower()}. "
                    f"Mentionne subtilement l'arrière-plan du personnage: {self.player.get('family_background', 'mystérieux')}. "
                    f"EXIGENCE ABSOLUE: Orthographe et grammaire impeccables, style narratif élégant et captivant."
                )
            
            # Génération de la scène avec l'IA
            logger.info("Génération de la scène initiale...")
            initial_scene = self.ai_manager.generate_response(scene_prompt, scene_context)
            
            print("\n" + "="*70)
            print(initial_scene)
            print("="*70 + "\n")
            
            # Stocker cette scène comme premier souvenir
            self._add_memory("formative", {
                "description": "Vos premiers moments dans cette aventure",
                "content": initial_scene,
                "emotional_impact": 0.8
            })
            
            # Ajouter au journal
            self._add_journal_entry("beginning", initial_scene)
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la scène initiale: {e}")
            print("\nVous commencez votre aventure dans un monde rempli de mystères et de possibilités.")
            return False
    
    def _generate_dream(self):
        """Génère un rêve reflétant le développement subconscient du personnage"""
        
        # Vérifier si le personnage dort
        if self.player.get("states", {}).get("activité_actuelle") != "sommeil":
            return False
        
        # Contexte pour la génération du rêve
        player_age = self.player.get("age", 0)
        personality = self.player.get("personality", {})
        memories = self.player.get("memories", {})
        recent_events = self.player.get("recent_events", [])
        
        # Sélectionner les éléments qui influencent le rêve
        dream_influences = []
        
        # Des événements récents
        if recent_events:
            for i in range(min(2, len(recent_events))):
                dream_influences.append({
                    "type": "recent_event",
                    "content": recent_events[i].get("description", "un événement récent")
                })
        
        # Des souvenirs importants
        for category in ["emotional", "traumatic", "joyful"]:
            if category in memories and memories[category]:
                # Prendre un souvenir aléatoire de chaque catégorie
                memory = random.choice(memories[category])
                dream_influences.append({
                    "type": f"memory_{category}",
                    "content": memory.get("description", "un souvenir")
                })
        
        # Des désirs inconscients basés sur la personnalité
        if "dominant_traits" in personality and personality["dominant_traits"]:
            trait = random.choice(personality["dominant_traits"])
            if trait == "curieux":
                dream_influences.append({
                    "type": "desire",
                    "content": "découvrir quelque chose de nouveau et fascinant"
                })
            elif trait == "introverti":
                dream_influences.append({
                    "type": "desire",
                    "content": "trouver un endroit paisible et serein"
                })
        
        # Générer le rêve avec l'IA
        dream_context = {
            "player_data": self.player,
            "dream_influences": dream_influences,
            "player_age": player_age
        }
        
        dream_prompt = (
            f"Génère un rêve pour {self.player['name']}, {player_age} an{'s' if player_age > 1 else ''}, "
            f"qui est en train de dormir. Le rêve doit être adapté à l'âge et à la psychologie du personnage, "
            f"et intégrer subtilement ces éléments: "
            f"{', '.join([influence['content'] for influence in dream_influences])}. "
            f"Pour un très jeune enfant (<3 ans), le rêve doit être simple et sensoriel. "
            f"Pour un enfant (3-12 ans), il peut être plus imaginatif. "
            f"Pour un adolescent ou adulte, il peut être plus complexe et symbolique. "
            f"Le rêve doit être écrit de façon immersive à la deuxième personne et révéler quelque chose "
            f"de subtil sur le développement psychologique du personnage."
        )
        
        try:
            logger.info("Génération d'un rêve...")
            dream_text = self.ai_manager.generate_response(dream_prompt, dream_context)
            print("\n" + "~"*70)
            print("VOUS RÊVEZ...".center(70))
            print("-"*70)
            print(dream_text)
            print("~"*70)
            
            # Ajouter au journal
            self._add_journal_entry("dream", dream_text)
            
            # Possibilité d'influence psychologique du rêve
            if random.random() < 0.3:  # 30% de chance
                self._apply_dream_psychological_effect()
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la génération du rêve: {e}")
            return False
    
    def _apply_dream_psychological_effect(self):
        """Applique un effet psychologique suite à un rêve"""
        # Note: Cette méthode sera implémentée dans une version future
        return True
# Fin BLOC 18: Méthodes d'exploration et de scène initiale

# BLOC 19: Méthodes d'interaction et générateurs de contexte
    def _simulate_environment(self):
        """Simule l'évolution de l'environnement et de l'écosystème du monde"""
        
        current_location = self.current_location
        
        # Vérifier si le lieu existe dans les données
        if current_location not in self.locations_data:
            logger.warning(f"Emplacement '{current_location}' non trouvé dans les données. Création d'un lieu par défaut...")
            # Créer un lieu par défaut si non trouvé
            self.locations_data[current_location] = {
                "name": "Lieu inconnu",
                "description": "Un endroit mystérieux dont vous ne savez rien",
                "connections": [],
                "npcs": []
            }
        
        location_data = self.locations_data.get(current_location, {})
        
        # Si l'environnement n'a pas été initialisé pour ce lieu
        if "environment" not in location_data:
            location_data["environment"] = self._initialize_environment(location_data)
        
        # Récupérer les données environnementales
        environment = location_data["environment"]
        
        # Facteurs externes qui affectent l'environnement
        time_of_day = "jour" if 6 <= self.game_time["hour"] <= 18 else "nuit"
        season = self._determine_current_season()
        weather = self.game_time.get("weather", "clair")
        
        # Mettre à jour les éléments environnementaux
        self._update_environment_elements(environment, time_of_day, season, weather)
        
        # 30% de chance de générer un événement environnemental
        if random.random() < 0.3:
            self._generate_environmental_event(environment)
        
        # Sauvegarder les changements
        self.locations_data[current_location]["environment"] = environment
        
        return environment

    def _initialize_environment(self, location_data):
        """Initialise l'environnement d'un lieu avec des détails écologiques"""
        
        location_name = location_data.get("name", "")
        location_type = location_data.get("type", self._guess_location_type(location_name))
        
        # Structure de base de l'environnement
        environment = {
            "type": location_type,
            "flora": [],
            "fauna": [],
            "ambient_sounds": [],
            "scents": [],
            "weather_effects": {},
            "day_night_cycle": {},
            "seasonal_changes": {},
            "special_features": []
        }
        
        # Remplir les détails en fonction du type de lieu
        if "forêt" in location_type.lower() or "bois" in location_type.lower():
            environment["flora"] = ["grands arbres", "buissons", "fougères", "champignons", "fleurs sauvages"]
            environment["fauna"] = ["oiseaux", "écureuils", "lapins", "insectes"]
            environment["ambient_sounds"] = ["bruissement des feuilles", "chants d'oiseaux", "craquement de branches"]
            environment["scents"] = ["humus", "mousse", "fleurs", "résine"]
        elif "village" in location_type.lower() or "ville" in location_type.lower():
            environment["flora"] = ["plantes en pot", "jardins", "arbres ornementaux"]
            environment["fauna"] = ["chats", "chiens", "oiseaux urbains"]
            environment["ambient_sounds"] = ["conversations", "activités artisanales", "jeux d'enfants"]
            environment["scents"] = ["nourriture", "fumée de bois", "herbes séchées"]
        # Autres types...
        
        # Effets météorologiques par défaut
        environment["weather_effects"] = {
            "clair": "lumière brillante, ombres nettes",
            "nuageux": "lumière diffuse, atmosphère calme",
            "pluvieux": "gouttes de pluie, surface mouillée, sons feutrés",
            "brumeux": "visibilité réduite, sons atténués, atmosphère mystérieuse",
            "orageux": "lumière spectaculaire, sons amplifiés, tension dans l'air"
        }
        
        # Cycle jour/nuit
        environment["day_night_cycle"] = {
            "aube": "lumière dorée, rosée matinale, réveil des créatures",
            "jour": "pleine activité, sons variés, luminosité maximale",
            "crépuscule": "lumière rouge-orangée, retour au calme, ambiance nostalgique", 
            "nuit": "sons nocturnes, lumière réduite, activité ralentie"
        }
        
        return environment
    
    def _determine_current_season(self):
        """Détermine la saison actuelle basée sur le jour du jeu"""
        day = self.game_time.get("day", 1)
        
        # Cycle de 120 jours pour les saisons
        season_day = day % 120
        
        if season_day < 30:
            return "printemps"
        elif season_day < 60:
            return "été"
        elif season_day < 90:
            return "automne"
        else:
            return "hiver"
    
    def _update_environment_elements(self, environment, time_of_day, season, weather):
        """Met à jour les éléments environnementaux selon les conditions"""
        # Implémentation simple pour l'instant
        return True

    def _generate_environmental_event(self, environment):
        """Génère un événement environnemental basé sur le lieu et les conditions"""
        
        env_type = environment["type"]
        time_of_day = "jour" if 6 <= self.game_time["hour"] <= 18 else "nuit"
        weather = self.game_time.get("weather", "clair")
        
        # Liste d'événements possibles selon le type d'environnement
        events = []
        
        # Événements pour la forêt
        if "forêt" in env_type.lower() or "bois" in env_type.lower():
            events.extend([
                "Un écureuil curieux s'approche doucement",
                "Une volée d'oiseaux s'envole soudainement",
                "Un rayon de lumière perce à travers les branches",
                "Le vent fait danser délicatement les feuilles",
                "Un animal furtif s'éloigne dans les sous-bois"
            ])
            
            # Événements spéciaux de nuit
            if time_of_day == "nuit":
                events.extend([
                    "Des lucioles illuminent un coin de la forêt",
                    "Un hululement mystérieux résonne entre les arbres",
                    "La lumière de la lune crée des ombres mouvantes"
                ])
        
        # Événements pour le village
        elif "village" in env_type.lower() or "ville" in env_type.lower():
            events.extend([
                "Une odeur de pain frais flotte dans l'air",
                "Des enfants passent en courant et riant",
                "Un artisan travaille minutieusement à sa porte",
                "Des voix chaleureuses s'élèvent d'une maison voisine",
                "Une charrette traverse lentement la rue principale"
            ])
            
            # Événements spéciaux selon l'heure
            if 7 <= self.game_time["hour"] <= 10:
                events.append("Les villageois ouvrent leurs volets et démarrent leur journée")
            elif 17 <= self.game_time["hour"] <= 20:
                events.append("Les familles se rassemblent pour le repas du soir, des lumières s'allument")
        
        # Par défaut, ajouter quelques événements génériques
        if not events:
            events.extend([
                "Une légère brise souffle autour de vous",
                "Vous entendez un son distant",
                "Le temps semble s'écouler paisiblement",
                "Une atmosphère tranquille règne sur les lieux"
            ])
        
        # Sélectionner et présenter un événement
        if events:
            chosen_event = random.choice(events)
            
            # Contexte pour enrichir l'événement
            event_context = {
                "base_event": chosen_event,
                "environment": environment,
                "time_of_day": time_of_day,
                "weather": weather,
                "player_data": self.player
            }
            
            event_prompt = (
                f"Enrichis cette description d'un événement environnemental: '{chosen_event}'. "
                f"Il se déroule dans un environnement de type {env_type}, pendant {time_of_day}, "
                f"avec un temps {weather}. Décris cet événement de façon immersive et sensorielle, "
                f"en 2-3 phrases captivantes, à la deuxième personne du singulier."
            )
            
            try:
                enriched_event = self.ai_manager.generate_response(event_prompt, event_context)
                print("\n" + "-"*70)
                print(enriched_event)
                print("-"*70)
                return True
            except Exception as e:
                logger.error(f"Erreur lors de la génération de l'événement environnemental: {e}")
                print(f"\n{chosen_event}")
                return True
        
        return False
    
    def _guess_location_type(self, location_name):
        """Devine le type de lieu en fonction de son nom"""
        location_name = location_name.lower()
        
        if "forêt" in location_name or "bois" in location_name:
            return "forêt"
        elif "village" in location_name or "ville" in location_name:
            return "village"
        elif "montagne" in location_name:
            return "montagne"
        elif "lac" in location_name or "rivière" in location_name:
            return "eau"
        elif "caverne" in location_name or "grotte" in location_name:
            return "caverne"
        elif "champ" in location_name or "prairie" in location_name:
            return "plaine"
        elif "route" in location_name or "chemin" in location_name:
            return "route"
        elif "temple" in location_name or "sanctuaire" in location_name:
            return "temple"
        else:
            return "lieu générique"
# Fin BLOC 19: Méthodes d'interaction et générateurs de contexte

# BLOC 20: Méthode de gestion des actions du joueur
    def _handle_player_action(self, action_index, actions_list):
        """Gère l'action choisie par le joueur de manière immersive"""
        
        if action_index >= len(actions_list):
            print("Action invalide. Veuillez réessayer.")
            return True
        
        chosen_action = actions_list[action_index]
        logger.info(f"Action du joueur: {chosen_action}")
        
        # Obtenir les informations contextuelles
        player_age = self.player.get("age", 0)
        current_location = self.current_location
        location_data = self.locations_data.get(current_location, {})
        
        # Construire le contexte pour la génération de la réaction
        action_context = {
            "player_data": self.player,
            "location_id": current_location,
            "location_name": location_data.get("name", "lieu inconnu"),
            "chosen_action": chosen_action,
            "time_of_day": "jour" if 6 <= self.game_time["hour"] <= 18 else "nuit",
            "weather": self.game_time.get("weather", "clair")
        }
        
        # Identifier les compétences liées à cette action
        related_skills = self._identify_skills_from_action(chosen_action)
        
        # Générer une réaction adaptée à l'action et à l'âge
        prompt = (
            f"Je suis {self.player['name']}, un {self._get_display_race_name(self.player.get('race'))} "
            f"de {player_age} an{'s' if player_age > 1 else ''} et je viens de {chosen_action}. "
            f"Décris de façon immersive ce qui se passe, les conséquences de mon action et ce que je ressens. "
            f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
            f"Yeux {self.player['appearance']['eyes'].lower()}, "
            f"Cheveux {self.player['appearance'].get('hair', 'peu ou pas de cheveux').lower() if player_age >= 1 else 'peu ou pas de cheveux'}, "
            f"Peau {self.player['appearance']['skin'].lower()}. "
            f"Utilise un style narratif très immersif à la deuxième personne du singulier. "
            f"EXIGENCE: Narration captivante, riche en détails sensoriels, avec une orthographe impeccable."
        )
        
        try:
            reaction = self.ai_manager.generate_response(prompt, action_context)
            print("\n" + "-"*70)
            print(reaction)
            print("-"*70)
            
            # Améliorer les compétences liées à l'action
            for skill, intensity in related_skills.items():
                self._improve_skill_by_use(skill, intensity)
                logger.debug(f"Amélioration de la compétence {skill} (intensité: {intensity})")
            
            # Faire avancer le temps en fonction de l'action
            time_advancement = random.randint(10, 40) if player_age < 3 else random.randint(15, 60)
            self._advance_time_minutes(time_advancement)
            
            # Possibilité d'événement aléatoire suite à l'action
            if random.random() < 0.3:  # 30% de chance
                self._generate_random_event()
                
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la réaction: {e}")
            print(f"\nVous {chosen_action.lower()}.")
            return True
# Fin BLOC 20: Méthode de gestion des actions du joueur

# BLOC 21: Méthodes pour la gestion du temps et des événements
    def _advance_time_minutes(self, minutes):
        """Avance le temps de jeu de X minutes"""
        current_hour = self.game_time.get("hour", 12)
        current_minute = self.game_time.get("minute", 0)
        
        # Ajouter les minutes
        total_minutes = current_minute + minutes
        added_hours = total_minutes // 60
        new_minutes = total_minutes % 60
        
        # Mettre à jour l'heure et les minutes
        new_hour = current_hour + added_hours
        if new_hour >= 24:
            self.game_time["day"] = self.game_time.get("day", 1) + (new_hour // 24)
            new_hour = new_hour % 24
        
        self.game_time["hour"] = new_hour
        self.game_time["minute"] = new_minutes
        
        # Afficher le temps écoulé
        if minutes > 0:
            logger.debug(f"Avancement du temps: {minutes} minutes")
            print(f"\n{minutes} minutes s'écoulent...")
            print(f"Il est maintenant {new_hour:02d}h{new_minutes:02d}.")
    
    def _advance_time_hours(self, hours):
        """Avance le temps de jeu de X heures"""
        logger.debug(f"Avancement du temps: {hours} heures")
        self._advance_time_minutes(hours * 60)
    
    def _generate_random_event(self):
        """Génère un événement aléatoire adapté à l'âge et au contexte"""
        
        player_age = self.player.get("age", 0)
        current_location = self.current_location
        time_of_day = "jour" if 6 <= self.game_time["hour"] <= 18 else "nuit"
        
        # Déterminer le type d'événement selon l'âge et le contexte
        if player_age < 1:  # Bébé
            event_types = ["parent", "sensation", "visite", "phénomène"]
            chosen_type = random.choice(event_types)
            
            if chosen_type == "parent":
                prompt = (
                    f"Génère un court événement où l'un des parents de {self.player['name']}, un bébé de {player_age} mois, "
                    f"vient interagir avec lui. Décris l'interaction du point de vue du bébé, "
                    f"avec les sensations, émotions et perceptions limitées mais intenses d'un nourrisson. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Peu ou pas de cheveux, "
                    f"Peau {self.player['appearance']['skin'].lower()}."
                )
            elif chosen_type == "sensation":
                prompt = (
                    f"Génère un court événement où {self.player['name']}, un bébé de {player_age} mois, "
                    f"découvre une nouvelle sensation (une texture, un son, une odeur, etc.). "
                    f"Décris cette découverte sensorielle du point de vue du bébé. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Peu ou pas de cheveux, "
                    f"Peau {self.player['appearance']['skin'].lower()}."
                )
        elif player_age < 6:  # Jeune enfant
            event_types = ["rencontre", "découverte", "jeu", "famille", "animal"]
            chosen_type = random.choice(event_types)
            
            if chosen_type == "rencontre":
                prompt = (
                    f"Génère un court événement où {self.player['name']}, un enfant de {player_age} ans, "
                    f"rencontre un autre enfant ou un adulte intéressant. "
                    f"Décris cette rencontre du point de vue de l'enfant, avec sa curiosité et sa perspective unique. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower()}, "
                    f"Peau {self.player['appearance']['skin'].lower()}."
                )
            elif chosen_type == "découverte":
                prompt = (
                    f"Génère un court événement où {self.player['name']}, un enfant de {player_age} ans, "
                    f"découvre quelque chose de nouveau et fascinant dans son environnement. "
                    f"Décris cette découverte et l'émerveillement qui l'accompagne. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower()}, "
                    f"Peau {self.player['appearance']['skin'].lower()}."
                )
        else:  # Adolescent ou adulte
            event_types = ["rencontre", "découverte", "défi", "opportunité", "mystère", "combat"]
            chosen_type = random.choice(event_types)
            
            if chosen_type == "rencontre":
                prompt = (
                    f"Génère une rencontre inattendue pour {self.player['name']} à {self.locations_data.get(current_location, {}).get('name', 'ce lieu')}. "
                    f"Un personnage intéressant apparaît et interagit brièvement avec le joueur. "
                    f"Décris qui est cette personne, son apparence, ce qu'elle dit ou fait. "
                    f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                    f"Yeux {self.player['appearance']['eyes'].lower()}, "
                    f"Cheveux {self.player['appearance']['hair'].lower()}, "
                    f"Peau {self.player['appearance']['skin'].lower()}."
                )
            elif chosen_type == "combat":
                if self.player.get("class") in ["Guerrier", "Mage", "Rôdeur", "Paladin", "Assassin"]:
                    prompt = (
                        f"Génère une brève escarmouche pour {self.player['name']}, un {self.player.get('class')} à {self.locations_data.get(current_location, {}).get('name', 'ce lieu')}. "
                        f"Un adversaire de niveau approprié apparaît, décris l'affrontement et sa conclusion. "
                        f"Le combat ne devrait pas être mortel mais représenter un défi. "
                        f"CARACTÉRISTIQUES PHYSIQUES À RESPECTER OBLIGATOIREMENT: "
                        f"Yeux {self.player['appearance']['eyes'].lower()}, "
                        f"Cheveux {self.player['appearance']['hair'].lower()}, "
                        f"Peau {self.player['appearance']['skin'].lower()}."
                    )
                else:
                    # Si la classe n'est pas orientée combat, revenir à un autre type d'événement
                    return self._generate_random_event()
        
        # Générer l'événement avec l'IA
        event_context = {
            "player_data": self.player,
            "event_type": chosen_type,
            "location_id": current_location,
            "time_of_day": time_of_day
        }
        
        try:
            logger.info(f"Génération d'un événement aléatoire de type '{chosen_type}'...")
            event_description = self.ai_manager.generate_response(prompt, event_context)
            print("\n" + "*"*70)
            print("ÉVÉNEMENT ALÉATOIRE".center(70))
            print("-"*70)
            print(event_description)
            print("*"*70)
            
            # Possible impact sur les compétences ou le personnage
            if random.random() < 0.5:  # 50% de chance
                if chosen_type == "combat":
                    combat_skills = ["Combat", "Défense", "Esquive", "Tactique"] if player_age >= 12 else ["Réflexes", "Mouvement"]
                    random_skill = random.choice(combat_skills)
                    self._improve_skill_by_use(random_skill, 1.2)
                elif chosen_type == "découverte":
                    mental_skills = ["Observation", "Analyse", "Connaissance"] if player_age >= 12 else ["Curiosité", "Perception"]
                    random_skill = random.choice(mental_skills)
                    self._improve_skill_by_use(random_skill, 1.0)
                elif chosen_type == "rencontre":
                    social_skills = ["Communication", "Persuasion", "Empathie"] if player_age >= 12 else ["Communication basique", "Expression"]
                    random_skill = random.choice(social_skills)
                    self._improve_skill_by_use(random_skill, 0.8)
            
            # Ajouter au journal
            self._add_journal_entry("event", event_description)
            
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la génération de l'événement aléatoire: {e}")
            return False
# Fin BLOC 21: Méthodes pour la gestion du temps et des événements

# BLOC 22: Méthodes pour les compétences et l'identification d'actions
    def _identify_skills_from_action(self, action):
        """Identifie les compétences qui pourraient être améliorées par cette action"""
        
        skills = {}
        action_lower = action.lower()
        player_age = self.player.get("age", 0)
        
        # Nouveau-né (0-1 an)
        if player_age < 1:
            if any(term in action_lower for term in ["gazu", "gazou", "cri", "son", "parole"]):
                skills["Gazouillis"] = 1.0
            if any(term in action_lower for term in ["regarde", "observe", "regard", "yeux"]):
                skills["Observation"] = 1.0
            if any(term in action_lower for term in ["souris", "sourire", "joie"]):
                skills["Sourire"] = 1.0
            if any(term in action_lower for term in ["attrape", "main", "bouge", "mouvement"]):
                skills["Réflexes moteurs"] = 1.0
            if any(term in action_lower for term in ["dors", "dormir", "endors", "sommeil"]):
                skills["Cycle de sommeil"] = 0.5
        
        # Tout-petit (1-3 ans)
        elif player_age < 3:
            if any(term in action_lower for term in ["marche", "déplace", "pas"]):
                skills["Marche"] = 1.0
            if any(term in action_lower for term in ["parle", "parole", "mot", "dire"]):
                skills["Parole"] = 1.0
            if any(term in action_lower for term in ["joue", "jouet", "jeu"]):
                skills["Jeux d'enfant"] = 1.0
            if any(term in action_lower for term in ["rampe", "quatre pattes"]):
                skills["Déplacement"] = 0.8
            if any(term in action_lower for term in ["dors", "sieste", "sommeil"]):
                skills["Repos"] = 0.5
        
        # Enfant (3-12 ans)
        elif player_age < 12:
            if any(term in action_lower for term in ["cour", "saute", "physique"]):
                skills["Activité physique"] = 1.0
            if any(term in action_lower for term in ["parle", "discute", "conversation"]):
                skills["Communication"] = 1.0
            if any(term in action_lower for term in ["dessin", "colori", "art"]):
                skills["Expression artistique"] = 1.0
            if any(term in action_lower for term in ["observe", "regarde", "étudie"]):
                skills["Observation"] = 0.8
            if any(term in action_lower for term in ["joue", "jeu", "amusement"]):
                skills["Jeu social"] = 0.8
        
        # Adolescent et adulte (12+ ans)
        else:
            # Compétences physiques
            if any(term in action_lower for term in ["combat", "attaque", "défense", "épée", "arme"]):
                skills["Combat"] = 1.2
            if any(term in action_lower for term in ["cours", "sprint", "endurance", "marche"]):
                skills["Endurance"] = 1.0
                skills["Athlétisme"] = 0.8
            
            # Compétences sociales
            if any(term in action_lower for term in ["parle", "discute", "conversation", "négocie"]):
                skills["Communication"] = 1.0
            if any(term in action_lower for term in ["charme", "séduction", "flirt", "persuade"]):
                skills["Charisme"] = 1.2
            
            # Compétences mentales
            if any(term in action_lower for term in ["observe", "analyse", "étudie", "examine"]):
                skills["Observation"] = 0.8
                skills["Analyse"] = 1.0
            if any(term in action_lower for term in ["lis", "livre", "écrit", "recherche"]):
                skills["Érudition"] = 1.2
            
            # Compétences de classe
            if self.player.get("class") == "Mage":
                if any(term in action_lower for term in ["magie", "sort", "incantation"]):
                    skills["Magie"] = 1.5
            if self.player.get("class") == "Guerrier":
                if any(term in action_lower for term in ["combat", "arme", "attaque", "défense"]):
                    skills["Combat"] = 1.5
        
        # Limiter à maximum 3 compétences améliorées par action
        if len(skills) > 3:
            # Garder les 3 avec les valeurs d'intensité les plus élevées
            skills = dict(sorted(skills.items(), key=lambda item: item[1], reverse=True)[:3])
        
        return skills
# Fin BLOC 22: Méthodes pour les compétences et l'identification d'actions

# BLOC 23: Méthodes pour la gestion de l'état du joueur et la génération de choix
    def _update_player_state(self):
        """Met à jour l'état du joueur (faim, fatigue, humeur, etc.)"""
        
        # Vérifier et initialiser les états si nécessaire
        if "states" not in self.player:
            self.player["states"] = {
                "faim": 20,  # 0-100 (0: mourant de faim, 100: plein)
                "fatigue": 20,  # 0-100 (0: exténué, 100: plein d'énergie)
                "moral": 60,  # 0-100 (0: déprimé, 100: extatique)
                "santé": 90,  # 0-100 (0: mourant, 100: parfait)
                "stress": 20,  # 0-100 (0: calme, 100: panique)
                "social": 50,  # 0-100 (0: isolé, 100: bien entouré)
                "activité_actuelle": "éveillé"  # éveillé, sommeil, etc.
            }
        
        # États personnalisés selon l'âge
        player_age = self.player.get("age", 0)
        states = self.player["states"]
        
        # Modifier la fatigue au fil du temps
        current_hour = self.game_time.get("hour", 12)
        
        # Les bébés et jeunes enfants se fatiguent plus vite et ont besoin de siestes
        if player_age < 3:
            # Durée d'éveil pour les bébés
            if states["activité_actuelle"] == "éveillé":
                # La fatigue augmente plus rapidement
                awakeness_penalty = min(3, max(1, 3 - player_age))  # 3 pour nouveau-nés, 2 pour 1 an, 1 pour 2 ans
                states["fatigue"] += awakeness_penalty
                
                # Les bébés ont besoin de siestes fréquentes
                max_awake_time = 2 if player_age < 1 else 4  # heures avant d'avoir besoin d'une sieste
                
                # Si fatigué, proposer une sieste automatiquement
                if states["fatigue"] >= 70 or (states["activité_actuelle"] == "éveillé" and states.get("last_sleep_hour", 0) + max_awake_time <= current_hour):
                    states["activité_actuelle"] = "sommeil"
                    self._add_journal_entry("sleep", f"Vous êtes épuisé et tombez endormi pour une sieste nécessaire...")
                    
        # Les enfants se fatiguent modérément
        elif player_age < 12:
            if states["activité_actuelle"] == "éveillé":
                states["fatigue"] += 0.5
                
        # Les adolescents et adultes se fatiguent normalement
        else:
            if states["activité_actuelle"] == "éveillé":
                states["fatigue"] += 0.3
        
        # Le besoin de dormir la nuit pour tout le monde
        if 22 <= current_hour <= 23 or 0 <= current_hour <= 5:
            states["fatigue"] += 1.0
            
            # Sommeil imposé pour les très jeunes
            if player_age < 6 and 22 <= current_hour and states["activité_actuelle"] != "sommeil":
                states["activité_actuelle"] = "sommeil"
                self._add_journal_entry("sleep", f"Il est tard pour un enfant de votre âge. Vous tombez dans un profond sommeil...")
        
        # Le besoin de manger (toutes les 4-6 heures)
        last_meal = states.get("last_meal_hour", 0)
        hours_since_meal = (current_hour - last_meal) % 24
        
        if hours_since_meal > 4:
            # Plus on attend, plus la faim augmente
            hunger_increase = min(5, hours_since_meal - 3)
            states["faim"] -= hunger_increase
        
        # La soif augmente plus rapidement que la faim
        states["faim"] = max(0, min(100, states["faim"]))
        states["fatigue"] = max(0, min(100, states["fatigue"]))
        
        # Petit feedback sur les besoins physiologiques aigus
        if states["faim"] <= 20 and player_age >= 3:  # Les bébés ne verbalisent pas leur faim
            print("\nVotre estomac gronde. Vous avez besoin de manger bientôt.")
            
        if states["fatigue"] >= 80:
            if player_age < 3:
                print("\nVos paupières sont lourdes. Vous avez besoin de dormir.")
            else:
                print("\nVous vous sentez très fatigué. Vous devriez vous reposer bientôt.")
                
        # Sauvegarder les états modifiés
        self.player["states"] = states
        
        return states
    
    def _generate_contextual_choices(self):
        """Génère des choix d'actions adaptés à l'âge et au contexte actuel"""
        
        player_age = self.player.get("age", 0)
        states = self.player.get("states", {})
        current_location = self.current_location
        location_data = self.locations_data.get(current_location, {})
        time_of_day = "jour" if 6 <= self.game_time["hour"] <= 18 else "nuit"
        
        # Choix disponibles (adaptés à l'âge)
        actions = []
        
        # Actions pour les bébés (0-1 an)
        if player_age < 1:
            # Le gameplay est limité pour un bébé, mais adapté au développement
            actions = [
                "Gazouiller joyeusement",
                "Observer votre environnement avec curiosité",
                "Essayer d'attraper un objet proche",
                "S'endormir paisiblement",
                "Sourire à un visage familier"
            ]
            
            # Ajouter des actions développementales spécifiques selon l'âge en mois
            months = int(player_age * 12)
            if months >= 3:
                actions.append("Rouler sur le côté")
            if months >= 6:
                actions.append("Tenter de s'asseoir")
            if months >= 9:
                actions.append("Essayer de se mettre à quatre pattes")
                actions.append("Babiller des syllabes")
                
        # Actions pour les tout-petits (1-3 ans)
        elif player_age < 3:
            base_actions = [
                "Explorer votre environnement",
                "Jouer avec un jouet",
                "Babiller ou essayer de parler",
                "Faire une sieste",
                "Observer les adultes autour de vous"
            ]
            
            # Ajouter des actions développementales selon l'âge
            if player_age >= 1:
                base_actions.append("Essayer de marcher")
                base_actions.append("Pointer du doigt ce qui vous intéresse")
            if player_age >= 1.5:
                base_actions.append("Empiler des objets")
                base_actions.append("Dire quelques mots simples")
            if player_age >= 2:
                base_actions.append("Courir maladroitement")
                base_actions.append("Participer à un jeu simple")
                base_actions.append("Utiliser des phrases de 2-3 mots")
            
            actions = base_actions
        
        # Actions pour les enfants (3-12 ans)
        elif player_age < 12:
            base_actions = [
                "Explorer les environs",
                "Jouer à un jeu",
                "Parler à quelqu'un",
                "Observer attentivement",
                "Se reposer un moment"
            ]
            
            # Ajouter des actions selon l'âge
            if player_age >= 5:
                base_actions.append("Demander à apprendre quelque chose")
                base_actions.append("Essayer une activité créative")
            if player_age >= 8:
                base_actions.append("Lire un livre simple")
                base_actions.append("Participer à une activité sportive")
            
            # Ajouter des actions selon le lieu
            if "village" in location_data.get("type", "").lower():
                base_actions.append("Visiter une boutique")
                base_actions.append("Parler à un villageois")
            elif "forêt" in location_data.get("type", "").lower():
                base_actions.append("Chercher des baies")
                base_actions.append("Observer les animaux")
            
            actions = base_actions
        
        # Actions pour les adolescents et adultes (12+ ans)
        else:
            base_actions = [
                "Explorer les environs",
                "Engager une conversation",
                "Observer attentivement",
                "Se reposer un moment",
                "Réfléchir à votre situation"
            ]
            
            # Ajouter des actions selon la classe
            player_class = self.player.get("class", "")
            
            if player_class == "Guerrier":
                base_actions.extend([
                    "S'entraîner au combat",
                    "Examiner les défenses du lieu"
                ])
            elif player_class == "Mage":
                base_actions.extend([
                    "Méditer pour restaurer votre mana",
                    "Étudier les flux magiques environnants"
                ])
            elif player_class == "Rôdeur":
                base_actions.extend([
                    "Traquer des empreintes",
                    "Chercher des ressources naturelles"
                ])
            
            # Ajouter des actions selon le lieu
            if "village" in location_data.get("type", "").lower() or "ville" in location_data.get("type", "").lower():
                base_actions.extend([
                    "Visiter le marché",
                    "Chercher des quêtes à la taverne",
                    "Se renseigner auprès des habitants"
                ])
            elif "forêt" in location_data.get("type", "").lower():
                base_actions.extend([
                    "Chercher des herbes médicinales",
                    "Chasser du petit gibier",
                    "Suivre un sentier mystérieux"
                ])
            
            # Ajouter des actions selon l'heure
            if time_of_day == "nuit":
                base_actions.append("Chercher un endroit pour dormir")
                base_actions.append("Monter la garde")
            
            actions = base_actions
        
        # Ajouter des actions contextuelles basées sur les besoins
        if states.get("faim", 50) <= 30 and player_age >= 3:
            actions.append("Chercher de la nourriture")
        if states.get("fatigue", 50) >= 70:
            actions.append("Trouver un endroit pour dormir")
        
        return actions
    
    def _display_contextual_information(self):
        """Affiche les informations contextuelles pertinentes"""
        
        current_location = self.current_location
        location_data = self.locations_data.get(current_location, {})
        location_name = location_data.get("name", "lieu inconnu")
        time_of_day = "jour" if 6 <= self.game_time["hour"] <= 18 else "nuit"
        player_age = self.player.get("age", 0)
        
        # Afficher une description adaptée à l'âge
        if player_age < 1:
            # Pour les bébés, description simplifiée
            print("\n" + "~"*60)
            print(f"Vous êtes dans votre berceau/espace familier.")
            print(f"Il fait {time_of_day}, et il est {self.game_time['hour']:02d}h{self.game_time['minute']:02d}.")
            print("~"*60)
        elif player_age < 5:
            # Pour les jeunes enfants, description simple
            print("\n" + "~"*60)
            print(f"Vous êtes à {location_name}.")
            print(f"Il fait {time_of_day}, et il est {self.game_time['hour']:02d}h{self.game_time['minute']:02d}.")
            print("~"*60)
        else:
            # Pour les plus âgés, plus d'informations
            print("\n" + "~"*60)
            print(f"Vous êtes à {location_name}.")
            print(f"Il fait {time_of_day}, et il est {self.game_time['hour']:02d}h{self.game_time['minute']:02d}.")
            
            # Informations sur l'environnement
            if "type" in location_data:
                print(f"Type d'environnement: {location_data['type']}")
                
            # Informations sur les connexions
            if "connections" in location_data and location_data["connections"]:
                connections_names = []
                for conn_id in location_data["connections"]:
                    conn_name = self.locations_data.get(conn_id, {}).get("name", conn_id)
                    connections_names.append(conn_name)
                print(f"Lieux accessibles: {', '.join(connections_names)}")
            
            # NPCs présents
            if "npcs" in location_data and location_data["npcs"]:
                npc_names = []
                for npc_id in location_data["npcs"]:
                    npc_name = self.character_data.get(npc_id, {}).get("name", npc_id)
                    npc_names.append(npc_name)
                print(f"Personnes présentes: {', '.join(npc_names)}")
            
            print("~"*60)
        
        # Afficher les états importants
        states = self.player.get("states", {})
        
        if player_age >= 3:  # Les tout jeunes enfants ne verbalisent pas leurs besoins de manière aussi explicite
            print("\nVotre état:")
            
            # Faim
            hunger = states.get("faim", 50)
            hunger_state = "Rassasié" if hunger > 80 else "Normal" if hunger > 40 else "Faim" if hunger > 20 else "Affamé"
            print(f"- Faim: {hunger_state}")
            
            # Fatigue
            fatigue = states.get("fatigue", 50)
            fatigue_state = "Reposé" if fatigue < 20 else "Normal" if fatigue < 60 else "Fatigué" if fatigue < 80 else "Épuisé"
            print(f"- Énergie: {fatigue_state}")
            
            # Moral
            mood = states.get("moral", 60)
            mood_state = "Excellent" if mood > 80 else "Bon" if mood > 60 else "Neutre" if mood > 40 else "Bas" if mood > 20 else "Terrible"
            print(f"- Moral: {mood_state}")
        
        return True
# Fin BLOC 23: Méthodes pour la gestion de l'état du joueur et la génération de choix

# BLOC 24: Méthodes pour la gestion de la mémoire et le journal
    def _add_memory(self, category, memory_data):
        """Ajoute un souvenir à la mémoire du personnage"""
        
        if "memories" not in self.player:
            self.player["memories"] = {
                "formative": [],
                "emotional": [],
                "traumatic": [],
                "joyful": [],
                "achievements": []
            }
        
        if category not in self.player["memories"]:
            self.player["memories"][category] = []
        
        # Ajouter un horodatage
        memory_data["timestamp"] = {
            "day": self.game_time.get("day", 1),
            "hour": self.game_time.get("hour", 12),
            "minute": self.game_time.get("minute", 0)
        }
        
        # Ajouter l'âge au moment du souvenir
        memory_data["age_at_memory"] = self.player.get("age", 0)
        
        # Ajouter le souvenir
        self.player["memories"][category].append(memory_data)
        
        # Limiter la taille de chaque catégorie de souvenirs
        max_memories = 10
        if len(self.player["memories"][category]) > max_memories:
            # Trier par impact émotionnel puis supprimer les moins importants
            self.player["memories"][category].sort(key=lambda x: x.get("emotional_impact", 0), reverse=True)
            self.player["memories"][category] = self.player["memories"][category][:max_memories]
        
        return True
    
    def _add_journal_entry(self, entry_type, content):
        """Ajoute une entrée au journal du personnage"""
        
        if "journal" not in self.player:
            self.player["journal"] = []
        
        entry = {
            "type": entry_type,
            "content": content,
            "timestamp": {
                "day": self.game_time.get("day", 1),
                "hour": self.game_time.get("hour", 12),
                "minute": self.game_time.get("minute", 0)
            }
        }
        
        self.player["journal"].append(entry)
        
        # Limiter la taille du journal
        max_entries = 100
        if len(self.player["journal"]) > max_entries:
            self.player["journal"] = self.player["journal"][-max_entries:]
        
        return True
    
    def _check_development_milestone(self):
        """Vérifie si un jalon de développement est atteint pour les jeunes personnages"""
        
        player_age = self.player.get("age", 0)
        if player_age >= 13:
            return False  # Plus de jalons pour les plus âgés
        
        # Jalons de développement par âge (simplifiés)
        milestones = {
            0.25: ["Tenir sa tête", "Sourire intentionnellement"],
            0.5: ["Se retourner", "Gazouiller"],
            0.75: ["S'asseoir avec soutien", "Babiller"],
            1.0: ["Se tenir debout avec soutien", "Dire ses premiers mots"],
            1.5: ["Marcher seul", "Utiliser une cuillère"],
            2.0: ["Courir", "Phrases de 2 mots"],
            3.0: ["Sauter", "Phrases complètes", "Dessiner des formes"],
            4.0: ["Sauter à cloche-pied", "Raconter une histoire"],
            5.0: ["Débuter apprentissage lecture", "Compter jusqu'à 20"],
            6.0: ["Lire des mots simples", "Nouer ses lacets"],
            8.0: ["Lire des phrases", "Logique simple", "Jeux de règles"],
            10.0: ["Pensée abstraite", "Lecture fluide", "Sens critique"]
        }
        
        # Trouver le prochain jalon à atteindre
        next_milestone = None
        next_age = 100  # Valeur arbitraire élevée
        
        for age, milestone_list in milestones.items():
            if player_age < age < next_age:
                next_milestone = milestone_list
                next_age = age
        
        # Si pas de prochain jalon ou dernier
        if next_milestone is None:
            return False
        
        # 10% de chance de déclencher un jalon si l'âge est proche
        if random.random() < 0.1 and next_age - player_age < 0.1:
            chosen_milestone = random.choice(next_milestone)
            
            milestone_context = {
                "player_data": self.player,
                "milestone": chosen_milestone,
                "age": player_age
            }
            
            milestone_prompt = (
                f"Décris un moment important où {self.player['name']}, âgé de {player_age:.1f} ans, "
                f"atteint le jalon de développement: '{chosen_milestone}'. "
                f"Raconte cette petite victoire développementale de façon touchante et immersive, "
                f"à la deuxième personne du singulier. Capture l'émotion et la fierté de ce moment."
            )
            
            try:
                logger.info(f"Jalon de développement: {chosen_milestone}")
                milestone_description = self.ai_manager.generate_response(milestone_prompt, milestone_context)
                
                print("\n" + "✨"*30)
                print("JALON DE DÉVELOPPEMENT".center(60))
                print("-"*60)
                print(milestone_description)
                print("✨"*30)
                
                # Ajouter aux souvenirs formatifs
                self._add_memory("formative", {
                    "description": f"Premier(e) {chosen_milestone}",
                    "content": milestone_description,
                    "emotional_impact": 0.9  # Forte impact émotionnel
                })
                
                # Ajouter au journal
                self._add_journal_entry("milestone", milestone_description)
                
                # Améliorer une compétence liée
                skill_name = self._milestone_to_skill(chosen_milestone)
                if skill_name:
                    self._improve_skill_by_use(skill_name, 2.0)  # Boost significatif
                
                return True
            except Exception as e:
                logger.error(f"Erreur lors de la génération du jalon de développement: {e}")
                return False
            
        return False
    
    def _milestone_to_skill(self, milestone):
        """Convertit un jalon de développement en nom de compétence associée"""
        
        milestone_lower = milestone.lower()
        
        # Mappings simples
        if "tête" in milestone_lower:
            return "Contrôle musculaire"
        elif "sourire" in milestone_lower:
            return "Expression émotionnelle"
        elif "retourner" in milestone_lower:
            return "Mobilité"
        elif "gazouiller" in milestone_lower or "babiller" in milestone_lower:
            return "Communication pré-verbale"
        elif "asseoir" in milestone_lower:
            return "Équilibre"
        elif "mot" in milestone_lower:
            return "Langage"
        elif "marcher" in milestone_lower:
            return "Bipédie"
        elif "cuillère" in milestone_lower:
            return "Motricité fine"
        elif "courir" in milestone_lower:
            return "Motricité globale"
        elif "phrases" in milestone_lower:
            return "Communication verbale"
        elif "dessin" in milestone_lower:
            return "Expression artistique"
        elif "sauter" in milestone_lower:
            return "Coordination"
        elif "histoire" in milestone_lower:
            return "Narration"
        elif "lecture" in milestone_lower or "lire" in milestone_lower:
            return "Lecture"
        elif "compter" in milestone_lower:
            return "Calcul"
        elif "lacets" in milestone_lower:
            return "Dextérité manuelle"
        elif "logique" in milestone_lower:
            return "Raisonnement"
        elif "règles" in milestone_lower:
            return "Compréhension sociale"
        elif "abstraite" in milestone_lower:
            return "Pensée abstraite"
        elif "critique" in milestone_lower:
            return "Esprit critique"
            
        # Par défaut
        return "Développement"
# Fin BLOC 24: Méthodes pour la gestion de la mémoire et le journal

# BLOC 25: Méthodes d'affichage d'informations et point d'entrée du programme
    def show_character_stats(self):
        """Affiche les statistiques du personnage"""
        
        print("\n" + "="*60)
        print("STATISTIQUES DU PERSONNAGE".center(60))
        print("="*60)
        
        race_display_name = self._get_display_race_name(self.player.get("race", ""))
        print(f"Nom: {self.player['name']}")
        print(f"Âge: {self.player['age']} an{'s' if self.player['age'] > 1 else ''}")
        print(f"Race: {race_display_name}")
        print(f"Classe: {self.player.get('class', 'Sans classe')}")
        
        if "stats" in self.player:
            print("\nAttributs:")
            for attr, value in self.player["stats"].items():
                print(f"- {attr.capitalize()}: {value:.1f}")
        
        if "skills" in self.player:
            print("\nCompétences:")
            for skill in self.player["skills"]:
                if isinstance(skill, dict):
                    print(f"- {skill['name']}: Niveau {skill.get('level', 1)} ({skill.get('exp', 0):.1f}/{10 * (skill.get('level', 1) ** 1.5):.1f} XP)")
                else:
                    print(f"- {skill}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def show_relationships(self):
        """Affiche les relations du personnage avec les autres personnages"""
        
        print("\n" + "="*60)
        print("RELATIONS".center(60))
        print("="*60)
        
        if "relationships" not in self.player or not self.player["relationships"]:
            print("Vous n'avez pas encore établi de relations significatives.")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        # Afficher d'abord les membres de la famille
        if "family_members" in self.player:
            print("Famille:")
            for member in self.player["family_members"]:
                relation = self.player["relationships"].get(member["id"], {"affinity": 50, "trust": 50, "familiarity": 50})
                affinity = relation.get("affinity", 50)
                relationship_quality = "Excellente" if affinity > 80 else "Bonne" if affinity > 60 else "Neutre" if affinity > 40 else "Tendue" if affinity > 20 else "Hostile"
                print(f"- {member['name']} ({member['relation']}): Relation {relationship_quality}")
            print("")
        
        # Afficher autres relations
        print("Autres relations:")
        other_shown = False
        
        for npc_id, relation in self.player["relationships"].items():
            # Vérifier si c'est un membre de la famille (déjà affiché)
            is_family = False
            if "family_members" in self.player:
                for member in self.player["family_members"]:
                    if member["id"] == npc_id:
                        is_family = True
                        break
            
            # Si ce n'est pas un membre de la famille, l'afficher
            if not is_family:
                other_shown = True
                npc_name = npc_id  # Par défaut
                
                # Essayer de trouver le nom réel du PNJ
                for character_id, character_data in self.character_data.items():
                    if character_id == npc_id:
                        npc_name = character_data.get("name", npc_id)
                        break
                
                affinity = relation.get("affinity", 50)
                trust = relation.get("trust", 50)
                familiarity = relation.get("familiarity", 10)
                
                relationship_quality = "Excellente" if affinity > 80 else "Bonne" if affinity > 60 else "Neutre" if affinity > 40 else "Tendue" if affinity > 20 else "Hostile"
                trust_level = "Totale" if trust > 80 else "Élevée" if trust > 60 else "Moyenne" if trust > 40 else "Faible" if trust > 20 else "Aucune"
                familiarity_level = "Intime" if familiarity > 80 else "Proche" if familiarity > 60 else "Connaissance" if familiarity > 40 else "Lointaine" if familiarity > 20 else "Étranger"
                
                print(f"- {npc_name}: Relation {relationship_quality}, Confiance {trust_level}, Familiarité {familiarity_level}")
        
        if not other_shown and "family_members" not in self.player:
            print("Aucune relation établie pour l'instant.")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def show_journal(self):
        """Affiche le journal du personnage"""
        
        print("\n" + "="*60)
        print("JOURNAL".center(60))
        print("="*60)
        
        if "journal" not in self.player or not self.player["journal"]:
            print("Votre journal est vide pour l'instant.")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        # Trier les entrées par date
        sorted_entries = sorted(self.player["journal"], 
                              key=lambda x: (x.get("timestamp", {}).get("day", 0), 
                                            x.get("timestamp", {}).get("hour", 0),
                                            x.get("timestamp", {}).get("minute", 0)))
        
        # Afficher les 10 dernières entrées (ou moins s'il y en a moins)
        display_entries = sorted_entries[-10:]  # Dernières 10 entrées
        
        for entry in display_entries:
            timestamp = entry.get("timestamp", {})
            day = timestamp.get("day", 1)
            hour = timestamp.get("hour", 12)
            minute = timestamp.get("minute", 0)
            
            entry_type = entry.get("type", "note").capitalize()
            
            print(f"\nJour {day}, {hour:02d}h{minute:02d} - {entry_type}")
            print("-"*50)
            
            # Afficher un extrait du contenu (limiter à 200 caractères)
            content = entry.get("content", "")
            if len(content) > 200:
                print(content[:200] + "...")
            else:
                print(content)
        
        # Option pour voir plus d'entrées
        print("\n1. Voir toutes les entrées")
        print("2. Retour")
        
        choice = self._get_numeric_choice(1, 2)
        
        if choice == 1:
            # Afficher toutes les entrées page par page
            entries_per_page = 3
            total_pages = (len(sorted_entries) + entries_per_page - 1) // entries_per_page
            current_page = 1
            
            while True:
                print("\n" + "="*60)
                print(f"JOURNAL (Page {current_page}/{total_pages})".center(60))
                print("="*60)
                
                start_idx = (current_page - 1) * entries_per_page
                end_idx = min(start_idx + entries_per_page, len(sorted_entries))
                page_entries = sorted_entries[start_idx:end_idx]
                
                for entry in page_entries:
                    timestamp = entry.get("timestamp", {})
                    day = timestamp.get("day", 1)
                    hour = timestamp.get("hour", 12)
                    minute = timestamp.get("minute", 0)
                    
                    entry_type = entry.get("type", "note").capitalize()
                    
                    print(f"\nJour {day}, {hour:02d}h{minute:02d} - {entry_type}")
                    print("-"*50)
                    print(entry.get("content", ""))
                
                if current_page < total_pages:
                    print("\n1. Page suivante")
                else:
                    print("\n1. Première page")
                    
                print("2. Retour")
                
                choice = self._get_numeric_choice(1, 2)
                
                if choice == 1:
                    # Passer à la page suivante ou revenir au début
                    if current_page < total_pages:
                        current_page += 1
                    else:
                        current_page = 1
                else:
                    break
        
        return


# Lancement du jeu si exécuté comme script principal
if __name__ == "__main__":
    game = MuskoTenseiRP()
    game.start()
# Fin BLOC 25: Méthodes d'affichage d'informations et point d'entrée du programme