# interface_cli.py
import os
import sys
import time
import random
import platform
import shutil
import re
from typing import Dict, List, Any, Tuple, Optional, Callable
import colorama
from colorama import Fore, Back, Style

# Initialiser colorama pour le support des couleurs sur Windows
colorama.init()

class InterfaceCLI:
    def __init__(self, game_instance=None):
        """
        Initialise l'interface CLI du jeu MUSKO TENSEI RP
        
        Args:
            game_instance: Instance du jeu principal (MuskoTenseiRP)
        """
        self.game = game_instance
        self.terminal_width, self.terminal_height = self._get_terminal_size()
        
        # Définir les couleurs et styles de base
        self.COLORS = {
            'title': Fore.CYAN + Style.BRIGHT,
            'subtitle': Fore.BLUE + Style.BRIGHT,
            'normal': Fore.WHITE,
            'prompt': Fore.GREEN + Style.BRIGHT,
            'input': Fore.YELLOW,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'critical': Fore.RED + Style.BRIGHT,
            'highlight': Fore.MAGENTA + Style.BRIGHT,
            'info': Fore.CYAN,
            'mana': Fore.BLUE + Style.BRIGHT,
            'health': Fore.RED,
            'gold': Fore.YELLOW + Style.BRIGHT,
            'exp': Fore.GREEN + Style.BRIGHT,
            'item': Fore.WHITE + Style.BRIGHT,
            'rare_item': Fore.BLUE + Style.BRIGHT,
            'epic_item': Fore.MAGENTA + Style.BRIGHT,
            'legendary_item': Fore.YELLOW + Style.BRIGHT,
            'npc_friendly': Fore.GREEN,
            'npc_neutral': Fore.WHITE,
            'npc_hostile': Fore.RED,
            'spell_fire': Fore.RED + Style.BRIGHT,
            'spell_water': Fore.BLUE + Style.BRIGHT,
            'spell_earth': Fore.GREEN,
            'spell_wind': Fore.CYAN,
            'spell_light': Fore.WHITE + Style.BRIGHT,
            'spell_dark': Fore.MAGENTA,
            'reset': Style.RESET_ALL
        }
        
        # Définir les émojis et symboles pour différents éléments
        # Les émojis fonctionnent sur la plupart des terminaux modernes
        self.SYMBOLS = {
            'health': '❤️',
            'mana': '🔮',
            'gold': '💰',
            'exp': '✨',
            'level': '⚜️',
            'sword': '⚔️',
            'shield': '🛡️',
            'magic': '✨',
            'potion': '🧪',
            'book': '📚',
            'quest': '📜',
            'npc': '👤',
            'player': '🧙‍♂️',
            'enemy': '👺',
            'boss': '👹',
            'location': '🏠',
            'dungeon': '🏰',
            'item': '📦',
            'skill': '💪',
            'time_day': '☀️',
            'time_night': '🌙',
            'save': '💾',
            'load': '📂',
            'success': '✅',
            'failure': '❌',
            'warning': '⚠️',
            'arrow': '→',
            'star': '★',
            'empty_star': '☆',
            'dot': '•',
            'separator': '═══',
            'box_horizontal': '━',
            'box_vertical': '┃',
            'box_corner_tl': '┏',
            'box_corner_tr': '┓',
            'box_corner_bl': '┗',
            'box_corner_br': '┛',
            'box_t_down': '┳',
            'box_t_up': '┻',
            'box_t_right': '┣',
            'box_t_left': '┫',
            'box_cross': '╋'
        }
        
        # Option pour désactiver les émojis si le terminal ne les supporte pas
        self.use_emojis = True
        
        # Historique des commandes pour rappel avec flèches (à implémenter)
        self.command_history = []
        self.history_position = 0
        
        # Définir l'écran d'accueil du jeu
        self.splash_screens = [self._create_splash_screen()]
        
        # Options d'affichage
        self.text_speed = 0.02  # Vitesse de défilement du texte (0 pour instantané)
        self.auto_clear = True  # Effacer l'écran automatiquement entre les commandes
        self.show_hints = True  # Afficher des astuces pendant le chargement
        
        # L'animation actuelle en cours, le cas échéant
        self.current_animation = None
    
    def _get_terminal_size(self) -> Tuple[int, int]:
        """
        Récupère la taille du terminal
        
        Returns:
            Tuple (largeur, hauteur)
        """
        try:
            columns, lines = shutil.get_terminal_size()
            return columns, lines
        except:
            # Valeurs par défaut si impossible de déterminer
            return 80, 24
    
    def _create_splash_screen(self) -> str:
        """
        Crée un écran d'accueil ASCII art
        
        Returns:
            Texte formaté pour l'écran d'accueil
        """
        return f'''{Fore.CYAN + Style.BRIGHT}
    ╔╦╗╦ ╦╔═╗╦╔═╔═╗  ╔╦╗╔═╗╔╗╔╔═╗╔═╗╦
    ║║║║ ║╚═╗╠╩╗║ ║   ║ ║╣ ║║║╚═╗║╣ ║
    ╩ ╩╚═╝╚═╝╩ ╩╚═╝   ╩ ╚═╝╝╚╝╚═╝╚═╝╩═╝
        ╦═╗╔═╗  {Fore.YELLOW + Style.BRIGHT}⚜️  {Fore.CYAN + Style.BRIGHT}╦═╗╔═╗
        ╠╦╝╠═╝  {Fore.YELLOW + Style.BRIGHT}✨  {Fore.CYAN + Style.BRIGHT}╠╦╝╠═╝
        ╩╚═╩    {Fore.YELLOW + Style.BRIGHT}🔮  {Fore.CYAN + Style.BRIGHT}╩╚═╩  
{Style.RESET_ALL}

{Fore.YELLOW}* Une nouvelle vie dans un monde de magie et d'aventure *{Style.RESET_ALL}
{Fore.WHITE}Inspiré par {Fore.GREEN}Mushoku Tensei - Jobless Reincarnation{Style.RESET_ALL}

{Fore.CYAN}[ Appuyez sur ENTRÉE pour commencer votre aventure ]{Style.RESET_ALL}
'''
    
    def clear_screen(self):
        """Efface l'écran du terminal"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    def update_terminal_size(self):
        """Met à jour la taille du terminal"""
        self.terminal_width, self.terminal_height = self._get_terminal_size()
    
    def draw_box(self, content: str, width: int = None, title: str = None, style: str = 'single', color: str = None) -> str:
        """
        Dessine une boîte autour du contenu
        
        Args:
            content: Texte à encadrer
            width: Largeur de la boîte (par défaut: taille du terminal)
            title: Titre optionnel de la boîte
            style: Style de la boîte ('single', 'double', 'thick')
            color: Couleur de la boîte
            
        Returns:
            Texte formaté avec la boîte
        """
        self.update_terminal_size()
        
        # Si aucune largeur n'est spécifiée, utiliser la largeur du terminal - 4
        if width is None:
            width = self.terminal_width - 4
            
        # Choisir le style de la boîte
        box_chars = {
            'single': {
                'horizontal': '─', 'vertical': '│', 
                'top_left': '┌', 'top_right': '┐',
                'bottom_left': '└', 'bottom_right': '┘',
                'title_left': '┤', 'title_right': '├'
            },
            'double': {
                'horizontal': '═', 'vertical': '║', 
                'top_left': '╔', 'top_right': '╗',
                'bottom_left': '╚', 'bottom_right': '╝',
                'title_left': '╡', 'title_right': '╞'
            },
            'thick': {
                'horizontal': '━', 'vertical': '┃', 
                'top_left': '┏', 'top_right': '┓',
                'bottom_left': '┗', 'bottom_right': '┛',
                'title_left': '┫', 'title_right': '┣'
            }
        }
        
        box = box_chars.get(style, box_chars['single'])
        
        # Appliquer la couleur
        box_color = self.COLORS.get(color, '') if color in self.COLORS else ''
        reset = Style.RESET_ALL if box_color else ''
        
        # Fractionner le contenu en lignes et s'assurer qu'aucune ligne ne dépasse la largeur
        lines = content.split('\n')
        wrapped_lines = []
        for line in lines:
            # Si la ligne est trop longue, la fractionner
            while len(line) > width - 4:
                wrapped_lines.append(line[:width-4])
                line = line[width-4:]
            wrapped_lines.append(line)
            
        # Créer la boîte
        box_str = []
        
        # Ligne du haut avec titre éventuel
        if title:
            title_len = len(title) + 2  # +2 pour l'espace de chaque côté
            left_width = (width - title_len) // 2
            right_width = width - title_len - left_width
            
            box_str.append(f"{box_color}{box['top_left']}{box['horizontal'] * left_width} {title} {box['horizontal'] * right_width}{box['top_right']}{reset}")
        else:
            box_str.append(f"{box_color}{box['top_left']}{box['horizontal'] * width}{box['top_right']}{reset}")
            
        # Contenu
        for line in wrapped_lines:
            padding = width - len(line)
            box_str.append(f"{box_color}{box['vertical']}{reset} {line}{' ' * (padding-1)}{box_color}{box['vertical']}{reset}")
            
        # Ligne du bas
        box_str.append(f"{box_color}{box['bottom_left']}{box['horizontal'] * width}{box['bottom_right']}{reset}")
        
        return "\n".join(box_str)
    
    def print_text(self, text: str, color: str = None, slow: bool = False, center: bool = False, bold: bool = False):
        """
        Affiche du texte avec des options de formatage
        
        Args:
            text: Texte à afficher
            color: Couleur du texte
            slow: Si True, affiche le texte caractère par caractère
            center: Si True, centre le texte dans le terminal
            bold: Si True, met le texte en gras
        """
        # Appliquer la couleur et le style
        text_color = self.COLORS.get(color, '') if color in self.COLORS else ''
        text_bold = Style.BRIGHT if bold else ''
        reset = Style.RESET_ALL if text_color or text_bold else ''
        
        # Centrer si nécessaire
        if center:
            lines = text.split('\n')
            formatted_lines = []
            for line in lines:
                space = max(0, (self.terminal_width - len(line)) // 2)
                formatted_lines.append(' ' * space + line)
            text = '\n'.join(formatted_lines)
        
        # Préparer le texte formaté
        formatted_text = f"{text_color}{text_bold}{text}{reset}"
        
        # Afficher le texte lentement ou normalement
        if slow and self.text_speed > 0:
            for char in formatted_text:
                print(char, end='', flush=True)
                time.sleep(self.text_speed)
            print()
        else:
            print(formatted_text)
    
    def print_header(self, title: str, subtitle: str = None):
        """
        Affiche un en-tête formaté avec titre et sous-titre optionnel
        
        Args:
            title: Titre principal
            subtitle: Sous-titre optionnel
        """
        self.update_terminal_size()
        
        # Créer une ligne décorative
        line = "═" * (self.terminal_width - 4)
        
        # Afficher le titre centré
        print("")
        self.print_text(title, color='title', center=True, bold=True)
        
        # Afficher le sous-titre si fourni
        if subtitle:
            self.print_text(subtitle, color='subtitle', center=True)
            
        # Afficher la ligne décorative
        self.print_text(line, color='normal', center=True)
        print("")
    
    def print_divider(self, style: str = 'normal'):
        """
        Affiche une ligne séparatrice
        
        Args:
            style: Style de la ligne ('normal', 'heavy', 'light', 'dotted')
        """
        self.update_terminal_size()
        
        divider_chars = {
            'normal': '─',
            'heavy': '━',
            'light': '╌',
            'dotted': '┄'
        }
        
        char = divider_chars.get(style, '─')
        divider = char * (self.terminal_width - 4)
        
        print("")
        self.print_text(divider, color='normal', center=True)
        print("")
    
    def get_formatted_status_bar(self, current: int, maximum: int, width: int = 20, 
                               filled_char: str = '█', empty_char: str = '░', 
                               color: str = None) -> str:
        """
        Crée une barre de statut formatée
        
        Args:
            current: Valeur actuelle
            maximum: Valeur maximale
            width: Largeur de la barre
            filled_char: Caractère pour la partie remplie
            empty_char: Caractère pour la partie vide
            color: Couleur de la barre
            
        Returns:
            Texte formaté pour la barre de statut
        """
        # Éviter la division par zéro
        if maximum <= 0:
            maximum = 1
            
        # Calculer le ratio et le nombre de caractères remplis
        ratio = min(1.0, current / maximum)
        filled_count = int(width * ratio)
        
        # Créer la barre
        bar_color = self.COLORS.get(color, '') if color in self.COLORS else ''
        reset = Style.RESET_ALL if bar_color else ''
        
        bar = f"{bar_color}{filled_char * filled_count}{empty_char * (width - filled_count)}{reset}"
        
        return f"{bar} {current}/{maximum}"
    
    def print_player_stats(self):
        """Affiche les statistiques du joueur dans une barre d'état en haut de l'écran"""
        if not self.game or not hasattr(self.game, "player"):
            return
            
        player = self.game.player
        
        # Récupérer les stats
        hp = player.get("current_hp", 0)
        max_hp = player.get("max_hp", 100)
        mp = player.get("current_mp", 0)
        max_mp = player.get("max_mp", 50)
        level = player.get("level", 1)
        xp = player.get("xp", 0)
        
        # Calculer l'XP nécessaire pour le niveau suivant
        next_level_xp = 0
        if hasattr(self.game, "character_progression"):
            _, next_level_xp = self.game.character_progression.get_next_level_xp(level)
        
        # Symboles pour les barres de statut
        hp_symbol = f"{self.SYMBOLS['health']} " if self.use_emojis else "HP: "
        mp_symbol = f"{self.SYMBOLS['mana']} " if self.use_emojis else "MP: "
        xp_symbol = f"{self.SYMBOLS['exp']} " if self.use_emojis else "XP: "
        lvl_symbol = f"{self.SYMBOLS['level']} " if self.use_emojis else "LVL: "
        
        # Créer les barres de statut
        hp_bar = self.get_formatted_status_bar(hp, max_hp, width=15, color='health')
        mp_bar = self.get_formatted_status_bar(mp, max_mp, width=15, color='mana')
        xp_bar = self.get_formatted_status_bar(xp, next_level_xp, width=15, color='exp')
        
        # Afficher les statistiques
        print(f"{hp_symbol}{hp_bar}  {mp_symbol}{mp_bar}  {lvl_symbol}{level}  {xp_symbol}{xp_bar}")
        
        # Ligne séparatrice
        self.print_divider('light')
    
    def print_location_info(self):
        """Affiche les informations sur la localisation actuelle"""
        if not self.game or not hasattr(self.game, "current_location"):
            return
            
        location_id = self.game.current_location
        
        # Obtenir les données de l'emplacement
        location_data = {}
        if hasattr(self.game, "location_data"):
            location_data = self.game.location_data.get(location_id, {})
            
        # Récupérer les infos
        location_name = location_data.get("name", "Unknown Location")
        location_type = location_data.get("type", "area")
        time_of_day = getattr(self.game, "time_of_day", "day")
        weather = getattr(self.game, "weather", "clear")
        
        # Symboles
        location_symbol = self.SYMBOLS.get(f"location", "🏠") if self.use_emojis else ""
        time_symbol = self.SYMBOLS.get(f"time_{time_of_day}", "🕓") if self.use_emojis else ""
        
        # Afficher les infos
        location_text = f"{location_symbol} {location_name} ({location_type.capitalize()})"
        time_text = f"{time_symbol} {time_of_day.capitalize()}, {weather.capitalize()}"
        
        # Centrer dans le terminal
        padding = max(0, self.terminal_width - len(location_text) - len(time_text) - 2)
        
        print(f"{self.COLORS['highlight']}{location_text}{' ' * padding}{time_text}{Style.RESET_ALL}")
        
        # Ligne séparatrice
        self.print_divider('light')
    
    def animate_text(self, text: str, animation_type: str = 'typing', color: str = None, delay: float = 0.03):
        """
        Anime l'affichage du texte avec différents effets
        
        Args:
            text: Texte à animer
            animation_type: Type d'animation ('typing', 'fade_in', 'blink', 'scroll')
            color: Couleur du texte
            delay: Délai entre chaque étape de l'animation
        """
        self.current_animation = animation_type
        text_color = self.COLORS.get(color, '') if color in self.COLORS else ''
        reset = Style.RESET_ALL if text_color else ''
        
        if animation_type == 'typing':
            for char in text:
                print(f"{text_color}{char}{reset}", end='', flush=True)
                time.sleep(delay)
            print()
            
        elif animation_type == 'fade_in':
            # Simuler un fondu en utilisant des caractères de plus en plus visibles
            chars = ' .:-=+*#%@'
            for i in range(len(chars)):
                print(f"{text_color}{text.replace(' ', chars[i])}{reset}", end='\r', flush=True)
                time.sleep(delay)
            print(f"{text_color}{text}{reset}")
            
        elif animation_type == 'blink':
            # Faire clignoter le texte
            for _ in range(3):
                print(f"{text_color}{text}{reset}", end='\r', flush=True)
                time.sleep(delay * 2)
                print(' ' * len(text), end='\r', flush=True)
                time.sleep(delay)
            print(f"{text_color}{text}{reset}")
            
        elif animation_type == 'scroll':
            # Faire défiler le texte de droite à gauche
            width = self.terminal_width
            padded_text = ' ' * width + text + ' ' * width
            for i in range(len(padded_text) - width):
                print(f"{text_color}{padded_text[i:i+width]}{reset}", end='\r', flush=True)
                time.sleep(delay)
            print()
            
        self.current_animation = None
    
    def display_splash_screen(self):
        """Affiche l'écran d'accueil du jeu"""
        self.clear_screen()
        print(random.choice(self.splash_screens))
        input()  # Attendre que l'utilisateur appuie sur Entrée
    
    def display_menu(self, title: str, options: List[Tuple[str, Any]], prompt: str = "Votre choix: "):
        """
        Affiche un menu et retourne le choix de l'utilisateur
        
        Args:
            title: Titre du menu
            options: Liste de tuples (texte_option, valeur_retour)
            prompt: Texte d'invite
            
        Returns:
            Valeur associée à l'option choisie
        """
        self.print_header(title)
        
        # Afficher les options
        for i, (option_text, _) in enumerate(options, 1):
            print(f"{self.COLORS['normal']}{i}. {option_text}{Style.RESET_ALL}")
        
        # Demander le choix de l'utilisateur
        while True:
            print()
            choice = input(f"{self.COLORS['prompt']}{prompt}{self.COLORS['input']}")
            print(Style.RESET_ALL, end="")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1][1]
                else:
                    print(f"{self.COLORS['error']}Choix invalide. Veuillez entrer un nombre entre 1 et {len(options)}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{self.COLORS['error']}Veuillez entrer un nombre.{Style.RESET_ALL}")
    
    def get_user_input(self, prompt: str = "> ", color: str = 'prompt', input_color: str = 'input'):
        """
        Récupère l'entrée de l'utilisateur avec formatage
        
        Args:
            prompt: Texte d'invite
            color: Couleur du prompt
            input_color: Couleur du texte saisi
            
        Returns:
            Texte saisi par l'utilisateur
        """
        prompt_color = self.COLORS.get(color, '') if color in self.COLORS else ''
        in_color = self.COLORS.get(input_color, '') if input_color in self.COLORS else ''
        reset = Style.RESET_ALL
        
        user_input = input(f"{prompt_color}{prompt}{in_color}")
        print(f"{reset}", end="")
        
        # Ajouter à l'historique des commandes si non vide
        if user_input.strip():
            self.command_history.append(user_input)
            self.history_position = len(self.command_history)
            
        return user_input
    
    def display_dialogue(self, character_name: str, text: str, character_mood: str = 'neutral', 
                        avatar: str = None, color: str = None, animate: bool = True):
        """
        Affiche un dialogue avec un personnage
        
        Args:
            character_name: Nom du personnage
            text: Texte du dialogue
            character_mood: Humeur du personnage (affecte l'affichage)
            avatar: Avatar ASCII art du personnage (si disponible)
            color: Couleur du texte (par défaut selon le type de PNJ)
            animate: Si True, anime l'affichage du texte
        """
        # Déterminer la couleur en fonction du type de PNJ
        if not color:
            if character_mood == 'friendly':
                color = 'npc_friendly'
            elif character_mood == 'hostile':
                color = 'npc_hostile'
            else:
                color = 'npc_neutral'
        
        # Créer une boîte de dialogue
        dialogue_header = f"{self.COLORS.get(color, '')}{character_name}{Style.RESET_ALL}"
        
        # Ajouter une indication visuelle de l'humeur
        mood_indicators = {
            'friendly': '😊 ',
            'neutral': '😐 ',
            'hostile': '😠 ',
            'happy': '😄 ',
            'sad': '😢 ',
            'angry': '😡 ',
            'surprised': '😲 ',
            'confused': '😕 ',
            'embarrassed': '😳 ',
            'thoughtful': '🤔 '
        }
        
        mood_indicator = ""
        if self.use_emojis and character_mood in mood_indicators:
            mood_indicator = mood_indicators[character_mood]
            
        # Formater le texte pour la boîte
        text_with_mood = f"{mood_indicator}{text}"
        
        # Afficher l'avatar si disponible
        if avatar:
            # Diviser l'écran en deux colonnes
            avatar_width = max(len(line) for line in avatar.split('\n'))
            dialogue_width = self.terminal_width - avatar_width - 8
            
            # Afficher l'avatar et le dialogue côte à côte
            avatar_lines = avatar.split('\n')
            text_lines = self._wrap_text(text_with_mood, dialogue_width)
            
            # Ajouter le nom au début
            dialogue_box = self.draw_box(text_with_mood, width=dialogue_width, 
                                       title=character_name, style='single', color=color)
            
            dialogue_box_lines = dialogue_box.split('\n')
            
            # Assurer que les deux ont le même nombre de lignes
            max_lines = max(len(avatar_lines), len(dialogue_box_lines))
            while len(avatar_lines) < max_lines:
                avatar_lines.append(' ' * avatar_width)
            while len(dialogue_box_lines) < max_lines:
                dialogue_box_lines.append(' ' * dialogue_width)
            
            # Afficher les lignes côte à côte
            for i in range(max_lines):
                print(f"{avatar_lines[i]}  {dialogue_box_lines[i]}")
        else:
            # Afficher simplement la boîte de dialogue
            dialogue_box = self.draw_box(text_with_mood, title=character_name, 
                                       style='single', color=color)
            
            if animate and self.text_speed > 0:
                dialogue_lines = dialogue_box.split('\n')
                for line in dialogue_lines:
                    print(line)
                    time.sleep(self.text_speed * 2)
            else:
                print(dialogue_box)
    
    def _wrap_text(self, text: str, width: int) -> List[str]:
        """
        Effectue un retour à la ligne du texte à une largeur donnée
        
        Args:
            text: Texte à formater
            width: Largeur maximale
            
        Returns:
            Liste des lignes formatées
        """
        lines = []
        for paragraph in text.split('\n'):
            current_line = []
            current_length = 0
            
            for word in paragraph.split():
                word_length = len(word)
                
                if current_length + word_length + 1 <= width:  # +1 pour l'espace
                    current_line.append(word)
                    current_length += word_length + 1
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length
                    
            if current_line:
                lines.append(' '.join(current_line))
                
        return lines
    
    def display_description(self, description: str, title: str = None, color: str = None, animate: bool = True):
        """
        Affiche une description de lieu ou d'objet
        
        Args:
            description: Texte de la description
            title: Titre optionnel
            color: Couleur du texte
            animate: Si True, anime l'affichage du texte
        """
        # Créer une boîte pour la description
        description_box = self.draw_box(description, title=title, style='single', color=color)
        
        if animate and self.text_speed > 0:
            description_lines = description_box.split('\n')
            for line in description_lines:
                print(line)
                time.sleep(self.text_speed)
        else:
            print(description_box)
    
    def display_inventory(self, inventory: List[Dict[str, Any]], gold: int = 0):
        """
        Affiche l'inventaire du joueur
        
        Args:
            inventory: Liste des objets dans l'inventaire
            gold: Quantité d'or possédée
        """
        if not inventory:
            self.print_text("Votre inventaire est vide.", color='info')
            return
            
        # En-tête de l'inventaire
        gold_symbol = f"{self.SYMBOLS['gold']} " if self.use_emojis else ""
        self.print_header(f"Inventaire ({len(inventory)} objets)", 
                        f"{gold_symbol}{self.COLORS['gold']}{gold} pièces d'or{Style.RESET_ALL}")
        
        # Regrouper par catégorie
        categories = {}
        for item in inventory:
            category = item.get("category", "Divers")
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        # Afficher par catégorie
        for category, items in categories.items():
            self.print_text(f"\n{category}:", color='subtitle', bold=True)
            
            for item in items:
                # Déterminer la rareté/couleur
                rarity = item.get("rarity", "common")
                if rarity == "rare":
                    color = "rare_item"
                elif rarity == "epic":
                    color = "epic_item"
                elif rarity == "legendary":
                    color = "legendary_item"
                else:
                    color = "item"
                    
                # Afficher le nom, la quantité et la description
                name = item.get("name", "Objet inconnu")
                count = item.get("count", 1)
                description = item.get("description", "")
                
                item_symbol = ""
                if self.use_emojis:
                    item_type = item.get("type", "")
                    if item_type == "weapon":
                        item_symbol = f"{self.SYMBOLS['sword']} "
                    elif item_type == "armor":
                        item_symbol = f"{self.SYMBOLS['shield']} "
                    elif item_type == "potion":
                        item_symbol = f"{self.SYMBOLS['potion']} "
                    elif item_type == "book":
                        item_symbol = f"{self.SYMBOLS['book']} "
                    else:
                        item_symbol = f"{self.SYMBOLS['item']} "
                
                self.print_text(f"{item_symbol}{self.COLORS[color]}{name}{Style.RESET_ALL} x{count}", color=None)
                if description:
                    self.print_text(f"  {description}", color='info')
    
    def display_skills(self, skills: Dict[str, Dict[str, Any]]):
        """
        Affiche les compétences du joueur
        
        Args:
            skills: Dictionnaire des compétences apprises
        """
        if not skills:
            self.print_text("Vous n'avez pas encore appris de compétences.", color='info')
            return
            
        # En-tête
        skill_count = len(skills)
        skill_symbol = f"{self.SYMBOLS['skill']} " if self.use_emojis else ""
        self.print_header(f"Compétences ({skill_count})", 
                        f"{skill_symbol}Vos pouvoirs et talents")
        
        # Regrouper par catégorie
        categories = {}
        for skill_id, skill_data in skills.items():
            # Obtenir les infos de la compétence depuis le jeu
            skill_info = {}
            if hasattr(self.game, "skills_data") and "skills" in self.game.skills_data:
                skill_info = self.game.skills_data["skills"].get(skill_id, {})
                
            category = skill_info.get("category", "Général")
            if category not in categories:
                categories[category] = []
                
            # Fusionner les données
            skill_entry = {**skill_info, **skill_data, "id": skill_id}
            categories[category].append(skill_entry)
        
        # Afficher par catégorie
        for category, category_skills in categories.items():
            self.print_text(f"\n{category}:", color='subtitle', bold=True)
            
            for skill in category_skills:
                # Déterminer le type et la couleur
                skill_type = skill.get("type", "active")
                
                if skill_type == "spell":
                    element = skill.get("element", "neutral")
                    color = f"spell_{element}" if f"spell_{element}" in self.COLORS else "info"
                elif skill_type == "passive":
                    color = "success"
                else:
                    color = "normal"
                    
                # Afficher le nom, le niveau et la description
                name = skill.get("name", "Compétence inconnue")
                level = skill.get("level", 1)
                description = skill.get("description", "")
                
                # Ajouter des étoiles pour le niveau
                stars = ""
                if self.use_emojis:
                    stars = self.SYMBOLS['star'] * level
                else:
                    stars = f"Niv. {level}"
                
                self.print_text(f"{self.COLORS[color]}{name}{Style.RESET_ALL} ({stars})", color=None)
                if description:
                    self.print_text(f"  {description}", color='info')
                
                # Afficher la barre de progression si applicable
                if "experience" in skill and "level" in skill:
                    xp = skill.get("experience", 0)
                    # Calculer l'XP pour le niveau suivant si la méthode existe
                    next_level_xp = 0
                    if hasattr(self.game, "character_progression"):
                        next_level_xp = self.game.character_progression._calculate_skill_xp_for_level(level + 1)
                    
                    if next_level_xp > 0:
                        xp_bar = self.get_formatted_status_bar(xp, next_level_xp, width=15, color='exp')
                        self.print_text(f"  Progression: {xp_bar}", color=None)
    
    def display_quests(self, quests: List[Dict[str, Any]], completed_quests: List[str] = None):
        """
        Affiche les quêtes actives et complétées
        
        Args:
            quests: Liste des quêtes actives
            completed_quests: Liste des IDs des quêtes complétées
        """
        # En-tête
        quest_symbol = f"{self.SYMBOLS['quest']} " if self.use_emojis else ""
        self.print_header("Journal de quêtes", f"{quest_symbol}Vos aventures en cours")
        
        # Afficher les quêtes actives
        if quests:
            self.print_text("\nQuêtes actives:", color='subtitle', bold=True)
            for quest in quests:
                # Obtenir les infos
                title = quest.get("title", "Quête sans nom")
                description = quest.get("description", "")
                objectives = quest.get("objectives", [])
                
                # Afficher la quête
                self.print_text(f"{self.COLORS['highlight']}{title}{Style.RESET_ALL}", color=None)
                if description:
                    self.print_text(f"  {description}", color='info')
                
                # Afficher les objectifs
                if objectives:
                    for obj in objectives:
                        obj_desc = obj.get("description", "")
                        completed = obj.get("completed", False)
                        
                        # Symbole pour l'état d'achèvement
                        status = ""
                        if self.use_emojis:
                            status = f"{self.SYMBOLS['success']} " if completed else f"{self.SYMBOLS['dot']} "
                        else:
                            status = "[✓] " if completed else "[ ] "
                            
                        self.print_text(f"  {status}{obj_desc}", color='success' if completed else 'normal')
        else:
            self.print_text("Aucune quête active.", color='info')
        
        # Afficher les quêtes complétées
        if completed_quests and hasattr(self.game, "quests_data"):
            self.print_text("\nQuêtes complétées:", color='subtitle', bold=True)
            
            for quest_id in completed_quests:
                # Obtenir le titre de la quête
                quest_info = self.game.quests_data.get(quest_id, {})
                title = quest_info.get("title", f"Quête {quest_id}")
                
                # Afficher avec une coche
                check = f"{self.SYMBOLS['success']} " if self.use_emojis else "[✓] "
                self.print_text(f"{check}{self.COLORS['success']}{title}{Style.RESET_ALL}", color=None)
    
    def display_combat_interface(self, player_stats: Dict[str, Any], enemy_stats: Dict[str, Any], 
                               combat_log: List[str] = None, available_actions: List[Dict[str, Any]] = None):
        """
        Affiche l'interface de combat
        
        Args:
            player_stats: Statistiques du joueur
            enemy_stats: Statistiques de l'ennemi
            combat_log: Historique des actions du combat
            available_actions: Actions disponibles pour le joueur
        """
        self.clear_screen()
        
        # En-tête du combat
        enemy_name = enemy_stats.get("name", "Ennemi")
        enemy_level = enemy_stats.get("level", 1)
        enemy_symbol = f"{self.SYMBOLS['enemy']} " if self.use_emojis else ""
        
        self.print_header(f"Combat contre {enemy_name}", f"{enemy_symbol}Niveau {enemy_level}")
        
        # Afficher les barres de vie
        player_hp = player_stats.get("current_hp", 0)
        player_max_hp = player_stats.get("max_hp", 100)
        player_mp = player_stats.get("current_mp", 0)
        player_max_mp = player_stats.get("max_mp", 50)
        
        enemy_hp = enemy_stats.get("current_hp", 0)
        enemy_max_hp = enemy_stats.get("max_hp", 100)
        
        # Symboles pour les barres de statut
        hp_symbol = f"{self.SYMBOLS['health']} " if self.use_emojis else "HP: "
        mp_symbol = f"{self.SYMBOLS['mana']} " if self.use_emojis else "MP: "
        
        # Créer les barres de statut
        player_hp_bar = self.get_formatted_status_bar(player_hp, player_max_hp, width=15, color='health')
        player_mp_bar = self.get_formatted_status_bar(player_mp, player_max_mp, width=15, color='mana')
        enemy_hp_bar = self.get_formatted_status_bar(enemy_hp, enemy_max_hp, width=20, color='health')
        
        # Afficher les statistiques
        print(f"{self.COLORS['normal']}Vous{Style.RESET_ALL}  {hp_symbol}{player_hp_bar}  {mp_symbol}{player_mp_bar}")
        print(f"{self.COLORS['error']}{enemy_name}{Style.RESET_ALL}  {hp_symbol}{enemy_hp_bar}")
        
        # Afficher le journal de combat
        self.print_divider('light')
        if combat_log:
            for i, log_entry in enumerate(combat_log[-5:]):  # Afficher les 5 dernières entrées
                self.print_text(log_entry)
                
        # Afficher les actions disponibles
        if available_actions:
            self.print_divider('light')
            self.print_text("Actions disponibles:", color='subtitle')
            
            for i, action in enumerate(available_actions, 1):
                action_name = action.get("name", f"Action {i}")
                action_desc = action.get("description", "")
                
                # Déterminer la couleur selon le type d'action
                action_type = action.get("type", "normal")
                if action_type == "attack":
                    color = "warning"
                elif action_type == "spell":
                    color = "mana"
                elif action_type == "item":
                    color = "info"
                else:
                    color = "normal"
                    
                self.print_text(f"{i}. {self.COLORS[color]}{action_name}{Style.RESET_ALL}", color=None)
                if action_desc:
                    self.print_text(f"   {action_desc}", color='info')
    
    def display_level_up(self, old_level: int, new_level: int, gained_stats: Dict[str, Any]):
        """
        Affiche une animation de montée de niveau
        
        Args:
            old_level: Ancien niveau
            new_level: Nouveau niveau
            gained_stats: Statistiques gagnées
        """
        level_symbol = f"{self.SYMBOLS['level']} " if self.use_emojis else ""
        
        # Animation de montée de niveau
        self.animate_text(f"\n{level_symbol} MONTÉE DE NIVEAU ! {level_symbol}", animation_type='blink', color='highlight')
        
        # Afficher les détails
        self.print_text(f"Vous êtes passé du niveau {old_level} au niveau {new_level} !", color='success')
        
        # Afficher les stats gagnées
        for stat, value in gained_stats.items():
            if stat == "attribute_points":
                self.print_text(f"  • Points d'attribut gagnés : +{value}", color='normal')
            elif stat == "skill_points":
                self.print_text(f"  • Points de compétence gagnés : +{value}", color='normal')
            else:
                self.print_text(f"  • {stat.capitalize()} : +{value}", color='normal')
    
    def display_notification(self, message: str, type: str = 'info', dismiss_after: int = None):
        """
        Affiche une notification
        
        Args:
            message: Message de notification
            type: Type de notification ('info', 'success', 'warning', 'error')
            dismiss_after: Temps en secondes avant disparition (None = attendre l'utilisateur)
        """
        # Déterminer le style et le symbole
        symbol = ""
        if self.use_emojis:
            if type == 'success':
                symbol = f"{self.SYMBOLS['success']} "
            elif type == 'warning':
                symbol = f"{self.SYMBOLS['warning']} "
            elif type == 'error':
                symbol = f"{self.SYMBOLS['failure']} "
            else:
                symbol = f"{self.SYMBOLS['info']} "
        
        # Afficher la notification
        notification_text = f"{symbol}{message}"
        notification_box = self.draw_box(notification_text, color=type)
        
        print(notification_box)
        
        # Attendre si nécessaire
        if dismiss_after:
            time.sleep(dismiss_after)
        else:
            input(f"{self.COLORS['prompt']}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
    
    def display_save_load_menu(self, save_slots: List[Dict[str, Any]]):
        """
        Affiche un menu de sauvegarde/chargement
        
        Args:
            save_slots: Liste des emplacements de sauvegarde disponibles
            
        Returns:
            Dictionnaire avec l'action et l'emplacement choisis
        """
        self.print_header("Sauvegarder / Charger", "Gérer vos parties")
        
        save_symbol = f"{self.SYMBOLS['save']} " if self.use_emojis else ""
        load_symbol = f"{self.SYMBOLS['load']} " if self.use_emojis else ""
        
        # Afficher les emplacements disponibles
        if save_slots:
            self.print_text("\nSauvegardes disponibles:", color='subtitle')
            
            for i, slot in enumerate(save_slots, 1):
                # Extraire les informations
                slot_name = slot.get("slot_name", f"Emplacement {i}")
                save_time = slot.get("metadata", {}).get("last_save_time", "Date inconnue")
                play_time = slot.get("metadata", {}).get("play_time", 0)
                play_time_str = self._format_playtime(play_time)
                
                # Formater l'affichage
                self.print_text(f"{i}. {self.COLORS['highlight']}{slot_name}{Style.RESET_ALL}", color=None)
                self.print_text(f"   Dernière sauvegarde: {save_time}", color='info')
                self.print_text(f"   Temps de jeu: {play_time_str}", color='info')
                
                player_info = slot.get("metadata", {}).get("player_info", {})
                if player_info:
                    level = player_info.get("level", 1)
                    location = player_info.get("location", "Lieu inconnu")
                    self.print_text(f"   Niveau {level}, {location}", color='info')
        else:
            self.print_text("Aucune sauvegarde disponible.", color='info')
        
        # Afficher les options
        options = []
        
        # Option de sauvegarde
        options.append((f"{save_symbol}Sauvegarder la partie", {"action": "save"}))
        
        # Options de chargement si des sauvegardes sont disponibles
        if save_slots:
            for i, slot in enumerate(save_slots, 1):
                slot_name = slot.get("slot_name", f"Emplacement {i}")
                options.append((f"{load_symbol}Charger {slot_name}", {"action": "load", "slot": i-1}))
        
        # Option pour revenir au jeu
        options.append(("Retour au jeu", {"action": "cancel"}))
        
        # Demander le choix de l'utilisateur
        return self.display_menu("Que souhaitez-vous faire ?", options, "Votre choix: ")
    
    def _format_playtime(self, seconds: int) -> str:
        """
        Formate un temps de jeu en heures, minutes, secondes
        
        Args:
            seconds: Temps de jeu en secondes
            
        Returns:
            Temps formaté
        """
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        elif minutes > 0:
            return f"{int(minutes)}m {int(seconds)}s"
        else:
            return f"{int(seconds)}s"
    
    def display_help(self, commands: Dict[str, str]):
        """
        Affiche un écran d'aide avec les commandes disponibles
        
        Args:
            commands: Dictionnaire des commandes et leurs descriptions
        """
        self.print_header("Aide", "Liste des commandes disponibles")
        
        for cmd, description in commands.items():
            self.print_text(f"{self.COLORS['prompt']}{cmd}{Style.RESET_ALL}", color=None)
            self.print_text(f"  {description}", color='info')
            
        self.print_text("\nAppuyez sur Entrée pour revenir au jeu...", color='normal')
        input()
    
    def display_loading_screen(self, message: str = "Chargement...", duration: float = 1.0):
        """
        Affiche un écran de chargement
        
        Args:
            message: Message à afficher
            duration: Durée minimale d'affichage en secondes
        """
        self.clear_screen()
        
        # Afficher le message de chargement
        self.print_text(message, color='info', center=True)
        
        # Animer un indicateur de progression
        width = min(40, self.terminal_width - 10)
        
        start_time = time.time()
        progress = 0
        
        while time.time() - start_time < duration:
            # Mise à jour de la barre de progression
            progress = min(1.0, (time.time() - start_time) / duration)
            filled = int(width * progress)
            
            # Dessiner la barre
            bar = f"[{self.COLORS['success']}{'■' * filled}{Style.RESET_ALL}{'□' * (width - filled)}]"
            percent = int(progress * 100)
            
            # Afficher la barre
            sys.stdout.write(f"\r{' ' * ((self.terminal_width - width - 7) // 2)}{bar} {percent}%")
            sys.stdout.flush()
            
            time.sleep(0.05)
        
        # Terminer avec une barre complète
        bar = f"[{self.COLORS['success']}{'■' * width}{Style.RESET_ALL}]"
        sys.stdout.write(f"\r{' ' * ((self.terminal_width - width - 7) // 2)}{bar} 100%")
        sys.stdout.flush()
        
        print("\n\n")
        
        # Afficher une astuce si activé
        if self.show_hints:
            hints = [
                "Appuyez sur 'h' pour afficher l'aide à tout moment.",
                "Les sorts de soin sont particulièrement utiles dans les donjons difficiles.",
                "N'oubliez pas de sauvegarder régulièrement votre progression.",
                "Améliorez vos compétences pour débloquer des techniques puissantes.",
                "Les objets rares peuvent être trouvés en explorant des zones dangereuses.",
                "Parler aux PNJ peut révéler des quêtes secrètes et des informations utiles.",
                "Certains ennemis sont vulnérables à des types d'attaques spécifiques.",
                "Améliorer votre réputation auprès des marchands vous donnera de meilleurs prix.",
                "Méditez pour restaurer votre mana plus rapidement.",
                "Les livres trouvés en exploration peuvent contenir des connaissances précieuses."
            ]
            
            hint = random.choice(hints)
            self.print_text(f"{self.SYMBOLS['info'] if self.use_emojis else 'ASTUCE:'} {hint}", 
                          color='highlight', center=True)
            
        time.sleep(0.5)
    
    def display_game_over(self, reason: str = None, score: int = None):
        """
        Affiche un écran de fin de jeu
        
        Args:
            reason: Raison de la fin du jeu
            score: Score final du joueur
        """
        self.clear_screen()
        
        # ASCII art "Game Over"
        game_over_art = f'''{Fore.RED + Style.BRIGHT}
   ▄████  ▄▄▄       ███▄ ▄███▓▓█████     ▒█████   ██▒   █▓▓█████  ██▀███  
  ██▒ ▀█▒▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒
 ▒██░▄▄▄░▒██  ▀█▄  ▓██    ▓██░▒███      ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒
 ░▓█  ██▓░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  
 ░▒▓███▀▒ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒
  ░▒   ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░
   ░   ░   ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░
 ░ ░   ░   ░   ▒   ░      ░      ░      ░ ░ ░ ▒       ░░     ░     ░░   ░ 
       ░       ░  ░       ░      ░  ░       ░ ░        ░     ░  ░   ░     
                                                      ░                   
{Style.RESET_ALL}'''
        print(game_over_art)
        
        # Afficher la raison de la fin du jeu
        if reason:
            self.print_text(reason, color='error', center=True)
            
        # Afficher le score
        if score is not None:
            self.print_text(f"\nScore final: {score}", color='highlight', center=True)
            
        # Afficher les options
        self.print_divider('heavy')
        
        options = [
            ("Charger une sauvegarde", "load"),
            ("Retourner au menu principal", "menu"),
            ("Quitter le jeu", "quit")
        ]
        
        return self.display_menu("Que souhaitez-vous faire ?", options)
    
    def display_character_creation(self, available_classes: List[Dict[str, Any]], 
                                  available_attributes: List[Dict[str, Any]]):
        """
        Affiche l'interface de création de personnage
        
        Args:
            available_classes: Liste des classes disponibles
            available_attributes: Liste des attributs disponibles
            
        Returns:
            Dictionnaire avec les choix du personnage
        """
        self.print_header("Création de personnage", "Façonnez votre nouvelle vie dans ce monde")
        
        # Demander le nom
        self.print_text("Comment voulez-vous vous appeler ?", color='prompt')
        name = self.get_user_input("Nom: ")
        
        # Afficher les classes disponibles
        self.print_divider()
        self.print_text("Choisissez votre classe:", color='prompt')
        
        class_options = []
        for i, class_data in enumerate(available_classes, 1):
            class_name = class_data.get("name", f"Classe {i}")
            class_id = class_data.get("id", f"class_{i}")
            class_desc = class_data.get("description", "")
            
            self.print_text(f"{i}. {self.COLORS['highlight']}{class_name}{Style.RESET_ALL}", color=None)
            self.print_text(f"   {class_desc}", color='info')
            
            class_options.append((class_name, class_id))
        
        # Demander la classe
        while True:
            choice = input(f"{self.COLORS['prompt']}Votre choix (1-{len(available_classes)}): {self.COLORS['input']}")
            print(Style.RESET_ALL, end="")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_classes):
                    chosen_class = class_options[choice_num - 1][1]
                    break
                else:
                    print(f"{self.COLORS['error']}Choix invalide.{Style.RESET_ALL}")
            except ValueError:
                print(f"{self.COLORS['error']}Veuillez entrer un nombre.{Style.RESET_ALL}")
        
        # Répartir les points d'attributs
        self.print_divider()
        self.print_text("Répartissez vos points d'attributs:", color='prompt')
        
        attribute_points = 20  # Points à répartir
        attributes = {}
        
        # Initialiser tous les attributs à 10
        for attr_data in available_attributes:
            attr_id = attr_data.get("id", "attr")
            attr_name = attr_data.get("name", "Attribut")
            attr_desc = attr_data.get("description", "")
            
            attributes[attr_id] = 10
            self.print_text(f"{self.COLORS['highlight']}{attr_name}{Style.RESET_ALL}: {attributes[attr_id]}", color=None)
            self.print_text(f"   {attr_desc}", color='info')
        
        # Répartition des points
        self.print_text(f"\nPoints restants: {attribute_points}", color='success')
        
        for attr_data in available_attributes:
            attr_id = attr_data.get("id", "attr")
            attr_name = attr_data.get("name", "Attribut")
            
            while True:
                points_to_add = input(f"{self.COLORS['prompt']}Points à ajouter à {attr_name} (0-{attribute_points}): {self.COLORS['input']}")
                print(Style.RESET_ALL, end="")
                
                try:
                    points = int(points_to_add)
                    if 0 <= points <= attribute_points:
                        attributes[attr_id] += points
                        attribute_points -= points
                        self.print_text(f"{attr_name} augmenté à {attributes[attr_id]}", color='success')
                        self.print_text(f"Points restants: {attribute_points}", color='info')
                        break
                    else:
                        print(f"{self.COLORS['error']}Nombre de points invalide.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{self.COLORS['error']}Veuillez entrer un nombre.{Style.RESET_ALL}")
            
                        # Arrêter la répartition des points si tous ont été utilisés
            if attribute_points == 0:
                break
        
        # Récapitulatif des choix
        self.print_divider()
        self.print_text("Récapitulatif de votre personnage:", color='highlight', center=True)
        self.print_text(f"Nom: {name}", color='normal')
        
        # Récupérer le nom de la classe choisie
        class_name = ""
        for cname, cid in class_options:
            if cid == chosen_class:
                class_name = cname
                break
        
        self.print_text(f"Classe: {class_name}", color='normal')
        self.print_text("Attributs:", color='normal')
        
        for attr_data in available_attributes:
            attr_id = attr_data.get("id", "attr")
            attr_name = attr_data.get("name", "Attribut")
            self.print_text(f"  {attr_name}: {attributes[attr_id]}", color='info')
        
        # Confirmation
        self.print_text("\nÊtes-vous satisfait de votre personnage?", color='prompt')
        confirm_options = [
            ("Oui, commencer l'aventure", True),
            ("Non, recommencer la création", False)
        ]
        
        confirmed = self.display_menu("Confirmation", confirm_options)
        
        if confirmed:
            return {
                "name": name,
                "class": chosen_class,
                "attributes": attributes
            }
        else:
            # Relancer la création de personnage
            return self.display_character_creation(available_classes, available_attributes)