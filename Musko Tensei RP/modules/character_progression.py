# character_progression.py
import json
import os
import random
import math
from typing import Dict, List, Any, Tuple, Optional

class CharacterProgression:
    def __init__(self, game_instance=None):
        """
        Initialise le système de progression des personnages
        
        Args:
            game_instance: Instance du jeu principal (MuskoTenseiRP)
        """
        self.game = game_instance
        
        # Charger les données de progression
        self.progression_data = self._load_data("progression")
        self.skills_data = self._load_data("skills")
        
        # Constantes de progression
        self.xp_curve = self.progression_data.get("xp_curve", {})
        self.attribute_costs = self.progression_data.get("attribute_costs", {})
        self.skill_categories = self.progression_data.get("skill_categories", {})
        
        # Cache pour les calculs fréquents
        self.level_requirements_cache = {}
        self.skill_unlock_cache = {}
        
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
    
    def calculate_xp_for_level(self, level: int) -> int:
        """
        Calcule l'XP nécessaire pour atteindre un niveau
        
        Args:
            level: Niveau cible
            
        Returns:
            XP totale nécessaire pour ce niveau
        """
        if level in self.level_requirements_cache:
            return self.level_requirements_cache[level]
            
        base_xp = self.xp_curve.get("base_xp", 100)
        scaling = self.xp_curve.get("scaling", 1.5)
        exponent = self.xp_curve.get("exponent", 1.8)
        
        xp_required = base_xp * (level ** exponent) * scaling
        
        # Mise en cache
        self.level_requirements_cache[level] = int(xp_required)
        
        return int(xp_required)
    
    def get_next_level_xp(self, current_level: int) -> Tuple[int, int]:
        """
        Obtient l'XP nécessaire pour le niveau actuel et le niveau suivant
        
        Args:
            current_level: Niveau actuel du joueur
            
        Returns:
            Tuple (XP pour niveau actuel, XP pour niveau suivant)
        """
        current_xp = self.calculate_xp_for_level(current_level)
        next_xp = self.calculate_xp_for_level(current_level + 1)
        
        return current_xp, next_xp
    
    def award_xp(self, xp_amount: int) -> Dict[str, Any]:
        """
        Attribue de l'XP au joueur et vérifie les montées de niveau
        
        Args:
            xp_amount: Quantité d'XP à attribuer
            
        Returns:
            Dictionnaire contenant les résultats (niveaux gagnés, etc.)
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"success": False, "message": "No player data available"}
        
        player = self.game.player
        current_level = player.get("level", 1)
        current_xp = player.get("xp", 0)
        
        # Ajouter l'XP
        new_xp = current_xp + xp_amount
        player["xp"] = new_xp
        
        # Vérifier si le joueur monte de niveau
        levels_gained = 0
        attribute_points_gained = 0
        skill_points_gained = 0
        new_level = current_level
        
        # Continuer à monter de niveau tant que l'XP est suffisante
        next_level_xp = self.calculate_xp_for_level(new_level + 1)
        
        while new_xp >= next_level_xp:
            new_level += 1
            levels_gained += 1
            
            # Attribuer des points
            attribute_pts = self.progression_data.get("attribute_points_per_level", 3)
            skill_pts = self.progression_data.get("skill_points_per_level", 2)
            
            attribute_points_gained += attribute_pts
            skill_points_gained += skill_pts
            
            # Vérifier le niveau suivant
            next_level_xp = self.calculate_xp_for_level(new_level + 1)
        
        # Mettre à jour le joueur si des niveaux ont été gagnés
        if levels_gained > 0:
            player["level"] = new_level
            player["attribute_points"] = player.get("attribute_points", 0) + attribute_points_gained
            player["skill_points"] = player.get("skill_points", 0) + skill_points_gained
            
            # Débloquer de nouvelles compétences selon le niveau
            new_skills = self.check_skill_unlocks(new_level)
            
            # Mettre à jour les stats de base
            self.update_base_stats(player)
            
            return {
                "success": True,
                "levels_gained": levels_gained,
                "new_level": new_level,
                "attribute_points_gained": attribute_points_gained,
                "skill_points_gained": skill_points_gained,
                "new_skills_available": new_skills
            }
        
        return {
            "success": True,
            "levels_gained": 0,
            "message": f"Gained {xp_amount} XP. Progress: {new_xp - next_level_xp + self.calculate_xp_for_level(new_level)}/{next_level_xp} to next level."
        }
    
    def check_skill_unlocks(self, level: int) -> List[Dict[str, Any]]:
        """
        Vérifie quelles compétences sont débloquées à un niveau donné
        
        Args:
            level: Niveau du joueur
            
        Returns:
            Liste des compétences nouvellement disponibles
        """
        # Vérifier si nous avons déjà calculé les compétences pour ce niveau
        if level in self.skill_unlock_cache:
            return self.skill_unlock_cache[level]
            
        unlocked_skills = []
        
        # Parcourir toutes les compétences
        for skill_id, skill_data in self.skills_data.get("skills", {}).items():
            requirements = skill_data.get("requirements", {})
            
            # Vérifier si la compétence nécessite ce niveau exact
            if requirements.get("level", 0) == level:
                unlocked_skills.append({
                    "id": skill_id,
                    "name": skill_data.get("name", "Unknown Skill"),
                    "description": skill_data.get("description", ""),
                    "category": skill_data.get("category", "general")
                })
        
        # Mettre en cache les résultats
        self.skill_unlock_cache[level] = unlocked_skills
        
        return unlocked_skills
    
    def update_base_stats(self, player: Dict[str, Any]) -> None:
        """
        Met à jour les statistiques de base du joueur en fonction de son niveau et de sa classe
        
        Args:
            player: Données du joueur à mettre à jour
        """
        level = player.get("level", 1)
        player_class = player.get("class", "fighter")
        base_stats = self.progression_data.get("base_stats", {}).get(player_class, {})
        
        # Si aucune statistique de base n'est définie pour cette classe, utiliser les valeurs par défaut
        if not base_stats:
            base_stats = self.progression_data.get("default_base_stats", {})
        
        # Calculer les nouvelles statistiques
        for stat, base_value in base_stats.items():
            growth_rate = base_stats.get(f"{stat}_growth", 0.1)
            new_value = base_value + (growth_rate * (level - 1) * base_value)
            
            # Arrondir et mettre à jour
            player[f"base_{stat}"] = int(new_value)
            
            # Mettre à jour les statistiques actuelles si nécessaires (comme HP, MP)
            if stat in ["hp", "mp"]:
                max_stat = f"max_{stat}"
                current_stat = stat
                
                player[max_stat] = int(new_value)
                
                # Si c'est une montée de niveau, restaurer complètement les stats
                if player.get(current_stat, 0) < player[max_stat]:
                    player[current_stat] = player[max_stat]
    
    def spend_attribute_points(self, attribute: str, points: int) -> Dict[str, Any]:
        """
        Dépense des points d'attribut pour améliorer une caractéristique
        
        Args:
            attribute: Attribut à améliorer
            points: Nombre de points à dépenser
            
        Returns:
            Résultat de l'opération
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"success": False, "message": "No player data available"}
            
        player = self.game.player
        available_points = player.get("attribute_points", 0)
        
        # Vérifier si l'attribut est valide
        valid_attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma", "perception"]
        if attribute not in valid_attributes:
            return {"success": False, "message": f"Invalid attribute: {attribute}"}
            
        # Vérifier si le joueur a assez de points
        if available_points < points:
            return {"success": False, "message": f"Not enough attribute points. Have {available_points}, need {points}."}
            
        # Dépenser les points et améliorer l'attribut
        player["attribute_points"] = available_points - points
        
        # Intialiser l'attribut s'il n'existe pas
        if "attributes" not in player:
            player["attributes"] = {}
        if attribute not in player["attributes"]:
            player["attributes"][attribute] = 10  # Valeur par défaut
            
        # Appliquer l'amélioration
        player["attributes"][attribute] += points
        
        # Mettre à jour les statistiques dérivées
        self.update_derived_stats(player)
        
        return {
            "success": True,
            "message": f"Spent {points} points on {attribute}. New value: {player['attributes'][attribute]}",
            "new_value": player["attributes"][attribute],
            "remaining_points": player["attribute_points"]
        }
    
    def update_derived_stats(self, player: Dict[str, Any]) -> None:
        """
        Met à jour les statistiques dérivées des attributs
        
        Args:
            player: Données du joueur à mettre à jour
        """
        # S'assurer que les attributs existent
        if "attributes" not in player:
            return
            
        attributes = player["attributes"]
        
        # Calculer les modificateurs selon les formules du jeu
        # Exemple pour un système basé sur D&D:
        # modificateur = (attribut - 10) // 2
        
        # HP max (Constitution)
        constitution = attributes.get("constitution", 10)
        base_hp = player.get("base_hp", 100)
        hp_per_con = self.progression_data.get("hp_per_constitution", 10)
        
        player["max_hp"] = base_hp + ((constitution - 10) * hp_per_con)
        
        # MP max (Intelligence/Wisdom)
        intelligence = attributes.get("intelligence", 10)
        wisdom = attributes.get("wisdom", 10)
        base_mp = player.get("base_mp", 50)
        mp_per_int = self.progression_data.get("mp_per_intelligence", 5)
        mp_per_wis = self.progression_data.get("mp_per_wisdom", 3)
        
        player["max_mp"] = base_mp + ((intelligence - 10) * mp_per_int) + ((wisdom - 10) * mp_per_wis)
        
        # Force d'attaque (Force/Dextérité selon l'arme)
        strength = attributes.get("strength", 10)
        dexterity = attributes.get("dexterity", 10)
        
        player["physical_attack"] = 10 + (strength - 10) * 2
        player["ranged_attack"] = 10 + (dexterity - 10) * 2
        
        # Défense (Constitution/Dextérité)
        player["physical_defense"] = 10 + ((constitution - 10) + (dexterity - 10)) // 2
        
        # Magic (Intelligence/Wisdom)
        player["magic_attack"] = 10 + (intelligence - 10) * 2
        player["magic_defense"] = 10 + (wisdom - 10) * 2
        
        # Initiative (Dextérité/Perception)
        perception = attributes.get("perception", 10)
        player["initiative"] = 10 + ((dexterity - 10) + (perception - 10)) // 2
        
        # Autres statistiques dérivées
        player["carry_capacity"] = 50 + (strength - 10) * 10
        player["critical_chance"] = 5 + (dexterity - 10) // 2
        player["persuasion"] = 10 + (charisma - 10) * 2 if (charisma := attributes.get("charisma", 10)) else 10
    
    def learn_skill(self, skill_id: str) -> Dict[str, Any]:
        """
        Apprend une nouvelle compétence au joueur
        
        Args:
            skill_id: ID de la compétence à apprendre
            
        Returns:
            Résultat de l'opération
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"success": False, "message": "No player data available"}
            
        player = self.game.player
        available_points = player.get("skill_points", 0)
        
        # Vérifier si la compétence existe
        skill_data = self.skills_data.get("skills", {}).get(skill_id)
        if not skill_data:
            return {"success": False, "message": f"Skill {skill_id} does not exist"}
            
        # Vérifier si le joueur a déjà cette compétence
        if "learned_skills" not in player:
            player["learned_skills"] = {}
            
        if skill_id in player["learned_skills"]:
            return {"success": False, "message": f"Skill {skill_data.get('name', skill_id)} already learned"}
            
        # Vérifier les prérequis
        requirements = skill_data.get("requirements", {})
        
        # Niveau requis
        if player.get("level", 1) < requirements.get("level", 0):
            return {"success": False, "message": f"Level {requirements.get('level')} required for this skill"}
            
        # Attributs requis
        for attr, value in requirements.get("attributes", {}).items():
            if player.get("attributes", {}).get(attr, 0) < value:
                return {"success": False, "message": f"{attr.capitalize()} {value} required for this skill"}
                
        # Compétences prérequises
        for req_skill in requirements.get("prerequisite_skills", []):
            if req_skill not in player.get("learned_skills", {}):
                req_skill_name = self.skills_data.get("skills", {}).get(req_skill, {}).get("name", req_skill)
                return {"success": False, "message": f"Prerequisite skill {req_skill_name} required"}
                
        # Vérifier le coût en points
        skill_cost = skill_data.get("cost", 1)
        if available_points < skill_cost:
            return {"success": False, "message": f"Not enough skill points. Have {available_points}, need {skill_cost}"}
            
        # Apprendre la compétence
        player["skill_points"] = available_points - skill_cost
        
        # Initialiser la compétence avec son niveau de base
        player["learned_skills"][skill_id] = {
            "level": 1,
            "experience": 0,
            "mastery": 0.0
        }
        
        # Si c'est une compétence passive, appliquer ses effets
        if skill_data.get("type") == "passive":
            self._apply_passive_skill_effects(player, skill_id, skill_data)
        
        return {
            "success": True,
            "message": f"Learned skill: {skill_data.get('name', skill_id)}",
            "skill_name": skill_data.get('name', skill_id),
            "skill_description": skill_data.get('description', ''),
            "remaining_points": player["skill_points"]
        }
    
    def _apply_passive_skill_effects(self, player: Dict[str, Any], skill_id: str, skill_data: Dict[str, Any]) -> None:
        """
        Applique les effets des compétences passives
        
        Args:
            player: Données du joueur
            skill_id: ID de la compétence
            skill_data: Données de la compétence
        """
        effects = skill_data.get("effects", {})
        
        # Appliquer des bonus aux attributs
        for attr, bonus in effects.get("attribute_bonuses", {}).items():
            if "attributes" not in player:
                player["attributes"] = {}
            if attr not in player["attributes"]:
                player["attributes"][attr] = 10
                
            player["attributes"][attr] += bonus
            
        # Appliquer des bonus aux statistiques
        for stat, bonus in effects.get("stat_bonuses", {}).items():
            if stat not in player:
                player[stat] = 0
                
            player[stat] += bonus
            
        # Mettre à jour les statistiques dérivées
        self.update_derived_stats(player)
    
    def improve_skill(self, skill_id: str, xp_amount: int) -> Dict[str, Any]:
        """
        Améliore une compétence existante en lui attribuant de l'XP
        
        Args:
            skill_id: ID de la compétence à améliorer
            xp_amount: Quantité d'XP à attribuer
            
        Returns:
            Résultat de l'opération
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"success": False, "message": "No player data available"}
            
        player = self.game.player
        
        # Vérifier si le joueur possède cette compétence
        if "learned_skills" not in player or skill_id not in player["learned_skills"]:
            return {"success": False, "message": f"Skill {skill_id} not learned yet"}
            
        skill = player["learned_skills"][skill_id]
        current_level = skill.get("level", 1)
        current_xp = skill.get("experience", 0)
        
        # Ajouter l'XP
        new_xp = current_xp + xp_amount
        skill["experience"] = new_xp
        
        # Calculer l'XP nécessaire pour le niveau suivant
        xp_for_next = self._calculate_skill_xp_for_level(current_level + 1)
        
        # Vérifier si la compétence monte de niveau
        if new_xp >= xp_for_next:
            new_level = current_level + 1
            skill["level"] = new_level
            
            # Mettre à jour la maîtrise
            skill["mastery"] = min(1.0, skill.get("mastery", 0) + 0.1)
            
            # Obtenir les données de la compétence
            skill_data = self.skills_data.get("skills", {}).get(skill_id, {})
            
            # Si c'est une compétence passive, mettre à jour ses effets
            if skill_data.get("type") == "passive":
                self._apply_passive_skill_effects(player, skill_id, skill_data)
            
            return {
                "success": True,
                "level_up": True,
                "new_level": new_level,
                "message": f"Skill {skill_data.get('name', skill_id)} improved to level {new_level}!",
                "next_level_xp": self._calculate_skill_xp_for_level(new_level + 1)
            }
        
        return {
            "success": True,
            "level_up": False,
            "message": f"Gained {xp_amount} XP for skill. Progress: {new_xp}/{xp_for_next}",
            "progress": new_xp / xp_for_next
        }
    
    def _calculate_skill_xp_for_level(self, level: int) -> int:
        """
        Calcule l'XP nécessaire pour atteindre un niveau de compétence
        
        Args:
            level: Niveau cible
            
        Returns:
            XP requise
        """
        base_skill_xp = self.progression_data.get("base_skill_xp", 50)
        skill_scaling = self.progression_data.get("skill_scaling", 1.2)
        
        return int(base_skill_xp * (level ** skill_scaling))
    
    def get_available_skills(self, player_level: int = None, attributes: Dict[str, int] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtient la liste des compétences disponibles pour le joueur
        
        Args:
            player_level: Niveau du joueur (si None, utilise le niveau actuel)
            attributes: Attributs du joueur (si None, utilise les attributs actuels)
            
        Returns:
            Dictionnaire des compétences disponibles, groupées par catégorie
        """
        if not self.game or not hasattr(self.game, "player"):
            return {}
            
        player = self.game.player
        
        # Utiliser les données fournies ou les données du joueur
        current_level = player_level if player_level is not None else player.get("level", 1)
        current_attributes = attributes if attributes is not None else player.get("attributes", {})
        learned_skills = player.get("learned_skills", {})
        
        available_skills = {}
        
        # Parcourir toutes les compétences
        for skill_id, skill_data in self.skills_data.get("skills", {}).items():
            # Ignorer les compétences déjà apprises
            if skill_id in learned_skills:
                continue
                
            # Vérifier les prérequis
            requirements = skill_data.get("requirements", {})
            
            # Niveau requis
            if current_level < requirements.get("level", 0):
                continue
                
            # Attributs requis
            meets_attr_requirements = True
            for attr, value in requirements.get("attributes", {}).items():
                if current_attributes.get(attr, 0) < value:
                    meets_attr_requirements = False
                    break
                    
            if not meets_attr_requirements:
                continue
                
            # Compétences prérequises
            meets_skill_requirements = True
            for req_skill in requirements.get("prerequisite_skills", []):
                if req_skill not in learned_skills:
                    meets_skill_requirements = False
                    break
                    
            if not meets_skill_requirements:
                continue
                
            # La compétence est disponible, l'ajouter à la catégorie appropriée
            category = skill_data.get("category", "general")
            
            if category not in available_skills:
                available_skills[category] = []
                
            available_skills[category].append({
                "id": skill_id,
                "name": skill_data.get("name", "Unknown Skill"),
                "description": skill_data.get("description", ""),
                "type": skill_data.get("type", "active"),
                "cost": skill_data.get("cost", 1),
                "effects": skill_data.get("effects", {})
            })
        
        return available_skills
    
    def calculate_spell_damage(self, spell_id: str) -> Dict[str, Any]:
        """
        Calcule les dégâts d'un sort en tenant compte des attributs et compétences du joueur
        
        Args:
            spell_id: ID du sort à calculer
            
        Returns:
            Informations sur les dégâts du sort
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"damage": 0, "error": "No player data available"}
            
        player = self.game.player
        
        # Obtenir les données du sort
        spell_data = self.skills_data.get("skills", {}).get(spell_id, {})
        if not spell_data or spell_data.get("type") != "spell":
            return {"damage": 0, "error": f"Invalid spell ID: {spell_id}"}
            
        # Vérifier si le joueur connaît ce sort
        if spell_id not in player.get("learned_skills", {}):
            return {"damage": 0, "error": f"Spell {spell_data.get('name', spell_id)} not learned"}
            
        # Récupérer le niveau de maîtrise du sort
        skill_level = player["learned_skills"][spell_id].get("level", 1)
        mastery = player["learned_skills"][spell_id].get("mastery", 0.0)
        
        # Calculer les dégâts de base
        base_damage = spell_data.get("base_damage", 10)
        scaling = spell_data.get("scaling", {})
        
        # Ajouter les bonus d'attributs
        attribute_bonus = 0
        for attr, scale in scaling.items():
            attribute_value = player.get("attributes", {}).get(attr, 10)
            attribute_bonus += (attribute_value - 10) * scale
            
        # Calculer les dégâts finaux
        level_multiplier = 1 + (0.1 * (skill_level - 1))
        mastery_bonus = 1 + mastery
        
        final_damage = (base_damage + attribute_bonus) * level_multiplier * mastery_bonus
        
        # Arrondir
        final_damage = int(final_damage)
        
        return {
            "damage": final_damage,
            "base_damage": base_damage,
            "attribute_bonus": attribute_bonus,
            "level_multiplier": level_multiplier,
            "mastery_bonus": mastery_bonus,
            "skill_level": skill_level,
            "spell_name": spell_data.get("name", spell_id),
            "element": spell_data.get("element", "neutral"),
            "mp_cost": spell_data.get("mp_cost", 10)
        }
    
    def calculate_attack_damage(self, weapon_id: str = None) -> Dict[str, Any]:
        """
        Calcule les dégâts d'une attaque physique
        
        Args:
            weapon_id: ID de l'arme utilisée (None pour attaque à mains nues)
            
        Returns:
            Informations sur les dégâts de l'attaque
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"damage": 0, "error": "No player data available"}
            
        player = self.game.player
        
        # Attributs du joueur
        strength = player.get("attributes", {}).get("strength", 10)
        dexterity = player.get("attributes", {}).get("dexterity", 10)
        
        # Dégâts de base (mains nues)
        base_damage = 5
        stat_modifier = strength - 10
        
        # Si une arme est spécifiée
        if weapon_id:
            # Obtenir les données de l'arme
            weapon_data = self.game.item_data.get("items", {}).get(weapon_id, {})
            if not weapon_data or weapon_data.get("type") != "weapon":
                return {"damage": base_damage, "error": f"Invalid weapon ID: {weapon_id}"}
                
            # Utiliser les dégâts de l'arme
            base_damage = weapon_data.get("damage", 5)
            
            # Déterminer l'attribut à utiliser selon le type d'arme
            weapon_type = weapon_data.get("weapon_type", "melee")
            if weapon_type in ["bow", "crossbow", "thrown"]:
                stat_modifier = dexterity - 10
        
        # Calculer les dégâts finaux
        final_damage = base_damage + (stat_modifier * 2)
        
        # Bonus de compétences
        weapon_skill = None
        if weapon_id:
            weapon_data = self.game.item_data.get("items", {}).get(weapon_id, {})
            weapon_type = weapon_data.get("weapon_type", "melee")
            
            # Trouver la compétence correspondant au type d'arme
            for skill_id, skill_data in player.get("learned_skills", {}).items():
                skill_info = self.skills_data.get("skills", {}).get(skill_id, {})
                if skill_info.get("weapon_type") == weapon_type:
                    weapon_skill = skill_id
                    break
        
        skill_bonus = 0
        if weapon_skill:
            skill_level = player["learned_skills"][weapon_skill].get("level", 1)
            mastery = player["learned_skills"][weapon_skill].get("mastery", 0.0)
            
            skill_bonus = (skill_level - 1) * 2 + (mastery * 10)
            final_damage += skill_bonus
        
        # Arrondir
        final_damage = max(1, int(final_damage))
        
        return {
            "damage": final_damage,
            "base_damage": base_damage,
            "stat_modifier": stat_modifier * 2,
            "skill_bonus": skill_bonus,
            "critical_chance": player.get("critical_chance", 5),
            "weapon_name": self.game.item_data.get("items", {}).get(weapon_id, {}).get("name", "Unarmed")
        }
    
    def get_class_specializations(self, player_class: str) -> List[Dict[str, Any]]:
        """
        Obtient les spécialisations disponibles pour une classe
        
        Args:
            player_class: Classe du joueur
            
        Returns:
            Liste des spécialisations disponibles
        """
        specializations = []
        
        class_data = self.progression_data.get("classes", {}).get(player_class, {})
        for spec_id, spec_data in class_data.get("specializations", {}).items():
            specializations.append({
                "id": spec_id,
                "name": spec_data.get("name", "Unknown Specialization"),
                "description": spec_data.get("description", ""),
                "requirement_level": spec_data.get("requirement_level", 10),
                "bonus_attributes": spec_data.get("bonus_attributes", {}),
                "bonus_skills": spec_data.get("bonus_skills", [])
            })
            
        return specializations
    
    def choose_specialization(self, specialization_id: str) -> Dict[str, Any]:
        """
        Choisit une spécialisation pour le joueur
        
        Args:
            specialization_id: ID de la spécialisation choisie
            
        Returns:
            Résultat de l'opération
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"success": False, "message": "No player data available"}
            
        player = self.game.player
        player_class = player.get("class", "fighter")
        player_level = player.get("level", 1)
        
        # Vérifier si le joueur a déjà une spécialisation
        if "specialization" in player:
            return {"success": False, "message": "Player already has a specialization"}
            
        # Obtenir les données de la spécialisation
        class_data = self.progression_data.get("classes", {}).get(player_class, {})
        specializations = class_data.get("specializations", {})
        
        if specialization_id not in specializations:
            return {"success": False, "message": f"Invalid specialization ID for class {player_class}"}
            
        spec_data = specializations[specialization_id]
        
        # Vérifier le niveau requis
        req_level = spec_data.get("requirement_level", 10)
        if player_level < req_level:
            return {"success": False, "message": f"Level {req_level} required for this specialization"}
            
        # Appliquer la spécialisation
        player["specialization"] = specialization_id
        
        # Appliquer les bonus d'attributs
        for attr, bonus in spec_data.get("bonus_attributes", {}).items():
            if "attributes" not in player:
                player["attributes"] = {}
            if attr not in player["attributes"]:
                player["attributes"][attr] = 10
                
            player["attributes"][attr] += bonus
            
        # Donner les compétences bonus
        for skill_id in spec_data.get("bonus_skills", []):
            if skill_id not in self.skills_data.get("skills", {}):
                continue
                
            if "learned_skills" not in player:
                player["learned_skills"] = {}
                
            # Donner la compétence gratuitement si le joueur ne l'a pas déjà
            if skill_id not in player["learned_skills"]:
                player["learned_skills"][skill_id] = {
                    "level": 1,
                    "experience": 0,
                    "mastery": 0.0
                }
                
        # Mettre à jour les statistiques dérivées
        self.update_derived_stats(player)
        
        return {
            "success": True,
            "message": f"Specialization chosen: {spec_data.get('name', specialization_id)}",
            "specialization_name": spec_data.get('name', specialization_id),
            "specialization_description": spec_data.get('description', ''),
            "bonus_attributes": spec_data.get('bonus_attributes', {}),
            "bonus_skills": [
                self.skills_data.get("skills", {}).get(skill_id, {}).get("name", skill_id)
                for skill_id in spec_data.get("bonus_skills", [])
            ]
        }
    
    def reset_skills(self) -> Dict[str, Any]:
        """
        Réinitialise les compétences du joueur et rembourse les points de compétence
        
        Returns:
            Résultat de l'opération
        """
        if not self.game or not hasattr(self.game, "player"):
            return {"success": False, "message": "No player data available"}
            
        player = self.game.player
        
        # Calculer les points de compétence à rembourser
        total_points = 0
        for skill_id, skill_data in player.get("learned_skills", {}).items():
            # Obtenir le coût de la compétence
            skill_info = self.skills_data.get("skills", {}).get(skill_id, {})
            total_points += skill_info.get("cost", 1)
            
        # Réinitialiser les compétences
        player["learned_skills"] = {}
        
        # Rembourser les points
        player["skill_points"] = player.get("skill_points", 0) + total_points
        
        # Mettre à jour les statistiques dérivées (certaines peuvent être affectées par des compétences passives)
        self.update_derived_stats(player)
        
        return {
            "success": True,
            "message": f"Skills reset. Refunded {total_points} skill points.",
            "refunded_points": total_points,
            "total_skill_points": player["skill_points"]
        }