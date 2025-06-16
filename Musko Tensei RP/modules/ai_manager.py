# ai_manager.py - Module de gestion de l'IA pour MUSKO TENSEI RP
import json
import os
import random
import time
import requests
from typing import Dict, List, Any, Optional, Tuple
import re

class AIManager:
    def __init__(self, game_instance=None, model_name="mistral-7b-instruct-v0.2", lm_studio_api_url="http://127.0.0.1:1234/v1"):
        """
        Initialise le gestionnaire d'IA pour MUSKO TENSEI RP.
        
        Args:
            game_instance: Instance du jeu principal
            model_name: Le modèle LLM à utiliser
            lm_studio_api_url: L'URL de l'API LM Studio
        """
        print("Initialisation du gestionnaire d'IA...")
        self.game = game_instance
        self.model_name = model_name
        self.lm_studio_api_url = lm_studio_api_url
        
        # Charger les données
        self.interaction_data = self._load_data("interactions")
        self.mature_data = self._load_data("mature")
        self.character_data = self._load_data("npcs")
        self.location_data = self._load_data("locations")
        self.item_data = self._load_data("items")
        
        # Système d'historique et de mémoire
        self.conversation_history = []
        self.memory_by_character = {}
        self.world_state_memory = {}
        
        # Paramètres de personnalisation du style narratif
        self.narrative_style = {
            "descriptive_detail": 0.8,  # 0-1, niveau de détail descriptif
            "sensory_immersion": 0.7,   # 0-1, immersion sensorielle
            "dialogue_quality": 0.9,    # 0-1, naturel et qualité des dialogues
            "emotional_tone": "balanced" # neutral, passionate, somber, humorous, balanced
        }
        
        # Cache pour les descriptions générées
        self.description_cache = {}
        
        # Limite de l'historique de conversation par personnage
        self.history_limit = 20
        
        # Personnalité du joueur détectée au fil du temps
        self.player_personality = {
            "kindness": 0,      # -1 à 1 (cruel à gentil)
            "boldness": 0,      # -1 à 1 (prudent à téméraire)
            "lechery": 0,       # -1 à 1 (vertueux à libidineux)
            "greed": 0,         # -1 à 1 (généreux à avare)
            "intelligence": 0,  # -1 à 1 (impulsif à réfléchi)
            "honor": 0          # -1 à 1 (sournois à honorable)
        }
        
        # Races disponibles dans le monde de MUSKO TENSEI
        self.available_races = [
            "Human Race", 
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
        
        # Descriptions détaillées des races
        self.race_descriptions = {
            "Human Race": "La Human Race est la race dominante dans le monde de Mushoku Tensei. Répandus sur le Continent Central, les humains possèdent une vaste diversité culturelle, politique et magique. Ils ne disposent pas de traits physiques distinctifs mais bénéficient d'une adaptabilité exceptionnelle. Certaines lignées nobles comme les Greyrat ont des spécialisations guerrières ou magiques. Leur société est structurée en royaumes (Asura, Shirone…) et académies de magie comme Ranoa.",
            
            "High Elf Race": "La High Elf Race est composée d'humanoïdes aux longues oreilles et à l'apparence gracieuse. Ils vivent principalement dans des forêts reculées, sous des systèmes matriarcaux ou tribaux. Leur longévité atteint plusieurs siècles. Ils sont connus pour leur affinité naturelle avec la magie, particulièrement la magie élémentaire. Les mariages interraciaux sont rares et parfois mal vus par leur société conservatrice.",
            
            "Dwarf Race": "La Dwarf Race est connue pour sa robustesse physique, sa petite taille, et sa grande maîtrise de la forge et de la minéralogie. Les nains vivent dans les montagnes ou en villes souterraines, organisés en clans fortement hiérarchisés. Peu portés sur la magie, ils excellent dans le maniement des armes lourdes et la fabrication d'équipements de haute qualité. Ils sont aussi réputés pour leur amour de l'alcool.",
            
            "Halfling Race": "La Halfling Race est composée de petits humanoïdes à l'apparence juvénile. Ils vivent dans des régions rurales, à l'écart des grands conflits. Ils sont pacifiques, orientés vers l'agriculture, l'artisanat et la vie communautaire. Ils ne possèdent ni puissance magique particulière ni capacité de combat exceptionnelle. Très rares dans le récit, ils incarnent la simplicité et la discrétion.",
            
            "Dragon Tribe": "La Dragon Tribe est une race ancienne venue du Dragon World. Ses membres présentent souvent des traits draconiques comme des écailles, des ailes ou une force surhumaine. Ils utilisent le Touki (aura de combat) et sont experts en combat martial et magique. Leur société est structurée autour des 'Cinq Généraux Dragons'. Le plus connu, Orsted, est le descendant direct du Dieu Dragon. Leur puissance fait d'eux des êtres redoutés et isolés.",
            
            "Migurd Race": "La Migurd Race est une branche des Demon Races. Ses membres ont une apparence enfantine, des cheveux et yeux bleus. Leur longévité dépasse les 200 ans, avec une croissance extrêmement lente. Ils possèdent une capacité télépathique entre eux, leur permettant de communiquer sans mots. Pacifiques, ils vivent en petites communautés isolées. Roxy Migurdia, célèbre tutrice de Rudeus, est issue de cette race.",
            
            "Superd Race": "La Superd Race est une tribu de guerriers démoniaques reconnaissables à leur peau verte, leurs cheveux violets, et leur gemme frontale rouge qui leur sert de troisième œil. Cette gemme leur permet de percevoir le mana et les êtres vivants. À la maturité, leur queue se transforme en une arme rigide semblable à un trident. Anciennement manipulés par Laplace, ils furent accusés à tort de massacre, menant à leur rejet par toutes les autres races. Ruijerd Superdia est le dernier représentant actif connu.",
            
            "Immortal Demon Race": "La Immortal Demon Race est constituée d'individus démoniaques capables de se régénérer même après des blessures mortelles. Leur immortalité est réelle mais peut entraîner une perte d'humanité ou une dégénérescence mentale. Atofe Raibaku en est le parfait exemple : une générale immortelle puissante mais psychologiquement instable. Cette race vit souvent en marge, crainte autant qu'admirée.",
            
            "Ogre Race": "La Ogre Race est une branche démoniaque primitive et brutale. Ces humanoïdes possèdent des cornes, une force physique énorme, mais une intelligence limitée. Ils sont peu réceptifs à la magie, mais redoutables au corps-à-corps. Leur culture est tribale et souvent soumise à des races plus stratèges ou magiciennes. Ils sont parfois utilisés comme gardes ou soldats mercenaires.",
            
            "Beast Race": "La Beast Race est composée d'anthropomorphes animaux, divisés en nombreuses sous-races (félins, canins, ursidés, etc.). Ils possèdent des oreilles, queues, et sens accrus. Ils vivent dans la Great Forest, organisés en tribus comme les Dorudia (félins) et Adorudia (canins). Ils sont loyaux, tribaux, et dotés d'une affinité naturelle avec le mana. Leurs traditions sont rigoureuses et respectées. Linia et Pursena en sont des exemples célèbres.",
            
            "Heaven Race": "La Heaven Race est une race extrêmement rare, supposément liée aux divinités ou aux entités célestes. Leurs capacités ne sont pas bien documentées, mais ils seraient dotés de pouvoirs surnaturels. Leur apparence est humanoïde, parfois éthérée. Ils sont cités dans les écrits anciens comme des entités supérieures ou gardiens cosmiques. Peu d'exemples concrets sont connus dans le récit.",
            
            "Sea Race": "La Sea Race (ou Ocean Race) regroupe des humanoïdes aquatiques vivant dans les zones marines ou côtières. Ils sont adaptés à la vie sous l'eau et possèdent des capacités comme la respiration aquatique, la nage rapide ou une affinité avec la magie de l'eau. Très peu explorés dans le récit principal, ils sont toutefois confirmés dans le lore comme existants et organisés en tribus marines.",
            
            "Mixed-Blood Race": "La Mixed-Blood Race désigne tous les individus issus d'unions interraciales (ex. humain + elfe, bête + démon…). Ils héritent de caractéristiques mixtes, parfois avantageuses, parfois conflictuelles. Souvent mal vus ou rejetés, ils doivent lutter pour leur reconnaissance. Sylphiette est une descendante humaine, elfe, et partiellement bestiale. Leur diversité est telle qu'aucune classification unique ne peut les résumer.",
            
            "Cursed Children": "Les Cursed Children sont des individus marqués par une malédiction divine, démoniaque ou magique. Ces malédictions affectent leur physique, leur esprit, ou leur interaction sociale. Orsted est par exemple victime d'une malédiction qui empêche les autres de le côtoyer sans peur. Ils sont souvent bannis, craints ou tués à la naissance. Certains développent des capacités uniques malgré la souffrance qu'elles entraînent.",
            
            "Elemental Spirits": "Les Elemental Spirits sont des entités nées de la concentration pure de mana élémentaire. Ils n'ont pas de forme stable, sont semi-éthérés, et possèdent des pouvoirs dévastateurs. Ils sont très peu connus, même dans les cercles de magie avancée. On suppose qu'ils maintiennent des équilibres magiques à l'échelle planétaire. Aucun n'a été rencontré directement dans le récit, mais ils sont évoqués dans les grimoires anciens.",
            
            "Sylphs": "Les Sylphs sont des fées du vent, très petites et insaisissables. Elles sont liées à l'élément air et sont capables de manipuler les courants, disparaître dans l'atmosphère, ou créer de petites tornades. Leur présence est anecdotique dans le récit, mais elles existent dans le lore étendu et les récits parallèles. Elles vivent recluses dans des zones d'altitude ou magiquement actives.",
            
            "Ancient Races": "Les Ancient Races regroupent les peuples disparus ou mythologiques de l'univers de Mushoku Tensei. Ils sont mentionnés dans les ruines, les artefacts oubliés, ou les anciens sorts. Leurs capacités, connaissances ou lignées ont parfois survécu à travers les races modernes. Ils sont considérés comme la source d'artefacts magiques ou de runes perdues."
        }
        
        # Tester la connexion à LM Studio au démarrage
        self.test_connection()
    
    def _load_data(self, data_name: str) -> Dict:
        """Charge un fichier de données JSON"""
        try:
            filepath = f"data/{data_name}.json"
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Erreur lors du chargement de {data_name}.json: {e}")
            return {}
    
    def _trim_history(self, history: List, limit: int = None) -> List:
        """Limite la taille de l'historique"""
        if limit is None:
            limit = self.history_limit
        if len(history) > limit:
            return history[-limit:]
        return history
    
    def _update_player_personality(self, user_input: str, context: Dict) -> None:
        """
        Analyse l'entrée du joueur pour détecter des traits de personnalité.
        Ce système s'affine au fil du temps pour mieux comprendre le joueur.
        """
        # Mots-clés associés à différents traits
        kindness_pos = ["aider", "sauver", "guérir", "protéger", "donner", "partager", "merci"]
        kindness_neg = ["tuer", "blesser", "abandonner", "ignorer", "souffrir", "détruire"]
        
        boldness_pos = ["attaquer", "défier", "risque", "oser", "aventurer", "explorer"]
        boldness_neg = ["fuir", "cacher", "éviter", "prudent", "attendre"]
        
        lechery_pos = ["séduire", "flirter", "embrasser", "caresser", "déshabiller", "nu", "sexe"]
        
        greed_pos = ["voler", "prendre", "garder", "argent", "or", "trésor", "refuser"]
        greed_neg = ["donner", "partager", "offrir", "générosité", "charité"]
        
        intelligence_pos = ["analyser", "réfléchir", "examiner", "étudier", "plan", "stratégie"]
        intelligence_neg = ["foncer", "immédiatement", "sans réfléchir", "précipiter"]
        
        # Analyse des mots-clés dans l'entrée utilisateur
        input_lower = user_input.lower()
        
        # Exemples de modifications basées sur les mots-clés
        for word in kindness_pos:
            if word in input_lower:
                self.player_personality["kindness"] = min(1.0, self.player_personality["kindness"] + 0.05)
                
        for word in kindness_neg:
            if word in input_lower:
                self.player_personality["kindness"] = max(-1.0, self.player_personality["kindness"] - 0.05)
        
        # Analyse du contexte (ex: le joueur aide-t-il lors d'une quête?)
        action_type = context.get("action_type", "")
        if action_type == "help_npc" or action_type == "save_npc":
            self.player_personality["kindness"] = min(1.0, self.player_personality["kindness"] + 0.1)
        elif action_type == "attack_innocent" or action_type == "steal":
            self.player_personality["kindness"] = max(-1.0, self.player_personality["kindness"] - 0.1)
            self.player_personality["honor"] = max(-1.0, self.player_personality["honor"] - 0.1)
    
    def add_to_history(self, character_id: str, message: Dict) -> None:
        """
        Ajoute un message à l'historique des conversations avec un personnage spécifique
        """
        if character_id not in self.memory_by_character:
            self.memory_by_character[character_id] = {"conversations": [], "relationships": {}, "events": []}
            
        self.memory_by_character[character_id]["conversations"].append(message)
        self.memory_by_character[character_id]["conversations"] = self._trim_history(
            self.memory_by_character[character_id]["conversations"]
        )
        
        # Ajouter également à l'historique général
        self.conversation_history.append({
            "character_id": character_id,
            "message": message
        })
        self.conversation_history = self._trim_history(self.conversation_history)
    
    def record_event(self, event_type: str, event_data: Dict) -> None:
        """
        Enregistre un événement important dans la mémoire du monde
        
        Args:
            event_type: Type d'événement (combat, quest, relationship, etc.)
            event_data: Données relatives à l'événement
        """
        if event_type not in self.world_state_memory:
            self.world_state_memory[event_type] = []
            
        event_data["timestamp"] = time.time()
        self.world_state_memory[event_type].append(event_data)
        
        # Si l'événement concerne un personnage spécifique, enregistrez-le aussi dans sa mémoire
        character_id = event_data.get("character_id")
        if character_id:
            if character_id not in self.memory_by_character:
                self.memory_by_character[character_id] = {"conversations": [], "relationships": {}, "events": []}
            
            self.memory_by_character[character_id]["events"].append({
                "type": event_type,
                "data": event_data,
                "timestamp": event_data["timestamp"]
            })
    
    def update_relationship(self, character_id: str, relationship_change: Dict) -> None:
        """
        Met à jour la relation avec un personnage
        
        Args:
            character_id: ID du personnage
            relationship_change: Changements à appliquer à la relation
        """
        if character_id not in self.memory_by_character:
            self.memory_by_character[character_id] = {"conversations": [], "relationships": {}, "events": []}
            
        for key, value in relationship_change.items():
            if key in self.memory_by_character[character_id]["relationships"]:
                self.memory_by_character[character_id]["relationships"][key] += value
            else:
                self.memory_by_character[character_id]["relationships"][key] = value
    
    def set_narrative_style(self, style_params: Dict) -> None:
        """
        Configure le style narratif du gestionnaire d'IA
        
        Args:
            style_params: Paramètres de style à modifier
        """
        for key, value in style_params.items():
            if key in self.narrative_style:
                self.narrative_style[key] = value
    
    def generate_response(self, prompt: str, context: Dict = None) -> Any:
        """
        Génère une réponse basée sur le prompt et le contexte.
        C'est la méthode principale utilisée par le jeu pour interagir avec l'IA.
        
        Args:
            prompt: Entrée utilisateur ou prompt interne
            context: Contexte de la demande (personnage, lieu, etc.)
            
        Returns:
            Réponse générée, peut être un texte ou une structure plus complexe selon le contexte
        """
        if context is None:
            context = {}
            
        # Mise à jour de la personnalité du joueur
        self._update_player_personality(prompt, context)
        
        # Déterminer le type d'interaction
        interaction_type = context.get("interaction_type", "dialogue")
        
        # Générer la réponse avec LM Studio
        try:
            # Format compatible avec LM Studio 0.3.16 pour Mistral
            # Créer un prompt d'instruction qui combine ce qui aurait été le message système avec l'entrée utilisateur
            system_instruction = (
                f"Tu es l'IA narrative du jeu de rôle MUSKO TENSEI RP, inspiré par l'univers de Mushoku Tensei. "
                f"Tu dois créer des réponses immersives qui font sentir au joueur qu'il EST réellement dans ce monde. "
                f"IMPORTANT: Fais extrêmement attention à l'orthographe et à la grammaire française. Relis-toi et vérifie systématiquement "
                f"tes écrits. Évite les fautes d'accord, de conjugaison ou de syntaxe qui briseraient l'immersion. "
                f"Type d'interaction actuelle: {interaction_type}. "
                f"Style narratif: Détails descriptifs ({int(self.narrative_style['descriptive_detail']*100)}%), "
                f"Immersion sensorielle ({int(self.narrative_style['sensory_immersion']*100)}%), "
                f"Ton émotionnel: {self.narrative_style['emotional_tone']}."
            )
            
            combined_prompt = f"{system_instruction}\n\nDemande du joueur: {prompt}"
            
            # Utiliser uniquement le rôle "user" pour le prompt combiné
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": combined_prompt}
                ],
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 800
            }
            
            # Afficher la requête pour débogage
            print(f"Envoi de la requête à LM Studio: {self.lm_studio_api_url}/chat/completions")
            
            # Envoyer la requête
            response = requests.post(f"{self.lm_studio_api_url}/chat/completions", 
                                    json=payload, 
                                    headers={"Content-Type": "application/json"})
            
            # Vérifier la réponse
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    if "message" in result["choices"][0]:
                        generated_text = result["choices"][0]["message"]["content"]
                    else:
                        generated_text = result["choices"][0].get("text", "")
                else:
                    generated_text = "Je ne sais pas quoi dire."
                
                print("✅ Connexion à LM Studio réussie!")
                
                # Post-traitement de la réponse
                processed_response = self._process_response(generated_text, interaction_type, context)
                
                # Enregistrement de la conversation si c'est un dialogue avec un PNJ
                if interaction_type == "dialogue" and "character_id" in context:
                    self.add_to_history(context["character_id"], {
                        "role": "assistant", 
                        "content": processed_response if isinstance(processed_response, str) else processed_response.get("text", "")
                    })
                
                return processed_response
            else:
                print(f"Erreur lors de l'appel à LM Studio: {response.status_code} {response.reason}")
                print(f"Détail de l'erreur: {response.text}")
                return self._get_fallback_response(interaction_type, context)
                
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse: {e}")
            # Fallback sur des réponses pré-écrites en cas d'échec
            return self._get_fallback_response(interaction_type, context)
    
    def _process_response(self, response: str, interaction_type: str, context: Dict) -> Any:
        """
        Traite la réponse brute de l'IA selon le type d'interaction
        
        Args:
            response: Texte brut de la réponse
            interaction_type: Type d'interaction
            context: Contexte de la demande
            
        Returns:
            Réponse traitée, peut être un texte ou une structure de données
        """
        # Nettoyage général
        response = response.strip()
        
        # Enlever les marqueurs potentiels du modèle
        response = re.sub(r'<s>|</s>|\[INST\]|\[/INST\]', '', response).strip()
        
        # Traitement spécifique selon le type d'interaction
        if interaction_type == "dialogue":
            # Pour le dialogue, on veut juste le texte nettoyé
            return response
            
        elif interaction_type == "combat":
            # Pour le combat, on veut extraire les informations structurées si possible
            try:
                # Chercher des motifs comme "Dégâts: X" ou "Action: Y"
                damage_match = re.search(r'Dégâts:?\s*(\d+)', response)
                action_match = re.search(r'Action:?\s*([^\.]+)', response)
                
                structured_data = {
                    "text": response,
                    "damages": int(damage_match.group(1)) if damage_match else None,
                    "action_type": action_match.group(1).strip() if action_match else "attack"
                }
                return structured_data
            except:
                # En cas d'erreur, retourner simplement le texte
                return {"text": response, "action_type": "attack"}
                
        elif interaction_type == "market":
            # Pour une interaction marchande, extraire prix et disposition
            try:
                price_match = re.search(r'Prix:?\s*(\d+)', response)
                mood_match = re.search(r'Disposition:?\s*([^\.]+)', response)
                
                return {
                    "text": response,
                    "price": int(price_match.group(1)) if price_match else None,
                    "merchant_mood": mood_match.group(1).strip() if mood_match else "neutral"
                }
            except:
                return {"text": response}
                
        elif interaction_type == "intimate":
            # Pour le contenu intime, vérifier qu'il correspond au niveau demandé
            intensity = context.get("intensity", "moderate")
            return {
                "text": response,
                "intensity": intensity
            }

        elif interaction_type == "race_description":
            # Pour les descriptions de race, utiliser les descriptions prédéfinies en cas d'échec
            race = context.get("race", "")
            if not response or len(response) < 20:  # Si la réponse est vide ou trop courte
                if race in self.race_descriptions:
                    return self.race_descriptions[race]
            return response
            
        # Par défaut, retourner simplement la réponse textuelle
        return response
    
    def _get_fallback_response(self, interaction_type: str, context: Dict) -> Any:
        """
        Fournit une réponse de secours en cas d'erreur avec l'API
        
        Args:
            interaction_type: Type d'interaction
            context: Contexte de la demande
            
        Returns:
            Réponse de secours
        """
        fallbacks = {
            "dialogue": [
                "Hmm... Je réfléchis à ce que vous venez de dire.",
                "Intéressant. Continuez, je vous écoute.",
                "Je vois ce que vous voulez dire. Que comptez-vous faire ensuite ?"
            ],
            "combat": [
                "Vous échangez des coups avec votre adversaire, cherchant une ouverture dans sa défense.",
                "L'adrénaline pulse dans vos veines alors que vous esquivez une attaque rapide.",
                "Votre adversaire recule sous la force de votre assaut, momentanément déstabilisé."
            ],
            "description": [
                "L'endroit est remarquable par son atmosphère unique et ses détails intrigants.",
                "Les sons et les odeurs de cet endroit créent une ambiance particulière.",
                "Vous observez attentivement les alentours, notant chaque détail important."
            ],
            "market": [
                "Le marchand examine votre offre avec un regard calculateur.",
                "\"Je pourrais peut-être baisser un peu mon prix, mais pas beaucoup...\"",
                "\"C'est de la qualité que je vous propose là ! Le prix est justifié.\""
            ],
            "intimate": [
                "Un moment de connexion intime se développe entre vous.",
                "La proximité crée une tension palpable dans l'air.",
                "Les regards en disent plus que les mots dans ce moment partagé."
            ],
            "race_description": self.race_descriptions  # Utiliser les descriptions de races pré-définies
        }
        
        if interaction_type == "race_description" and "race" in context:
            race = context["race"]
            return fallbacks["race_description"].get(race, "Une race mystérieuse et rare.")
        else:
            if isinstance(fallbacks.get(interaction_type), list):
                return random.choice(fallbacks.get(interaction_type, fallbacks["dialogue"]))
            else:
                return random.choice(fallbacks["dialogue"])
    
    def generate_description(self, location_id: str, time_of_day: str = "day", weather: str = "clear") -> str:
        """
        Génère une description immersive d'un lieu
        
        Args:
            location_id: ID du lieu à décrire
            time_of_day: Moment de la journée (dawn, day, dusk, night)
            weather: Conditions météorologiques (clear, cloudy, rainy, etc.)
            
        Returns:
            Description immersive du lieu
        """
        # Vérifier si une description existe déjà en cache pour ces paramètres
        cache_key = f"{location_id}_{time_of_day}_{weather}"
        if cache_key in self.description_cache:
            return self.description_cache[cache_key]
        
        # Récupérer les données du lieu
        location_data = self.location_data.get(location_id, {})
        location_name = location_data.get("name", "lieu inconnu")
        base_description = location_data.get("description", "Un endroit ordinaire.")
        
        # Contexte pour la génération
        context = {
            "interaction_type": "description",
            "location_id": location_id,
            "location_name": location_name,
            "time_of_day": time_of_day,
            "weather": weather
        }
        
        # Prompt spécifique pour la description
        prompt = (
            f"Décris en détail {location_name} pendant {time_of_day} avec un temps {weather}. "
            f"Fais très attention à l'orthographe et à la grammaire française. "
            f"Utilise des phrases correctes grammaticalement et sans fautes."
        )
        
        # Générer la description
        description = self.generate_response(prompt, context)
        
        # Si la description est vide ou trop courte, utiliser la description de base
        if not description or (isinstance(description, str) and len(description) < 30):
            description = f"{base_description} {self._get_weather_time_description(weather, time_of_day)}"
        
        # Mettre en cache pour réutilisation future
        self.description_cache[cache_key] = description
        
        return description
    
    def _get_weather_time_description(self, weather, time_of_day):
        """Génère une description simple en fonction de la météo et de l'heure"""
        weather_desc = {
            "clear": "Le ciel est dégagé.",
            "cloudy": "Des nuages parsèment le ciel.",
            "rainy": "La pluie tombe doucement.",
            "stormy": "Un orage gronde au loin.",
            "foggy": "Une brume épaisse enveloppe les environs.",
            "snowy": "Des flocons de neige tombent paisiblement."
        }
        
        time_desc = {
            "dawn": "Les premières lueurs du jour apparaissent à l'horizon.",
            "day": "Le soleil illumine pleinement la scène.",
            "dusk": "Le soleil descend lentement, baignant tout dans une lumière dorée.",
            "night": "La nuit a déployé son manteau sombre, ponctué d'étoiles."
        }
        
        return f"{weather_desc.get(weather, '')} {time_desc.get(time_of_day, '')}"
    
    def generate_npc_dialogue(self, character_id: str, dialogue_type: str, user_input: str, additional_context: Dict = None) -> str:
        """
        Génère un dialogue pour un PNJ
        
        Args:
            character_id: ID du personnage
            dialogue_type: Type de dialogue (greeting, quest, trade, etc.)
            user_input: Entrée de l'utilisateur
            additional_context: Contexte supplémentaire
            
        Returns:
            Réponse du PNJ
        """
        # Récupérer les données du personnage
        character_data = self.character_data.get(character_id, {})
        character_name = character_data.get("name", "Inconnu")
        
        # Créer le contexte
        context = {
            "interaction_type": "dialogue",
            "dialogue_type": dialogue_type,
            "character_id": character_id,
            "character_name": character_name,
            "character_data": character_data
        }
        
        # Ajouter le contexte supplémentaire s'il existe
        if additional_context:
            context.update(additional_context)
        
        # Enregistrer l'entrée de l'utilisateur dans l'historique
        self.add_to_history(character_id, {"role": "user", "content": user_input})
        
        # Ajouter une instruction pour éviter les fautes
        dialogue_prompt = (
            f"{user_input}\n\n"
            f"Rappel: Réponds en tant que {character_name}. Fais très attention à l'orthographe "
            f"et à la grammaire française. Évite absolument toute faute qui briserait l'immersion."
        )
        
        # Générer la réponse
        return self.generate_response(dialogue_prompt, context)
    
    def generate_combat_narrative(self, player_data: Dict, enemy_id: str, action: str, combat_state: Dict) -> Dict:
        """
        Génère une narration de combat immersive
        
        Args:
            player_data: Données du joueur
            enemy_id: ID de l'ennemi
            action: Action effectuée par le joueur
            combat_state: État actuel du combat
            
        Returns:
            Narration du combat avec données structurées
        """
        # Récupérer les données de l'ennemi
        enemy_data = self.character_data.get(enemy_id, {})
        enemy_name = enemy_data.get("name", "adversaire")
        
        # Contexte du combat
        combat_context = {
            "interaction_type": "combat",
            "enemy_id": enemy_id,
            "enemy_name": enemy_name,
            "enemy_data": enemy_data,
            "player_data": player_data,
            "action": action,
            "combat_round": combat_state.get("round", 1),
            "player_hp_percent": combat_state.get("player_hp_percent", 100),
            "enemy_hp_percent": combat_state.get("enemy_hp_percent", 100),
            "combat_style": player_data.get("combat_style", "balanced")
        }
        
        # Prompt spécifique selon l'action
        if action == "attack":
            prompt = (
                f"Je {action} {enemy_name} avec mon {player_data.get('weapon', 'arme')}. "
                f"Décris ce combat de façon immersive et dynamique. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        elif action == "skill":
            skill_name = combat_state.get("skill_name", "compétence")
            prompt = (
                f"J'utilise ma compétence {skill_name} contre {enemy_name}. "
                f"Décris l'utilisation de cette compétence et ses effets spectaculaires. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        elif action == "defend":
            prompt = (
                f"Je me mets en position défensive face à {enemy_name}. "
                f"Décris ma posture défensive et la réaction de mon adversaire. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        elif action == "flee":
            prompt = (
                f"Je tente de fuir le combat contre {enemy_name}. "
                f"Décris ma tentative de fuite et la réaction de mon adversaire. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        else:
            prompt = (
                f"Je {action} pendant le combat contre {enemy_name}. "
                f"Décris cette action et son déroulement dans le combat. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        
        # Générer et retourner la narration
        return self.generate_response(prompt, combat_context)
    
    def generate_market_interaction(self, merchant_id: str, item_id: str, action: str, player_data: Dict) -> Dict:
        """
        Génère une interaction de marché réaliste
        
        Args:
            merchant_id: ID du marchand
            item_id: ID de l'objet concerné
            action: Action (buy, sell, haggle)
            player_data: Données du joueur
            
        Returns:
            Interaction de marché avec données structurées
        """
        # Récupérer les données du marchand et de l'objet
        merchant_data = self.character_data.get(merchant_id, {})
        merchant_name = merchant_data.get("name", "marchand")
        
        item_data = self.item_data.get(item_id, {})
        item_name = item_data.get("name", "objet")
        base_price = item_data.get("price", 100)
        
        # Calculer le prix ajusté selon la réputation et le charisme
        charisma_mod = player_data.get("stats", {}).get("charisme", 10) / 10
        reputation_mod = player_data.get("reputation", {}).get(merchant_id, 0) / 100
        price_mod = 1.0 - (charisma_mod * 0.1) - (reputation_mod * 0.2)
        adjusted_price = max(1, int(base_price * price_mod))
        
        # Contexte pour l'interaction
        market_context = {
            "interaction_type": "market",
            "merchant_id": merchant_id,
            "merchant_name": merchant_name,
            "merchant_data": merchant_data,
            "item_id": item_id,
            "item_name": item_name,
            "item_data": item_data,
            "base_price": base_price,
            "adjusted_price": adjusted_price,
            "player_data": player_data,
            "action": action
        }
        
        # Prompt spécifique selon l'action
        if action == "buy":
            prompt = (
                f"Je souhaite acheter {item_name}. Combien ça coûte ? "
                f"Crée un dialogue réaliste avec le marchand {merchant_name}. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        elif action == "sell":
            prompt = (
                f"Je voudrais vendre {item_name}. Combien pouvez-vous m'offrir ? "
                f"Crée un dialogue réaliste avec le marchand {merchant_name}. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        elif action == "haggle":
            prompt = (
                f"C'est un peu cher. Pouvez-vous faire un meilleur prix pour {item_name} ? "
                f"Crée un dialogue réaliste de marchandage avec {merchant_name}. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        else:
            prompt = (
                f"Je m'intéresse à {item_name}. "
                f"Crée un dialogue réaliste avec le marchand {merchant_name}. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        
        # Générer et retourner l'interaction
        return self.generate_response(prompt, market_context)
    
    def generate_intimate_scene(self, partner_id: str, intensity: str, location_id: str, additional_context: Dict = None) -> Dict:
        """
        Génère une scène intime adaptée aux préférences
        
        Args:
            partner_id: ID du partenaire
            intensity: Niveau d'intensité (mild, moderate, explicit)
            location_id: ID du lieu
            additional_context: Contexte supplémentaire
            
        Returns:
            Scène intime générée
        """
        # Vérifier si le contenu mature est activé dans le contexte
        mature_enabled = additional_context.get("mature_content_enabled", False) if additional_context else False
        
        # Si le contenu mature n'est pas activé, générer une version atténuée
        if not mature_enabled and intensity != "mild":
            intensity = "mild"
        
        # Récupérer les données du partenaire et du lieu
        partner_data = self.character_data.get(partner_id, {})
        partner_name = partner_data.get("name", "partenaire")
        
        location_data = self.location_data.get(location_id, {})
        location_name = location_data.get("name", "lieu")
        
        # Contexte pour la génération
        intimate_context = {
            "interaction_type": "intimate",
            "partner_id": partner_id,
            "partner_name": partner_name,
            "partner_data": partner_data,
            "location_id": location_id,
            "location_name": location_name,
            "intensity": intensity,
            "mature_content_enabled": mature_enabled
        }
        
        # Ajouter le contexte supplémentaire s'il existe
        if additional_context:
            intimate_context.update(additional_context)
        
        # Prompt selon l'intensité
        if intensity == "mild":
            prompt = (
                f"Un moment romantique et tendre se développe entre moi et {partner_name} à {location_name}. "
                f"Décris cette scène avec délicatesse et émotion. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        elif intensity == "moderate":
            prompt = (
                f"Une scène d'intimité modérée se développe entre moi et {partner_name} à {location_name}. "
                f"Décris cette scène avec sensibilité et suggestion. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        else:
            prompt = (
                f"Une scène d'intimité explicite se développe entre moi et {partner_name} à {location_name}. "
                f"Décris cette scène avec intensité tout en restant élégant. "
                f"Fais très attention à l'orthographe et à la grammaire française."
            )
        
        # Générer la scène
        result = self.generate_response(prompt, intimate_context)
        
        # Ajouter des métadonnées à la réponse
        if isinstance(result, str):
            return {
                "text": result,
                "intensity": intensity,
                "partner_name": partner_name,
                "location_name": location_name
            }
        else:
            return result
    
    def analyze_intent(self, user_input: str) -> Dict:
        """
        Analyse l'intention de l'utilisateur dans son entrée
        
        Args:
            user_input: Entrée utilisateur
            
        Returns:
            Dictionnaire avec l'intention détectée
        """
        # Liste de mots-clés pour différentes intentions
        intent_keywords = {
            "combat": ["attaquer", "combattre", "frapper", "tuer", "éliminer", "vaincre"],
            "dialogue": ["parler", "discuter", "questionner", "demander", "interroger"],
            "movement": ["aller", "marcher", "courir", "voyager", "entrer", "sortir"],
            "examine": ["examiner", "regarder", "observer", "inspecter", "étudier"],
            "inventory": ["inventaire", "sac", "équiper", "utiliser", "prendre", "ramasser"],
            "market": ["acheter", "vendre", "marchander", "négocier", "prix"],
            "intimate": ["embrasser", "caresser", "séduire", "flirter", "intimer"]
        }
        
        # Convertir l'entrée en minuscules
        input_lower = user_input.lower()
        
        # Rechercher les mots-clés dans l'entrée
        detected_intents = {}
        for intent, keywords in intent_keywords.items():
            for keyword in keywords:
                if keyword in input_lower:
                    if intent in detected_intents:
                        detected_intents[intent] += 1
                    else:
                        detected_intents[intent] = 1
        
        # Si des intentions sont détectées, retourner la plus probable
        if detected_intents:
            primary_intent = max(detected_intents, key=detected_intents.get)
            
            # Analyser les paramètres selon l'intention
            params = self._extract_intent_parameters(user_input, primary_intent)
            
            return {
                "type": primary_intent,
                "confidence": detected_intents[primary_intent] / len(input_lower.split()),
                "params": params
            }
        
        # Si aucune intention claire n'est détectée, considérer comme dialogue général
        return {"type": "dialogue", "confidence": 0.3, "params": {}}
    
    def _extract_intent_parameters(self, user_input: str, intent_type: str) -> Dict:
        """
        Extrait les paramètres spécifiques à une intention
        
        Args:
            user_input: Entrée utilisateur
            intent_type: Type d'intention
            
        Returns:
            Paramètres extraits
        """
        params = {}
        
        if intent_type == "combat":
            # Chercher la cible du combat
            target_match = re.search(r'(?:attaquer|combattre|frapper|tuer|éliminer|vaincre)\s+(?:le\s+|la\s+|l[\']\s*)?([a-zéèêàâùûôç\s]+)', user_input.lower())
            if target_match:
                params["target"] = target_match.group(1).strip()
                
            # Chercher l'arme ou la méthode
            weapon_match = re.search(r'avec\s+(?:mon|ma|mes)?\s*([a-zéèêàâùûôç\s]+)', user_input.lower())
            if weapon_match:
                params["weapon"] = weapon_match.group(1).strip()
            
            # Chercher une compétence spécifique
            skill_match = re.search(r'(?:utiliser|lancer)\s+([a-zéèêàâùûôç\s]+)', user_input.lower())
            if skill_match:
                params["skill"] = skill_match.group(1).strip()
        
        elif intent_type == "dialogue":
            # Chercher l'interlocuteur
            target_match = re.search(r'(?:parler|discuter|questionner|demander|interroger)\s+(?:à|au|aux|avec)?\s+(?:le\s+|la\s+|l[\']\s*)?([a-zéèêàâùûôç\s]+)', user_input.lower())
            if target_match:
                params["target"] = target_match.group(1).strip()
                
            # Chercher le sujet de conversation
            topic_match = re.search(r'(?:à propos|sur|concernant|de)\s+([a-zéèêàâùûôç\s]+)', user_input.lower())
            if topic_match:
                params["topic"] = topic_match.group(1).strip()
        
        elif intent_type == "movement":
            # Chercher la destination
            destination_match = re.search(r'(?:aller|marcher|courir|voyager|entrer|sortir)\s+(?:à|au|aux|vers|dans|par)?\s+(?:le\s+|la\s+|l[\']\s*)?([a-zéèêàâùûôç\s]+)', user_input.lower())
            if destination_match:
                params["destination"] = destination_match.group(1).strip()
        
        # Autres types d'intentions peuvent avoir leurs propres paramètres à extraire
        
        return params
    
    def generate_quest_dialogue(self, quest_id: str, npc_id: str, stage: str, player_data: Dict) -> str:
        """
        Génère un dialogue lié à une quête
        
        Args:
            quest_id: ID de la quête
            npc_id: ID du PNJ
            stage: Étape de la quête (start, progress, complete)
            player_data: Données du joueur
            
        Returns:
            Dialogue généré pour la quête
        """
        from_cache = self._check_quest_dialogue_cache(quest_id, npc_id, stage)
        if from_cache:
            return from_cache
        
        # Contexte de quête pour le dialogue
        quest_context = {
            "interaction_type": "dialogue",
            "dialogue_type": "quest",
            "character_id": npc_id,
            "quest_id": quest_id,
            "quest_stage": stage,
            "player_data": player_data
        }
        
        # Prompt différent selon l'étape de la quête
        if stage == "start":
            prompt = (
                "Je suis prêt à accepter votre quête. Que dois-je faire ? "
                "Crée un dialogue immersif d'attribution de quête. "
                "Fais très attention à l'orthographe et à la grammaire française."
            )
        elif stage == "progress":
            prompt = (
                "Je suis en train de travailler sur votre quête. Des conseils supplémentaires ? "
                "Crée un dialogue immersif de progression de quête. "
                "Fais très attention à l'orthographe et à la grammaire française."
            )
        elif stage == "complete":
            prompt = (
                "J'ai terminé ce que vous m'avez demandé de faire. "
                "Crée un dialogue immersif de fin de quête avec félicitations. "
                "Fais très attention à l'orthographe et à la grammaire française."
            )
        else:
            prompt = (
                "Parlons de la quête que vous m'avez confiée. "
                "Crée un dialogue immersif à propos de cette quête. "
                "Fais très attention à l'orthographe et à la grammaire française."
            )
        
        # Générer le dialogue
        response = self.generate_response(prompt, quest_context)
        
        # Mettre en cache pour réutilisation
        self._cache_quest_dialogue(quest_id, npc_id, stage, response)
        
        return response
    
    def _check_quest_dialogue_cache(self, quest_id: str, npc_id: str, stage: str) -> Optional[str]:
        """Vérifie si un dialogue de quête est en cache"""
        # Cette méthode pourrait être étendue pour utiliser un cache persistant
        cache_key = f"quest_{quest_id}_{npc_id}_{stage}"
        return self.description_cache.get(cache_key)
    
    def _cache_quest_dialogue(self, quest_id: str, npc_id: str, stage: str, dialogue: str) -> None:
        """Met en cache un dialogue de quête"""
        cache_key = f"quest_{quest_id}_{npc_id}_{stage}"
        self.description_cache[cache_key] = dialogue
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à LM Studio avec un message simple
        
        Returns:
            True si la connexion est réussie, False sinon
        """
        try:
            print("Test de la connexion à LM Studio...")
            
            # Format compatible avec LM Studio 0.3.16
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": "Tu es l'IA narrative du jeu de rôle MUSKO TENSEI RP. Dis bonjour en tant que narrateur d'un jeu de rôle médiéval fantastique."}
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }
            
            # Envoyer la requête
            url = f"{self.lm_studio_api_url}/chat/completions"
            print(f"Envoi de la requête à LM Studio: {url}")
            
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    if "message" in result["choices"][0]:
                        generated_text = result["choices"][0]["message"]["content"]
                    else:
                        generated_text = result["choices"][0].get("text", "")
                    
                    print(f"Test de connexion LM Studio: {generated_text}")
                    print("✅ Connexion à LM Studio réussie!")
                    return True
                else:
                    print("❌ Format de réponse inattendu")
                    print(f"Réponse reçue: {result}")
                    return False
            else:
                print(f"❌ Échec de la connexion à LM Studio: {response.status_code} {response.reason}")
                print(f"Détail de l'erreur: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors du test de connexion à LM Studio: {e}")
            return False