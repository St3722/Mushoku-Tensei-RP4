# main.py dans le dossier modules - imports corrigés
import os
import sys
import time
import random
import json
from typing import Dict, List, Any, Optional

# Ajoutez le répertoire racine du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Option 1: Imports relatifs (fonctionne quand on exécute depuis le dossier modules)
from modules.save_manager import SaveManager
from ai_manager import AIManager
from modules.character_progression import CharacterProgression 
from modules.interface_cli import InterfaceCLI

class MuskoTenseiRP:
    """Classe principale du jeu MUSKO TENSEI RP"""
    
    def __init__(self):
        """Initialise le jeu et charge les données nécessaires"""
        self.version = "1.0.0"
        
        # Initialiser l'interface
        self.ui = InterfaceCLI(self)
        
        # Afficher l'écran de chargement
        self.ui.display_loading_screen("Initialisation du monde...")
        
        # Charger les données de base
        self.load_game_data()
        
        # Initialiser les gestionnaires
        self.ai_manager = AIManager()
        self.save_manager = SaveManager(self)
        self.character_progression = CharacterProgression(self)
        
        # État du jeu
        self.running = True
        self.current_location = "starting_town"
        self.time_of_day = "day"
        self.day_count = 1
        self.season = "spring"
        self.weather = "clear"
        self.discovered_locations = ["starting_town"]
        
        # Données du joueur (initialisées à une valeur par défaut)
        self.player = {
            "name": "Aventurier",
            "class": "fighter",
            "level": 1,
            "xp": 0,
            "attributes": {
                "strength": 10,
                "dexterity": 10,
                "constitution": 10,
                "intelligence": 10,
                "wisdom": 10,
                "charisma": 10,
                "perception": 10
            },
            "current_hp": 100,
            "max_hp": 100,
            "current_mp": 50,
            "max_mp": 50,
            "attribute_points": 0,
            "skill_points": 0,
            "gold": 100,
            "learned_skills": {},
            "equipment": {},
            "inventory": []
        }
        
        # Quêtes et relations
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
        self.quest_states = {}
        self.relationships = {}
        
        # Statistiques de jeu
        self.game_stats = {
            "enemies_defeated": 0,
            "quests_completed": 0,
            "items_collected": 0,
            "money_earned": 0,
            "money_spent": 0,
            "distance_traveled": 0,
            "spells_cast": 0,
            "skill_uses": 0
        }
        
        # Drapeaux de jeu (pour suivre les choix et événements)
        self.game_flags = {}
    
def load_game_data(self):
    """Charge toutes les données statiques du jeu"""
    try:
        # Chemin vers le dossier data (un niveau au-dessus du dossier modules)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        
        # Charger les données des lieux
        with open(os.path.join(data_dir, "locations.json"), "r", encoding="utf-8") as f:
            self.location_data = json.load(f)
        
        # Charger les données des PNJ
        with open(os.path.join(data_dir, "npcs.json"), "r", encoding="utf-8") as f:
            self.npc_data = json.load(f)
        
        # Charger les données des objets
        with open(os.path.join(data_dir, "items.json"), "r", encoding="utf-8") as f:
            self.item_data = json.load(f)
        
        # Charger les données des compétences
        with open(os.path.join(data_dir, "skills.json"), "r", encoding="utf-8") as f:
            self.skills_data = json.load(f)
        
        # Charger les données des quêtes
        with open(os.path.join(data_dir, "quests.json"), "r", encoding="utf-8") as f:
            self.quests_data = json.load(f)
            
        # Charger les données de combat
        with open(os.path.join(data_dir, "combat.json"), "r", encoding="utf-8") as f:
            self.combat_data = json.load(f)
            
        print("Toutes les données du jeu ont été chargées avec succès!")
        
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        sys.exit(1)
    
    def start(self):
        """Démarre le jeu"""
        # Afficher l'écran d'accueil
        self.ui.display_splash_screen()
        
        # Menu principal
        self.show_main_menu()
    
    def show_main_menu(self):
        """Affiche le menu principal du jeu"""
        while self.running:
            options = [
                ("Nouvelle partie", "new_game"),
                ("Charger une partie", "load_game"),
                ("Options", "options"),
                ("À propos", "about"),
                ("Quitter", "quit")
            ]
            
            choice = self.ui.display_menu("MUSKO TENSEI RP", options)
            
            if choice == "new_game":
                self.new_game()
            elif choice == "load_game":
                self.load_game()
            elif choice == "options":
                self.show_options()
            elif choice == "about":
                self.show_about()
            elif choice == "quit":
                self.quit_game()
    
    def new_game(self):
        """Commence une nouvelle partie"""
        # Vérifier l'âge pour le contenu mature
        self.check_mature_content()
        
        # Afficher l'introduction du jeu
        self.ui.clear_screen()
        intro_text = """
Dans un flash de douleur et de confusion, vos derniers souvenirs de votre ancienne vie s'estompent.
Puis, une lumière chaude et douce vous enveloppe...

Vous êtes né dans un monde nouveau. Un monde de magie, d'épées et de fantaisie.
Une seconde chance vous est offerte - celle de vivre une vie extraordinaire, 
de forger votre destin selon vos propres termes.

Bienvenue dans le monde de Mushoku Tensei.
        """
        self.ui.print_text(intro_text, color='normal', slow=True)
        self.ui.get_user_input("Appuyez sur Entrée pour continuer...")
        
        # Création du personnage
        self.create_character()
        
        # Démarrer le jeu proprement dit
        self.game_loop()
    
    def check_mature_content(self):
        """Vérifie si le joueur souhaite activer le contenu mature"""
        self.ui.print_header("Contenu Mature", "Avertissement")
        
        warning_text = """
Ce jeu peut contenir du contenu mature, incluant:

- Violence et combats détaillés
- Langage adulte
- Thèmes romantiques et situations intimes
- Sujets sensibles ou controversés

Vous pouvez personnaliser le niveau de contenu mature dans les options.
        """
        self.ui.print_text(warning_text, color='warning')
        
        options = [
            ("Activer le contenu mature (18+ ans seulement)", True),
            ("Désactiver le contenu mature", False)
        ]
        
        mature_content = self.ui.display_menu("Souhaitez-vous activer le contenu mature?", options)
        
        # Initialiser le gestionnaire de contenu mature
        if hasattr(self, 'mature_content_manager'):
            self.mature_content_manager.verify_age(mature_content)
        else:
            # Si le module n'est pas encore importé, stocker le choix
            self.mature_content_enabled = mature_content
    
    def create_character(self):
        """Interface de création de personnage"""
        # Charger les classes disponibles
        available_classes = [
            {
                "id": "warrior",
                "name": "Guerrier",
                "description": "Spécialistes du combat rapproché, les guerriers excellent dans le maniement des armes et la résistance physique."
            },
            {
                "id": "mage",
                "name": "Mage",
                "description": "Maîtres de la magie élémentaire, les mages peuvent lancer des sorts puissants mais sont fragiles physiquement."
            },
            {
                "id": "rogue",
                "name": "Voleur",
                "description": "Agiles et furtifs, les voleurs excellent dans les attaques rapides et précises, ainsi que dans diverses compétences utilitaires."
            },
            {
                "id": "priest",
                "name": "Prêtre",
                "description": "Bénis par les dieux, les prêtres peuvent guérir leurs alliés et invoquer des pouvoirs divins contre leurs ennemis."
            }
        ]
        
        # Liste des attributs
        available_attributes = [
            {
                "id": "strength",
                "name": "Force",
                "description": "Détermine les dégâts physiques et la capacité à porter des charges lourdes."
            },
            {
                "id": "dexterity",
                "name": "Dextérité",
                "description": "Affecte la précision, l'esquive et les attaques rapides."
            },
            {
                "id": "constitution",
                "name": "Constitution",
                "description": "Augmente les points de vie et la résistance aux maladies et poisons."
            },
            {
                "id": "intelligence",
                "name": "Intelligence",
                "description": "Influence la puissance magique et la capacité d'apprentissage."
            },
            {
                "id": "wisdom",
                "name": "Sagesse",
                "description": "Améliore la perception, l'intuition et la régénération de mana."
            },
            {
                "id": "charisma",
                "name": "Charisme",
                "description": "Affecte les interactions sociales et les prix chez les marchands."
            },
            {
                "id": "perception",
                "name": "Perception",
                "description": "Permet de repérer les pièges, objets cachés et détails subtils."
            }
        ]
        
        # Lancer l'interface de création
        character_choices = self.ui.display_character_creation(available_classes, available_attributes)
        
        # Mettre à jour les données du joueur
        self.player["name"] = character_choices["name"]
        self.player["class"] = character_choices["class"]
        self.player["attributes"] = character_choices["attributes"]
        
        # Initialiser les statistiques dérivées
        self.character_progression.update_derived_stats(self.player)
        self.character_progression.update_base_stats(self.player)
    
    def load_game(self):
        """Charge une partie sauvegardée"""
        # Lister les sauvegardes disponibles
        save_slots = self.save_manager.list_saves()
        
        if not save_slots:
            self.ui.display_notification("Aucune sauvegarde disponible.", type="info")
            return
        
        # Afficher le menu de chargement
        load_result = self.ui.display_save_load_menu(save_slots)
        
        if load_result["action"] == "load" and "slot" in load_result:
            slot_index = load_result["slot"]
            if 0 <= slot_index < len(save_slots):
                save_path = save_slots[slot_index]["file_path"]
                
                # Afficher un écran de chargement
                self.ui.display_loading_screen("Chargement de la sauvegarde...")
                
                # Charger la sauvegarde
                load_result = self.save_manager.load_game(save_path)
                
                if load_result["success"]:
                    self.ui.display_notification("Partie chargée avec succès!", type="success", dismiss_after=1)
                    self.game_loop()
                else:
                    self.ui.display_notification(f"Erreur lors du chargement: {load_result['message']}", type="error")
    
    def show_options(self):
        """Affiche le menu des options"""
        while True:
            options = [
                ("Paramètres d'affichage", "display"),
                ("Paramètres de contenu mature", "mature"),
                ("Paramètres de jeu", "gameplay"),
                ("Retour au menu principal", "back")
            ]
            
            choice = self.ui.display_menu("Options", options)
            
            if choice == "display":
                self.show_display_options()
            elif choice == "mature":
                self.show_mature_options()
            elif choice == "gameplay":
                self.show_gameplay_options()
            elif choice == "back":
                break
    
    def show_display_options(self):
        """Affiche les options d'affichage"""
        options = [
            (f"Vitesse du texte: {self.ui.text_speed:.2f}s", "text_speed"),
            (f"Effacement automatique de l'écran: {'Activé' if self.ui.auto_clear else 'Désactivé'}", "auto_clear"),
            (f"Afficher les astuces: {'Activé' if self.ui.show_hints else 'Désactivé'}", "show_hints"),
            (f"Utiliser les émojis: {'Activé' if self.ui.use_emojis else 'Désactivé'}", "use_emojis"),
            ("Retour", "back")
        ]
        
        while True:
            choice = self.ui.display_menu("Paramètres d'affichage", options)
            
            if choice == "text_speed":
                speeds = [
                    ("Instantané", 0),
                    ("Très rapide", 0.01),
                    ("Rapide", 0.02),
                    ("Normal", 0.03),
                    ("Lent", 0.05),
                    ("Très lent", 0.08)
                ]
                new_speed = self.ui.display_menu("Choisissez la vitesse du texte", speeds)
                self.ui.text_speed = new_speed
                
                # Mettre à jour l'option dans le menu
                options[0] = (f"Vitesse du texte: {self.ui.text_speed:.2f}s", "text_speed")
                
            elif choice == "auto_clear":
                self.ui.auto_clear = not self.ui.auto_clear
                options[1] = (f"Effacement automatique de l'écran: {'Activé' if self.ui.auto_clear else 'Désactivé'}", "auto_clear")
                
            elif choice == "show_hints":
                self.ui.show_hints = not self.ui.show_hints
                options[2] = (f"Afficher les astuces: {'Activé' if self.ui.show_hints else 'Désactivé'}", "show_hints")
                
            elif choice == "use_emojis":
                self.ui.use_emojis = not self.ui.use_emojis
                options[3] = (f"Utiliser les émojis: {'Activé' if self.ui.use_emojis else 'Désactivé'}", "use_emojis")
                
            elif choice == "back":
                break
    
    def show_mature_options(self):
        """Affiche les options de contenu mature"""
        # Vérifier si le gestionnaire de contenu mature est initialisé
        if not hasattr(self, 'mature_content_manager'):
            self.ui.display_notification("Les options de contenu mature ne sont pas disponibles actuellement.", type="info")
            return
            
        # Obtenir les niveaux actuels
        filters = self.mature_content_manager.player_preferences["filters"]
        
        options = [
            (f"Contenu violent: {filters['violence']}", "violence"),
            (f"Contenu intime: {filters['sexual_content']}", "sexual_content"),
            (f"Langage: {filters['language']}", "language"),
            (f"Thèmes controversés: {filters['controversial_themes']}", "controversial"),
            (f"Système de consentement: {'Activé' if self.mature_content_manager.player_preferences['consent_system_enabled'] else 'Désactivé'}", "consent"),
            ("Retour", "back")
        ]
        
        while True:
            choice = self.ui.display_menu("Paramètres de contenu mature", options)
            
            if choice == "back":
                break
            elif choice == "consent":
                # Inverser l'état du système de consentement
                consent_enabled = not self.mature_content_manager.player_preferences["consent_system_enabled"]
                result = self.mature_content_manager.set_consent_system(consent_enabled)
                
                if result["success"]:
                    options[4] = (f"Système de consentement: {'Activé' if consent_enabled else 'Désactivé'}", "consent")
                    
                    if "warning" in result and result["warning"]:
                        self.ui.display_notification(result["warning"], type="warning")
                else:
                    self.ui.display_notification(result["message"], type="error")
            else:
                # Gérer les niveaux de filtres
                filter_levels = self.mature_content_manager.content_data.get("settings", {}).get("content_filters", {}).get(choice, {}).get("options", [])
                
                if filter_levels:
                    level_options = [(level, level) for level in filter_levels]
                    new_level = self.ui.display_menu(f"Niveau de {choice}", level_options)
                    
                    result = self.mature_content_manager.set_content_filter(choice, new_level)
                    
                    if result["success"]:
                        # Mettre à jour l'option dans le menu
                        filter_index = {"violence": 0, "sexual_content": 1, "language": 2, "controversial": 3}.get(choice, 0)
                        options[filter_index] = (f"Contenu {choice}: {new_level}", choice)
                        
                        if "warning" in result and result["warning"]:
                            self.ui.display_notification(result["warning"], type="warning")
                    else:
                        self.ui.display_notification(result["message"], type="error")
    
    def show_gameplay_options(self):
        """Affiche les options de gameplay"""
        options = [
            ("Difficulté", "difficulty"),
            ("Audio", "audio"),
            ("Contrôles", "controls"),
            ("Retour", "back")
        ]
        
        choice = self.ui.display_menu("Paramètres de jeu", options)
        
        # Pour l'instant, ces options sont des placeholders
        if choice != "back":
            self.ui.display_notification("Cette fonctionnalité sera disponible dans une future mise à jour.", type="info")
    
    def show_about(self):
        """Affiche les informations sur le jeu"""
        about_text = f"""
MUSKO TENSEI RP

Version: {self.version}

Un jeu de rôle textuel inspiré par Mushoku Tensei: Jobless Reincarnation.

Développé par: St3722

Ce jeu utilise les technologies suivantes:
- Python (programmation)
- LM Studio & Mistral-7b (IA narrative)

Remerciements:
- À tous les fans de Mushoku Tensei
- À la communauté du développement de jeux indépendants
        """
        
        self.ui.display_description(about_text, title="À propos", color="info")
        self.ui.get_user_input("Appuyez sur Entrée pour revenir au menu...")
    
    def quit_game(self):
        """Quitte le jeu proprement"""
        self.ui.clear_screen()
        self.ui.print_text("Merci d'avoir joué à MUSKO TENSEI RP!", color='highlight', center=True)
        self.ui.print_text("À bientôt pour de nouvelles aventures...", color='normal', center=True)
        
        time.sleep(1.5)
        self.running = False
        sys.exit(0)
    
    def game_loop(self):
        """Boucle principale du jeu"""
        self.running = True
        
        # Afficher la description initiale
        self.display_current_location()
        
        while self.running:
            # Afficher les informations de base
            self.ui.print_player_stats()
            self.ui.print_location_info()
            
            # Obtenir la commande du joueur
            command = self.ui.get_user_input("> ")
            
            # Traiter la commande
            if command.lower() in ["q", "quit", "exit"]:
                self.running = False
            elif command.lower() in ["h", "help", "aide"]:
                self.show_help()
            elif command.lower() in ["i", "inv", "inventory"]:
                self.show_inventory()
            elif command.lower() in ["s", "skills", "competences"]:
                self.show_skills()
            elif command.lower() in ["m", "map", "carte"]:
                self.show_map()
            elif command.lower() in ["j", "journal", "quests"]:
                self.show_quests()
            elif command.lower() in ["save", "sauvegarder"]:
                self.save_game()
            elif command.lower() in ["load", "charger"]:
                self.load_game_menu()
            else:
                # Analyser l'intention de la commande
                self.process_command(command)
            
            # Auto-sauvegarde périodique (toutes les 10 minutes de jeu par exemple)
            # À implémenter plus tard
    
    def process_command(self, command: str):
        """
        Traite une commande du joueur et détermine l'action à effectuer
        
        Args:
            command: Commande saisie par le joueur
        """
        # Analyser l'intention avec l'IA
        intent = self.ai_manager.analyze_intent(command)
        intent_type = intent.get("type", "dialogue")
        
        # Traiter l'intention
        if intent_type == "movement":
            self.handle_movement(intent)
        elif intent_type == "dialogue":
            self.handle_dialogue(intent, command)
        elif intent_type == "combat":
            self.handle_combat(intent)
        elif intent_type == "examine":
            self.handle_examine(intent, command)
        elif intent_type == "inventory":
            self.handle_inventory_action(intent)
        elif intent_type == "market":
            self.handle_market(intent)
        elif intent_type == "intimate":
            self.handle_intimate(intent, command)
        else:
            # Si aucune intention claire n'est détectée, traiter comme un dialogue général
            # ou afficher un message d'aide
            self.ui.display_notification("Je ne comprends pas cette commande. Tapez 'aide' pour voir les commandes disponibles.", type="info")
    
    def display_current_location(self):
        """Affiche la description du lieu actuel"""
        location_id = self.current_location
        location_data = self.location_data.get(location_id, {})
        
        if not location_data:
            self.ui.display_notification(f"Erreur: Lieu {location_id} introuvable.", type="error")
            return
            
        # Obtenir les informations de base
        name = location_data.get("name", "Lieu inconnu")
        
        # Générer une description immersive avec l'IA
        description = self.ai_manager.generate_description(
            location_id, 
            self.time_of_day, 
            self.weather
        )
        
        # Afficher la description
        self.ui.display_description(description, title=name)
    
    def handle_movement(self, intent: Dict[str, Any]):
        """
        Gère les déplacements du joueur
        
        Args:
            intent: Intention analysée du joueur
        """
        # Extraire la destination souhaitée
        destination = intent.get("params", {}).get("destination", "").lower()
        
        if not destination:
            self.ui.display_notification("Où souhaitez-vous aller?", type="info")
            return
        
        # Récupérer les destinations possibles depuis le lieu actuel
        current_location = self.location_data.get(self.current_location, {})
        exits = current_location.get("exits", {})
        
        # Vérifier si la destination est accessible
        destination_id = None
        
        for exit_id, exit_data in exits.items():
            exit_name = exit_data.get("name", "").lower()
            
            if destination in exit_name or destination == exit_id.lower():
                destination_id = exit_id
                break
        
        if not destination_id:
            self.ui.display_notification(f"Vous ne pouvez pas aller à '{destination}' depuis ici.", type="warning")
            return
            
        # Vérifier les conditions éventuelles (à implémenter plus tard)
        # Par exemple: vérifier si le joueur a la clé pour une porte verrouillée
        
        # Effectuer le déplacement
        self.ui.display_loading_screen(f"Vous vous rendez à {exits[destination_id]['name']}...")
        
        # Mettre à jour la position
        self.current_location = destination_id
        
        # Si c'est un nouveau lieu, l'ajouter aux lieux découverts
        if destination_id not in self.discovered_locations:
            self.discovered_locations.append(destination_id)
        
        # Afficher la description du nouveau lieu
        self.display_current_location()
    
    def handle_dialogue(self, intent: Dict[str, Any], command: str):
        """
        Gère les dialogues avec les PNJ
        
        Args:
            intent: Intention analysée du joueur
            command: Commande originale du joueur
        """
        # Extraire la cible du dialogue
        target = intent.get("params", {}).get("target", "").lower()
        
        if not target:
            self.ui.display_notification("Avec qui voulez-vous parler?", type="info")
            return
        
        # Chercher le PNJ dans le lieu actuel
        current_location = self.location_data.get(self.current_location, {})
        npcs = current_location.get("npcs", [])
        
        npc_id = None
        npc_data = None
        
        for npc in npcs:
            npc_info = self.npc_data.get(npc, {})
            npc_name = npc_info.get("name", "").lower()
            
            if target in npc_name or target == npc.lower():
                npc_id = npc
                npc_data = npc_info
                break
        
        if not npc_id:
            self.ui.display_notification(f"Il n'y a personne qui s'appelle '{target}' ici.", type="warning")
            return
        
        # Déterminer le type de dialogue
        dialogue_type = "greeting"
        if "topic" in intent.get("params", {}):
            topic = intent["params"]["topic"].lower()
            if "quête" in topic or "mission" in topic:
                dialogue_type = "quest"
            elif "achat" in topic or "vend" in topic or "prix" in topic:
                dialogue_type = "trade"
            elif "rumeur" in topic or "info" in topic or "nouvelle" in topic:
                dialogue_type = "info"
        
        # Générer le dialogue avec l'IA
        response = self.ai_manager.generate_npc_dialogue(
            npc_id, 
            dialogue_type, 
            command, 
            {
                "location_id": self.current_location,
                "time_of_day": self.time_of_day,
                "weather": self.weather
            }
        )
        
        # Afficher le dialogue
        npc_name = npc_data.get("name", "NPC")
        npc_mood = npc_data.get("default_mood", "neutral")
        
        # Obtenir l'avatar si disponible
        avatar = npc_data.get("avatar_ascii", None)
        
        self.ui.display_dialogue(npc_name, response, npc_mood, avatar)
    
    def handle_combat(self, intent: Dict[str, Any]):
        """
        Gère les combats
        
        Args:
            intent: Intention analysée du joueur
        """
        # Extraire la cible du combat
        target = intent.get("params", {}).get("target", "").lower()
        
        if not target:
            self.ui.display_notification("Qui voulez-vous attaquer?", type="info")
            return
        
        # Chercher l'ennemi dans le lieu actuel
        current_location = self.location_data.get(self.current_location, {})
        enemies = current_location.get("enemies", [])
        
        enemy_id = None
        enemy_data = None
        
        for enemy in enemies:
            enemy_info = self.npc_data.get(enemy, {})
            enemy_name = enemy_info.get("name", "").lower()
            
            if target in enemy_name or target == enemy.lower():
                enemy_id = enemy
                enemy_data = enemy_info
                break
        
        if not enemy_id:
            self.ui.display_notification(f"Il n'y a pas d'ennemi nommé '{target}' ici.", type="warning")
            return
        
        # Initialiser le combat
        self.start_combat(enemy_id)
    
    def start_combat(self, enemy_id: str):
        """
        Initialise et gère un combat complet
        
        Args:
            enemy_id: ID de l'ennemi à combattre
        """
        # Récupérer les données de l'ennemi
        enemy_data = self.npc_data.get(enemy_id, {})
        enemy_name = enemy_data.get("name", "Ennemi")
        
        # Créer les stats de combat de l'ennemi
        enemy_stats = {
            "name": enemy_name,
            "id": enemy_id,
            "level": enemy_data.get("level", 1),
            "current_hp": enemy_data.get("hp", 100),
            "max_hp": enemy_data.get("hp", 100),
            "attack": enemy_data.get("attack", 10),
            "defense": enemy_data.get("defense", 5),
            "speed": enemy_data.get("speed", 10),
            "skills": enemy_data.get("skills", [])
        }
        
        # Initialiser le journal de combat
        combat_log = [
            f"Un combat commence entre vous et {enemy_name}!"
        ]
        
        # Déterminer qui agit en premier
        player_speed = self.player.get("attributes", {}).get("dexterity", 10)
        enemy_speed = enemy_stats["speed"]
        
        player_first = player_speed >= enemy_speed
        
        # Boucle de combat
        combat_active = True
        turn_count = 0
        
        while combat_active:
            turn_count += 1
            
            # Mettre à jour l'interface de combat
            available_actions = self._get_combat_actions()
            
            self.ui.display_combat_interface(
                self.player, 
                enemy_stats, 
                combat_log,
                available_actions
            )
            
            # Tour du joueur (s'il agit en premier ou si ce n'est pas le premier tour)
            if player_first or turn_count > 1:
                # Demander l'action du joueur
                action_choice = self.ui.get_user_input("Action: ")
                
                try:
                    action_index = int(action_choice) - 1
                    if 0 <= action_index < len(available_actions):
                        action = available_actions[action_index]
                        combat_result = self._process_combat_action(action, enemy_stats)
                        
                        # Ajouter le résultat au journal
                        combat_log.append(combat_result["message"])
                        
                        # Appliquer les dégâts
                        enemy_stats["current_hp"] -= combat_result.get("damage", 0)
                        
                        # Vérifier si l'ennemi est vaincu
                        if enemy_stats["current_hp"] <= 0:
                            enemy_stats["current_hp"] = 0
                            combat_log.append(f"Vous avez vaincu {enemy_name}!")
                            combat_active = False
                            break
                    else:
                        combat_log.append("Action invalide.")
                except ValueError:
                    combat_log.append("Veuillez entrer un numéro d'action valide.")
            
            # Tour de l'ennemi
            if combat_active:
                enemy_action = self._get_enemy_action(enemy_stats)
                enemy_result = self._process_enemy_action(enemy_action, enemy_stats)
                
                # Ajouter le résultat au journal
                combat_log.append(enemy_result["message"])
                
                # Appliquer les dégâts
                self.player["current_hp"] -= enemy_result.get("damage", 0)
                
                # Vérifier si le joueur est vaincu
                if self.player["current_hp"] <= 0:
                    self.player["current_hp"] = 0
                    combat_log.append("Vous avez été vaincu!")
                    combat_active = False
            
            # Limiter la taille du journal de combat
            if len(combat_log) > 10:
                combat_log = combat_log[-10:]
        
        # Combat terminé
        self.ui.display_combat_interface(
            self.player, 
            enemy_stats, 
            combat_log, 
            []
        )
        
        # Attendre que le joueur confirme
        self.ui.get_user_input("Appuyez sur Entrée pour continuer...")
        
        # Gérer les récompenses si le joueur a gagné
        if enemy_stats["current_hp"] <= 0:
            self._handle_combat_rewards(enemy_data)
        elif self.player["current_hp"] <= 0:
            self._handle_player_defeat()
    
    def _get_combat_actions(self) -> List[Dict[str, Any]]:
        """
        Récupère les actions disponibles en combat
        
        Returns:
            Liste des actions disponibles
        """
        actions = [
            {
                "name": "Attaque",
                "type": "attack",
                "description": "Attaquer avec votre arme équipée"
            }
        ]
        
        # Ajouter les compétences de combat disponibles
        for skill_id, skill_data in self.player.get("learned_skills", {}).items():
            skill_info = self.skills_data.get("skills", {}).get(skill_id, {})
            
            if skill_info.get("combat_usable", False):
                skill_name = skill_info.get("name", skill_id)
                skill_desc = skill_info.get("description", "")
                mp_cost = skill_info.get("mp_cost", 0)
                
                # Vérifier si le joueur a assez de MP
                if self.player["current_mp"] >= mp_cost:
                    actions.append({
                        "name": f"{skill_name} (MP: {mp_cost})",
                        "type": "skill",
                        "skill_id": skill_id,
                        "description": skill_desc
                    })
        
        # Ajouter l'option de défense
        actions.append({
            "name": "Défendre",
            "type": "defend",
            "description": "Réduire les dégâts reçus au prochain tour"
        })
        
        # Ajouter l'option d'utiliser un objet
        potions = [item for item in self.player.get("inventory", []) if item.get("type") == "potion"]
        if potions:
            actions.append({
                "name": "Utiliser un objet",
                "type": "item",
                "description": "Utiliser une potion ou un objet consommable"
            })
        
        # Ajouter l'option de fuite
        actions.append({
            "name": "Fuir",
            "type": "flee",
            "description": "Tenter de fuir le combat (pas toujours possible)"
        })
        
        return actions
    
    def _process_combat_action(self, action: Dict[str, Any], enemy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite une action de combat du joueur
        
        Args:
            action: Action choisie
            enemy: Données de l'ennemi
            
        Returns:
            Résultat de l'action
        """
        action_type = action.get("type", "attack")
        
        # Attaque de base
        if action_type == "attack":
            # Calculer les dégâts
            weapon_id = self.player.get("equipment", {}).get("weapon")
            damage_info = self.character_progression.calculate_attack_damage(weapon_id)
            
            base_damage = damage_info["damage"]
            enemy_def = enemy.get("defense", 0)
            
            # Appliquer la défense de l'ennemi
            final_damage = max(1, base_damage - enemy_def)
            
            # Chance de critique
            crit_chance = damage_info.get("critical_chance", 5)
            is_crit = random.randint(1, 100) <= crit_chance
            
            if is_crit:
                final_damage = int(final_damage * 1.5)
                return {
                    "damage": final_damage,
                    "message": f"Coup critique! Vous infligez {final_damage} points de dégâts à {enemy['name']}!"
                }
            else:
                return {
                    "damage": final_damage,
                    "message": f"Vous attaquez {enemy['name']} et infligez {final_damage} points de dégâts."
                }
        
        # Compétence
        elif action_type == "skill":
            skill_id = action.get("skill_id")
            
            if skill_id:
                # Récupérer les infos de la compétence
                skill_info = self.skills_data.get("skills", {}).get(skill_id, {})
                skill_name = skill_info.get("name", skill_id)
                mp_cost = skill_info.get("mp_cost", 0)
                
                # Vérifier et déduire le coût en MP
                if self.player["current_mp"] >= mp_cost:
                    self.player["current_mp"] -= mp_cost
                    
                    # Calculer les dégâts selon le type de compétence
                    if skill_info.get("type") == "spell":
                        damage_info = self.character_progression.calculate_spell_damage(skill_id)
                        base_damage = damage_info["damage"]
                    else:
                        damage_info = self.character_progression.calculate_attack_damage()
                        base_damage = damage_info["damage"] * 1.2  # Bonus pour compétence physique
                    
                    # Appliquer les effets
                    # (À développer plus tard pour les effets spéciaux, statuts, etc.)
                    
                    # Calculer les dégâts finaux
                    enemy_def = enemy.get("defense", 0)
                    final_damage = max(1, base_damage - enemy_def // 2)  # Les compétences ignorent une partie de la défense
                    
                    # Mettre à jour les statistiques
                    self.game_stats["skill_uses"] += 1
                    if skill_info.get("type") == "spell":
                        self.game_stats["spells_cast"] += 1
                    
                    # Améliorer la compétence avec l'expérience
                    if hasattr(self, "character_progression"):
                        self.character_progression.improve_skill(skill_id, 2)  # 2 XP pour l'utilisation en combat
                    
                    return {
                        "damage": final_damage,
                        "message": f"Vous utilisez {skill_name} et infligez {final_damage} points de dégâts à {enemy['name']}!"
                    }
                else:
                    return {
                        "damage": 0,
                        "message": f"Vous n'avez pas assez de MP pour utiliser {skill_name}."
                    }
            else:
                return {
                    "damage": 0,
                    "message": "Impossible d'utiliser cette compétence."
                }
        
        # Défense
        elif action_type == "defend":
            self.player["defending"] = True
            return {
                "damage": 0,
                "message": "Vous adoptez une posture défensive, réduisant les dégâts au prochain tour."
            }
        
        # Utilisation d'objet
        elif action_type == "item":
            # Simplification: utiliser la première potion trouvée
            potions = [item for item in self.player.get("inventory", []) if item.get("type") == "potion"]
            
            if potions:
                potion = potions[0]
                potion_name = potion.get("name", "Potion")
                
                # Effet de la potion
                if potion.get("effect") == "heal":
                    heal_amount = potion.get("effect_value", 20)
                    self.player["current_hp"] = min(self.player["max_hp"], self.player["current_hp"] + heal_amount)
                    
                    # Retirer la potion de l'inventaire
                    if potion.get("count", 1) > 1:
                        potion["count"] -= 1
                    else:
                        self.player["inventory"].remove(potion)
                    
                    return {
                        "damage": 0,
                        "message": f"Vous utilisez {potion_name} et récupérez {heal_amount} points de vie."
                    }
                elif potion.get("effect") == "mana":
                    mana_amount = potion.get("effect_value", 20)
                    self.player["current_mp"] = min(self.player["max_mp"], self.player["current_mp"] + mana_amount)
                    
                    # Retirer la potion de l'inventaire
                    if potion.get("count", 1) > 1:
                        potion["count"] -= 1
                    else:
                        self.player["inventory"].remove(potion)
                    
                    return {
                        "damage": 0,
                        "message": f"Vous utilisez {potion_name} et récupérez {mana_amount} points de mana."
                    }
            
            return {
                "damage": 0,
                "message": "Vous n'avez pas d'objets utilisables."
            }
        
        # Tentative de fuite
        elif action_type == "flee":
            # Calculer les chances de fuite
            player_speed = self.player.get("attributes", {}).get("dexterity", 10)
            enemy_speed = enemy.get("speed", 10)
            
            flee_chance = 50 + (player_speed - enemy_speed) * 5
            flee_chance = max(10, min(90, flee_chance))  # Entre 10% et 90%
            
            if random.randint(1, 100) <= flee_chance:
                # Fuite réussie
                self.ui.display_notification("Vous parvenez à fuir le combat!", type="success")
                return {
                    "damage": 0,
                    "message": "Vous fuyez le combat.",
                    "flee": True
                }
            else:
                # Fuite échouée
                return {
                    "damage": 0,
                    "message": "Vous tentez de fuir, mais l'ennemi vous en empêche!"
                }
        
        # Action non reconnue
        return {
            "damage": 0,
            "message": "Action non reconnue."
        }
    
    def _get_enemy_action(self, enemy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Détermine l'action de l'ennemi
        
        Args:
            enemy: Données de l'ennemi
            
        Returns:
            Action choisie
        """
        # Liste des actions possibles
        possible_actions = ["attack"]
        
        # Ajouter les compétences s'il en a
        for skill in enemy.get("skills", []):
            possible_actions.append(f"skill:{skill}")
        
        # Choisir une action aléatoire
        action = random.choice(possible_actions)
        
        if action == "attack":
            return {"type": "attack"}
        elif action.startswith("skill:"):
            skill_id = action.split(":")[1]
            return {"type": "skill", "skill_id": skill_id}
        else:
            return {"type": "attack"}  # Par défaut
    
    def _process_enemy_action(self, action: Dict[str, Any], enemy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite une action de combat de l'ennemi
        
        Args:
            action: Action choisie
            enemy: Données de l'ennemi
            
        Returns:
            Résultat de l'action
        """
        action_type = action.get("type", "attack")
        
        # Attaque de base
        if action_type == "attack":
            # Calculer les dégâts
            base_damage = enemy.get("attack", 10)
            player_def = self.player.get("physical_defense", 5)
            
            # Si le joueur est en défense, réduire les dégâts
            if self.player.get("defending", False):
                player_def *= 2
                self.player["defending"] = False  # Réinitialiser l'état de défense
            
            # Appliquer la défense du joueur
            final_damage = max(1, base_damage - player_def)
            
            # Chance de critique
            is_crit = random.randint(1, 100) <= 5  # 5% de chance
            
            if is_crit:
                final_damage = int(final_damage * 1.5)
                return {
                    "damage": final_damage,
                    "message": f"Coup critique! {enemy['name']} vous inflige {final_damage} points de dégâts!"
                }
            else:
                return {
                    "damage": final_damage,
                    "message": f"{enemy['name']} vous attaque et vous inflige {final_damage} points de dégâts."
                }
        
        # Compétence
        elif action_type == "skill":
            skill_id = action.get("skill_id")
            
            if skill_id:
                # Dans un jeu plus complexe, récupérer les infos de la compétence
                skill_name = "attaque spéciale"  # Simplifié
                
                # Calculer les dégâts (un peu plus élevés qu'une attaque normale)
                base_damage = enemy.get("attack", 10) * 1.3
                player_def = self.player.get("physical_defense", 5)
                
                # Si le joueur est en défense, réduire les dégâts
                if self.player.get("defending", False):
                    player_def *= 2
                    self.player["defending"] = False  # Réinitialiser l'état de défense
                
                # Appliquer la défense du joueur (les compétences ignorent une partie de la défense)
                final_damage = max(1, base_damage - player_def // 2)
                
                return {
                    "damage": int(final_damage),
                    "message": f"{enemy['name']} utilise {skill_name} et vous inflige {int(final_damage)} points de dégâts!"
                }
            else:
                # Fallback sur une attaque normale
                return self._process_enemy_action({"type": "attack"}, enemy)
        
        # Action non reconnue
        return {
            "damage": 0,
            "message": f"{enemy['name']} hésite."
        }
    
    def _handle_combat_rewards(self, enemy_data: Dict[str, Any]):
        """
        Gère les récompenses de combat
        
        Args:
            enemy_data: Données de l'ennemi
        """
        # XP gagnée
        xp_reward = enemy_data.get("xp_reward", 10)
        
        # Or gagné
        gold_reward = enemy_data.get("gold_reward", 5)
        
        # Objets potentiellement gagnés
        item_drops = enemy_data.get("drops", [])
        dropped_items = []
        
        # Traiter chaque objet potentiel
        for drop in item_drops:
            drop_chance = drop.get("chance", 100)  # En pourcentage
            
            if random.randint(1, 100) <= drop_chance:
                item_id = drop.get("item_id")
                count = drop.get("count", 1)
                
                if item_id:
                    item_data = self.item_data.get("items", {}).get(item_id, {})
                    
                    if item_data:
                        # Ajouter l'objet à l'inventaire
                        self._add_item_to_inventory(item_id, count)
                        
                        dropped_items.append({
                            "name": item_data.get("name", item_id),
                            "count": count
                        })
        
        # Mettre à jour les statistiques
        self.game_stats["enemies_defeated"] += 1
        self.game_stats["money_earned"] += gold_reward
        
        # Ajouter l'or
        self.player["gold"] = self.player.get("gold", 0) + gold_reward
        
        # Afficher les récompenses
        reward_text = f"Vous avez gagné {xp_reward} points d'expérience et {gold_reward} pièces d'or."
        
        if dropped_items:
            reward_text += "\n\nObjets récupérés:"
            for item in dropped_items:
                reward_text += f"\n • {item['name']} x{item['count']}"
        
        self.ui.display_notification(reward_text, type="success")
        
        # Attribuer l'XP et vérifier les montées de niveau
        level_before = self.player["level"]
        level_result = self.character_progression.award_xp(xp_reward)
        
        if level_result.get("levels_gained", 0) > 0:
            new_level = level_result["new_level"]
            gained_stats = {
                "attribute_points": level_result["attribute_points_gained"],
                "skill_points": level_result["skill_points_gained"]
            }
            
            # Afficher la montée de niveau
            self.ui.display_level_up(level_before, new_level, gained_stats)
    
    def _handle_player_defeat(self):
        """Gère la défaite du joueur"""
        # Options après la défaite
        options = [
            ("Charger une sauvegarde", "load"),
            ("Retourner au menu principal", "menu"),
            ("Quitter le jeu", "quit")
        ]
        
        choice = self.ui.display_game_over(
            reason="Vous avez été vaincu en combat!",
            score=self.game_stats["enemies_defeated"] * 10 + self.player["level"] * 100
        )
        
        if choice == "load":
            self.load_game()
        elif choice == "menu":
            self.show_main_menu()
        else:
            self.quit_game()
    
    def _add_item_to_inventory(self, item_id: str, count: int = 1):
        """
        Ajoute un objet à l'inventaire du joueur
        
        Args:
            item_id: ID de l'objet
            count: Quantité à ajouter
        """
        # Initialiser l'inventaire si nécessaire
        if "inventory" not in self.player:
            self.player["inventory"] = []
        
        # Vérifier si l'objet existe déjà dans l'inventaire
        for item in self.player["inventory"]:
            if item.get("id") == item_id:
                item["count"] = item.get("count", 1) + count
                return
        
        # Sinon, ajouter le nouvel objet
        item_data = self.item_data.get("items", {}).get(item_id, {})
        
        if item_data:
            self.player["inventory"].append({
                "id": item_id,
                "name": item_data.get("name", item_id),
                "description": item_data.get("description", ""),
                "type": item_data.get("type", "misc"),
                "category": item_data.get("category", "Divers"),
                "rarity": item_data.get("rarity", "common"),
                "count": count
            })
    
    def handle_examine(self, intent: Dict[str, Any], command: str):
        """
        Gère l'examen d'objets ou d'éléments du jeu
        
        Args:
            intent: Intention analysée du joueur
            command: Commande originale du joueur
        """
        # Pour l'instant, simplement générer une description avec l'IA
        context = {
            "interaction_type": "description",
            "location_id": self.current_location,
            "time_of_day": self.time_of_day,
            "weather": self.weather
        }
        
        response = self.ai_manager.generate_response(command, context)
        
        # Afficher la description
        self.ui.display_description(response, title="Observation")
    
    def handle_inventory_action(self, intent: Dict[str, Any]):
        """
        Gère les actions liées à l'inventaire
        
        Args:
            intent: Intention analysée du joueur
        """
        # Pour l'instant, simplement afficher l'inventaire
        self.show_inventory()
    
    def show_inventory(self):
        """Affiche l'inventaire du joueur"""
        self.ui.display_inventory(self.player.get("inventory", []), self.player.get("gold", 0))
    
    def show_skills(self):
        """Affiche les compétences du joueur"""
        self.ui.display_skills(self.player.get("learned_skills", {}))
    
    def show_map(self):
        """Affiche la carte des lieux découverts"""
        # Simplification pour l'instant
        self.ui.display_notification("Carte non disponible dans cette version.", type="info")
    
    def show_quests(self):
        """Affiche le journal de quêtes"""
        self.ui.display_quests(self.active_quests, self.completed_quests)
    
    def save_game(self):
        """Interface de sauvegarde de la partie"""
        # Créer un nom pour la sauvegarde
        save_name = f"save_{time.strftime('%Y%m%d_%H%M%S')}"
        
        # Demander un slot
        slots = ["Emplacement 1", "Emplacement 2", "Emplacement 3", "Personnalisé"]
        slot_values = ["slot1", "slot2", "slot3", "custom"]
        
        options = [(slots[i], slot_values[i]) for i in range(len(slots))]
        
        slot = self.ui.display_menu("Choisissez un emplacement de sauvegarde", options)
        
        if slot == "custom":
            # Demander un nom personnalisé
            self.ui.print_text("Entrez un nom pour votre sauvegarde:", color="prompt")
            custom_slot = self.ui.get_user_input("Nom: ")
            slot = custom_slot.strip() if custom_slot.strip() else "custom"
        
        # Afficher un écran de chargement
        self.ui.display_loading_screen("Sauvegarde en cours...")
        
        # Effectuer la sauvegarde
        result = self.save_manager.save_game(slot, save_name)
        
        if result["success"]:
            self.ui.display_notification("Partie sauvegardée avec succès!", type="success")
        else:
            self.ui.display_notification(f"Erreur lors de la sauvegarde: {result['message']}", type="error")
    
    def load_game_menu(self):
        """Menu de chargement de partie"""
        save_slots = self.save_manager.list_saves()
        
        if not save_slots:
            self.ui.display_notification("Aucune sauvegarde disponible.", type="info")
            return
        
        # Afficher le menu de chargement
        load_result = self.ui.display_save_load_menu(save_slots)
        
        if load_result["action"] == "load" and "slot" in load_result:
            slot_index = load_result["slot"]
            if 0 <= slot_index < len(save_slots):
                save_path = save_slots[slot_index]["file_path"]
                
                # Afficher un écran de chargement
                self.ui.display_loading_screen("Chargement de la sauvegarde...")
                
                # Charger la sauvegarde
                load_result = self.save_manager.load_game(save_path)
                
                if load_result["success"]:
                    self.ui.display_notification("Partie chargée avec succès!", type="success", dismiss_after=1)
                    # Continuer le jeu
                else:
                    self.ui.display_notification(f"Erreur lors du chargement: {load_result['message']}", type="error")
    
    def show_help(self):
        """Affiche l'aide du jeu"""
        commands = {
            "se déplacer/aller à [lieu]": "Se déplacer vers un lieu",
            "parler à/discuter avec [personnage]": "Engager une conversation",
            "examiner/regarder [objet/lieu]": "Observer quelque chose en détail",
            "attaquer/combattre [ennemi]": "Initier un combat",
            "prendre/ramasser [objet]": "Prendre un objet",
            "utiliser/équiper [objet]": "Utiliser ou équiper un objet",
            "acheter/vendre [objet]": "Commercer avec un marchand",
            "i, inv, inventaire": "Afficher votre inventaire",
            "s, skills, compétences": "Afficher vos compétences",
            "m, map, carte": "Afficher la carte",
            "j, journal, quêtes": "Afficher votre journal de quêtes",
            "save, sauvegarder": "Sauvegarder la partie",
            "load, charger": "Charger une partie sauvegardée",
            "h, help, aide": "Afficher cette aide",
            "q, quit, exit": "Quitter le jeu"
        }
        
        self.ui.display_help(commands)
    
    def handle_market(self, intent: Dict[str, Any]):
        """
        Gère les interactions de marché
        
        Args:
            intent: Intention analysée du joueur
        """
        # Vérifier si un marchand est présent
        location_data = self.location_data.get(self.current_location, {})
        npcs = location_data.get("npcs", [])
        
        merchant_id = None
        merchant_data = None
        
        for npc_id in npcs:
            npc_data = self.npc_data.get(npc_id, {})
            if npc_data.get("is_merchant", False):
                merchant_id = npc_id
                merchant_data = npc_data
                break
        
        if not merchant_id:
            self.ui.display_notification("Il n'y a pas de marchand dans cette zone.", type="info")
            return
        
        # Afficher l'écran de commerce
        self._show_merchant_interface(merchant_id, merchant_data)
    
    def _show_merchant_interface(self, merchant_id: str, merchant_data: Dict[str, Any]):
        """
        Affiche l'interface de commerce avec un marchand
        
        Args:
            merchant_id: ID du marchand
            merchant_data: Données du marchand
        """
        merchant_name = merchant_data.get("name", "Marchand")
        
                # Récupérer les objets en vente
        for_sale = merchant_data.get("sells", [])
        inventory = self.player.get("inventory", [])
        player_gold = self.player.get("gold", 0)
        
        # Utiliser un drapeau pour contrôler la boucle au lieu de break
        showing_merchant = True
        
        while showing_merchant:
            options = [
                ("Acheter des objets", "buy"),
                ("Vendre des objets", "sell"),
                ("Quitter", "exit")
            ]
            
            choice = self.ui.display_menu(f"Commerce avec {merchant_name}", options)
            
            if choice == "buy":
                self._handle_buying(merchant_id, merchant_data)
            elif choice == "sell":
                self._handle_selling(merchant_id, merchant_data)
            elif choice == "exit":
                showing_merchant = False  # Au lieu de break
    
    def _handle_buying(self, merchant_id: str, merchant_data: Dict[str, Any]):
        """
        Gère l'achat d'objets auprès d'un marchand
        
        Args:
            merchant_id: ID du marchand
            merchant_data: Données du marchand
        """
        merchant_name = merchant_data.get("name", "Marchand")
        for_sale = merchant_data.get("sells", [])
        player_gold = self.player.get("gold", 0)
        
        if not for_sale:
            self.ui.display_notification(f"{merchant_name} n'a rien à vendre pour le moment.", type="info")
            return
            
        # Préparer la liste des objets à vendre
        items_for_sale = []
        for item_id in for_sale:
            item_data = self.item_data.get("items", {}).get(item_id, {})
            if item_data:
                base_price = item_data.get("price", 10)
                
                # Ajuster le prix selon le charisme du joueur et la réputation
                charisma_mod = self.player.get("attributes", {}).get("charisma", 10) - 10
                reputation_mod = self.relationships.get(merchant_id, 0)
                
                price_modifier = 1.0 - (charisma_mod * 0.01) - (reputation_mod * 0.005)
                price_modifier = max(0.7, min(1.3, price_modifier))  # Limite entre 70% et 130%
                
                final_price = max(1, int(base_price * price_modifier))
                
                items_for_sale.append({
                    "id": item_id,
                    "name": item_data.get("name", item_id),
                    "price": final_price,
                    "description": item_data.get("description", "")
                })
        
        # Afficher les objets à vendre
        self.ui.print_header(f"Objets en vente chez {merchant_name}", f"Votre or: {player_gold}")
        
        for i, item in enumerate(items_for_sale, 1):
            affordable = player_gold >= item["price"]
            color = "normal" if affordable else "error"
            
            self.ui.print_text(f"{i}. {item['name']} - {item['price']} or", color=color)
            self.ui.print_text(f"   {item['description']}", color="info")
        
        # Option pour quitter
        self.ui.print_text(f"{len(items_for_sale) + 1}. Retour", color="warning")
        
        # Demander à l'utilisateur ce qu'il veut acheter
        choice = self.ui.get_user_input("Que voulez-vous acheter? ")
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(items_for_sale):
                item = items_for_sale[choice_num - 1]
                
                # Vérifier si le joueur a assez d'or
                if player_gold >= item["price"]:
                    # Effectuer l'achat
                    self.player["gold"] -= item["price"]
                    self._add_item_to_inventory(item["id"])
                    
                    # Mettre à jour les statistiques
                    self.game_stats["money_spent"] += item["price"]
                    
                    # Afficher confirmation
                    self.ui.display_notification(f"Vous avez acheté {item['name']} pour {item['price']} or.", type="success")
                else:
                    self.ui.display_notification("Vous n'avez pas assez d'or pour acheter cet objet.", type="warning")
            elif choice_num == len(items_for_sale) + 1:
                return  # Retour au menu précédent
            else:
                self.ui.display_notification("Choix invalide.", type="error")
        except ValueError:
            self.ui.display_notification("Veuillez entrer un numéro valide.", type="error")
    
    def _handle_selling(self, merchant_id: str, merchant_data: Dict[str, Any]):
        """
        Gère la vente d'objets à un marchand
        
        Args:
            merchant_id: ID du marchand
            merchant_data: Données du marchand
        """
        inventory = self.player.get("inventory", [])
        player_gold = self.player.get("gold", 0)
        
        if not inventory:
            self.ui.display_notification("Vous n'avez rien à vendre.", type="info")
            return
            
        # Préparer la liste des objets à vendre
        items_to_sell = []
        for item in inventory:
            item_id = item.get("id")
            item_data = self.item_data.get("items", {}).get(item_id, {})
            
            if item_data:
                base_price = item_data.get("price", 10)
                
                # Le prix de vente est généralement inférieur au prix d'achat
                sell_price = max(1, int(base_price * 0.5))
                
                # Ajuster selon le charisme et la réputation
                charisma_mod = self.player.get("attributes", {}).get("charisma", 10) - 10
                reputation_mod = self.relationships.get(merchant_id, 0)
                
                price_modifier = 1.0 + (charisma_mod * 0.01) + (reputation_mod * 0.005)
                price_modifier = max(0.4, min(0.8, price_modifier))  # Limite entre 40% et 80% du prix de base
                
                final_price = max(1, int(base_price * price_modifier))
                
                items_to_sell.append({
                    "item": item,
                    "name": item.get("name", item_id),
                    "price": final_price,
                    "count": item.get("count", 1),
                    "description": item.get("description", "")
                })
        
        # Afficher les objets à vendre
        self.ui.print_header("Vos objets à vendre", f"Votre or: {player_gold}")
        
        for i, item in enumerate(items_to_sell, 1):
            self.ui.print_text(f"{i}. {item['name']} x{item['count']} - {item['price']} or chacun", color="normal")
            self.ui.print_text(f"   {item['description']}", color="info")
        
        # Option pour quitter
        self.ui.print_text(f"{len(items_to_sell) + 1}. Retour", color="warning")
        
        # Demander à l'utilisateur ce qu'il veut vendre
        choice = self.ui.get_user_input("Que voulez-vous vendre? ")
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(items_to_sell):
                item_info = items_to_sell[choice_num - 1]
                item = item_info["item"]
                
                # Demander la quantité si l'objet est empilable
                quantity = 1
                if item_info["count"] > 1:
                    quantity_input = self.ui.get_user_input(f"Combien d'exemplaires (1-{item_info['count']})? ")
                    try:
                        quantity = int(quantity_input)
                        quantity = max(1, min(quantity, item_info["count"]))
                    except ValueError:
                        quantity = 1
                
                # Calculer le prix total
                total_price = item_info["price"] * quantity
                
                # Effectuer la vente
                self.player["gold"] += total_price
                
                # Mettre à jour l'inventaire
                if quantity >= item_info["count"]:
                    # Retirer l'objet complètement
                    self.player["inventory"].remove(item)
                else:
                    # Réduire la quantité
                    item["count"] -= quantity
                
                # Mettre à jour les statistiques
                self.game_stats["money_earned"] += total_price
                
                # Afficher confirmation
                self.ui.display_notification(f"Vous avez vendu {item_info['name']} x{quantity} pour {total_price} or.", type="success")
            elif choice_num == len(items_to_sell) + 1:
                return  # Retour au menu précédent
            else:
                self.ui.display_notification("Choix invalide.", type="error")
        except ValueError:
            self.ui.display_notification("Veuillez entrer un numéro valide.", type="error")
    
    def handle_intimate(self, intent: Dict[str, Any], command: str):
        """
        Gère les interactions intimes
        
        Args:
            intent: Intention analysée du joueur
            command: Commande originale du joueur
        """
        # Vérifier si le contenu mature est activé
        mature_enabled = False
        if hasattr(self, "mature_content_manager"):
            mature_enabled = self.mature_content_manager.is_enabled
        elif hasattr(self, "mature_content_enabled"):
            mature_enabled = self.mature_content_enabled
            
        if not mature_enabled:
            self.ui.display_notification("Le contenu mature est désactivé dans les options.", type="info")
            return
            
        # Extraire la cible de l'interaction
        target = intent.get("params", {}).get("target", "").lower()
        
        if not target:
            self.ui.display_notification("Avec qui souhaitez-vous interagir?", type="info")
            return
        
        # Chercher le PNJ dans le lieu actuel
        current_location = self.location_data.get(self.current_location, {})
        npcs = current_location.get("npcs", [])
        
        npc_id = None
        npc_data = None
        
        for npc in npcs:
            npc_info = self.npc_data.get(npc, {})
            npc_name = npc_info.get("name", "").lower()
            
            if target in npc_name or target == npc.lower():
                npc_id = npc
                npc_data = npc_info
                break
        
        if not npc_id:
            self.ui.display_notification(f"Il n'y a personne qui s'appelle '{target}' ici.", type="warning")
            return
            
        # Vérifier si le PNJ peut avoir des interactions intimes
        if not npc_data.get("romance_enabled", False):
            self.ui.display_notification(f"{npc_data.get('name', 'Ce personnage')} ne semble pas intéressé.", type="info")
            return
            
        # Vérifier la relation avec le PNJ
        relationship_level = self.relationships.get(npc_id, 0)
        
        if relationship_level < 50:  # Seuil arbitraire
            self.ui.display_notification(f"Votre relation avec {npc_data.get('name', 'ce personnage')} n'est pas assez développée.", type="warning")
            return
            
        # Générer le contenu avec l'IA
        # Déterminer le niveau d'intensité selon la relation
        if relationship_level >= 90:
            intensity = "explicit"
        elif relationship_level >= 70:
            intensity = "moderate"
        else:
            intensity = "mild"
            
        response = self.ai_manager.generate_intimate_scene(
            npc_id, 
            intensity, 
            self.current_location, 
            {
                "mature_content_enabled": mature_enabled,
                "player_name": self.player.get("name", "Joueur"),
                "relationship_level": relationship_level,
                "time_of_day": self.time_of_day,
                "weather": self.weather
            }
        )
        
        # Afficher la scène
        if isinstance(response, dict) and "text" in response:
            scene_text = response["text"]
        else:
            scene_text = response
            
        self.ui.display_description(scene_text, title=f"Moment intime avec {npc_data.get('name', 'NPC')}")
        
        # Améliorer la relation
        self.relationships[npc_id] = min(100, relationship_level + 5)
        
        # Attendre la confirmation du joueur
        self.ui.get_user_input("Appuyez sur Entrée pour continuer...")


# Point d'entrée du programme
if __name__ == "__main__":
    try:
        # Vérifier que tous les fichiers nécessaires existent
        # Utiliser des chemins relatifs depuis le point où le script est exécuté
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        required_files = [
            os.path.join(data_dir, "locations.json"),
            os.path.join(data_dir, "npcs.json"),
            os.path.join(data_dir, "items.json"),
            os.path.join(data_dir, "skills.json"),
            os.path.join(data_dir, "quests.json"),
            os.path.join(data_dir, "combat.json"),
            os.path.join(data_dir, "progression.json")
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
                
        if missing_files:
            print("Erreur: Fichiers manquants:")
            for file in missing_files:
                print(f"- {file}")
            print("\nVeuillez vous assurer que tous les fichiers de données sont présents.")
            sys.exit(1)
        
        # Lancer le jeu
        game = MuskoTenseiRP()
        game.start()
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)