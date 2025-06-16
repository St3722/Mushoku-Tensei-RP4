# save_manager.py
import json
import os
import time
import gzip
import base64
import shutil
import pickle
import zipfile
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

class SaveManager:
    def __init__(self, game_instance=None):
        """
        Initialise le gestionnaire de sauvegarde
        
        Args:
            game_instance: Instance du jeu principal (MuskoTenseiRP)
        """
        self.game = game_instance
        self.save_directory = "saves"
        self.auto_save_directory = os.path.join(self.save_directory, "auto")
        self.quick_save_path = os.path.join(self.save_directory, "quicksave")
        self.max_auto_saves = 5
        self.max_saves_per_slot = 3  # Nombre de versions par slot
        
        # Cryptage simple (pour obfusquer légèrement les sauvegardes)
        self.encryption_key = "musko_tensei_rp"
        
        # S'assurer que les répertoires existent
        self._ensure_directories()
        
        # Métadonnées de la sauvegarde actuelle
        self.current_save_metadata = {
            "save_name": None,
            "save_slot": None,
            "last_save_time": None,
            "play_time": 0,  # En secondes
            "game_version": "1.0.0"
        }
        
        # Compteur de temps de jeu
        self.play_time_start = time.time()
    
    def _ensure_directories(self):
        """Crée les répertoires de sauvegarde s'ils n'existent pas"""
        os.makedirs(self.save_directory, exist_ok=True)
        os.makedirs(self.auto_save_directory, exist_ok=True)
    
    def _update_play_time(self):
        """Met à jour le temps de jeu total"""
        current_time = time.time()
        elapsed = current_time - self.play_time_start
        self.current_save_metadata["play_time"] += elapsed
        self.play_time_start = current_time
    
    def _reset_play_time_counter(self):
        """Réinitialise le compteur de temps pour une nouvelle session"""
        self.play_time_start = time.time()
    
    def _get_save_data(self) -> Dict[str, Any]:
        """
        Récupère toutes les données à sauvegarder
        
        Returns:
            Dictionnaire contenant toutes les données de sauvegarde
        """
        if not self.game:
            return {"error": "No game instance provided"}
        
        # Mise à jour du temps de jeu
        self._update_play_time()
        
        # Structure de base des données de sauvegarde
        save_data = {
            "metadata": self.current_save_metadata.copy(),
            "player": self.game.player.copy() if hasattr(self.game, "player") else {},
            "world_state": {
                "current_location": getattr(self.game, "current_location", ""),
                "discovered_locations": getattr(self.game, "discovered_locations", []),
                "time_of_day": getattr(self.game, "time_of_day", "day"),
                "day_count": getattr(self.game, "day_count", 1),
                "season": getattr(self.game, "season", "spring"),
                "weather": getattr(self.game, "weather", "clear")
            },
            "quests": {
                "active_quests": getattr(self.game, "active_quests", []),
                "completed_quests": getattr(self.game, "completed_quests", []),
                "failed_quests": getattr(self.game, "failed_quests", []),
                "quest_states": getattr(self.game, "quest_states", {})
            },
            "relationships": getattr(self.game, "relationships", {}),
            "inventory": getattr(self.game, "inventory", []),
            "equipment": getattr(self.game, "equipment", {}),
            "skills": getattr(self.game, "skills", {}),
            "game_flags": getattr(self.game, "game_flags", {}),
            "ai_memory": self._get_ai_memory(),
            "mature_content_settings": self._get_mature_content_settings(),
            "stats": {
                "enemies_defeated": getattr(self.game, "enemies_defeated", 0),
                "items_collected": getattr(self.game, "items_collected", 0),
                "money_earned": getattr(self.game, "money_earned", 0),
                "money_spent": getattr(self.game, "money_spent", 0),
                "skills_learned": getattr(self.game, "skills_learned", 0),
                "spells_cast": getattr(self.game, "spells_cast", 0),
                "distance_traveled": getattr(self.game, "distance_traveled", 0),
                "quests_completed": len(getattr(self.game, "completed_quests", []))
            },
            "save_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "game_version": self.current_save_metadata["game_version"]
        }
        
        # Ajouter des données spécifiques au jeu si nécessaire
        if hasattr(self.game, "get_additional_save_data"):
            additional_data = self.game.get_additional_save_data()
            save_data.update(additional_data)
        
        return save_data
    
    def _get_ai_memory(self) -> Dict[str, Any]:
        """Récupère les données de mémoire de l'IA qui doivent être sauvegardées"""
        ai_memory = {}
        
        if hasattr(self.game, "ai_manager"):
            ai_manager = self.game.ai_manager
            
            # Sauvegarder uniquement les informations essentielles de l'IA
            ai_memory = {
                "conversation_history": getattr(ai_manager, "conversation_history", [])[-20:],  # Limiter à 20 entrées
                "memory_by_character": getattr(ai_manager, "memory_by_character", {}),
                "world_state_memory": getattr(ai_manager, "world_state_memory", {}),
                "player_personality": getattr(ai_manager, "player_personality", {})
            }
        
        return ai_memory
    
    def _get_mature_content_settings(self) -> Dict[str, Any]:
        """Récupère les paramètres de contenu mature"""
        mature_settings = {}
        
        if hasattr(self.game, "mature_content_manager"):
            mcm = self.game.mature_content_manager
            mature_settings = {
                "age_verified": getattr(mcm, "age_verified", False),
                "content_enabled": getattr(mcm, "is_enabled", False),
                "maturity_level": getattr(mcm, "maturity_level", "standard"),
                "filters": getattr(mcm, "filters", {})
            }
        
        return mature_settings
    
    def _encrypt_data(self, data: bytes) -> bytes:
        """
        Chiffre légèrement les données avec un XOR simple (non cryptographiquement sûr)
        
        Args:
            data: Données à chiffrer
            
        Returns:
            Données chiffrées
        """
        key_bytes = self.encryption_key.encode('utf-8')
        key_len = len(key_bytes)
        encrypted = bytearray(len(data))
        
        for i in range(len(data)):
            encrypted[i] = data[i] ^ key_bytes[i % key_len]
            
        return bytes(encrypted)
    
    def _decrypt_data(self, data: bytes) -> bytes:
        """
        Déchiffre les données (XOR est symétrique)
        
        Args:
            data: Données chiffrées
            
        Returns:
            Données déchiffrées
        """
        # Le même algorithme XOR fonctionne pour déchiffrer
        return self._encrypt_data(data)
    
    def _compress_data(self, data_dict: Dict) -> bytes:
        """
        Compresse et chiffre les données de sauvegarde
        
        Args:
            data_dict: Données à compresser
            
        Returns:
            Données compressées et chiffrées
        """
        # Convertir en JSON
        json_data = json.dumps(data_dict)
        
        # Compresser
        compressed = gzip.compress(json_data.encode('utf-8'), compresslevel=9)
        
        # Chiffrer légèrement (obfuscation)
        encrypted = self._encrypt_data(compressed)
        
        return encrypted
    
    def _decompress_data(self, data: bytes) -> Dict:
        """
        Déchiffre et décompresse les données de sauvegarde
        
        Args:
            data: Données compressées et chiffrées
            
        Returns:
            Dictionnaire de données décompressé
        """
        try:
            # Déchiffrer
            decrypted = self._decrypt_data(data)
            
            # Décompresser
            decompressed = gzip.decompress(decrypted).decode('utf-8')
            
            # Convertir en dictionnaire
            return json.loads(decompressed)
        except Exception as e:
            print(f"Erreur lors de la décompression des données: {e}")
            return {}
    
    def _get_save_info(self, save_path: str) -> Dict[str, Any]:
        """
        Extrait les informations de base d'une sauvegarde sans la charger complètement
        
        Args:
            save_path: Chemin du fichier de sauvegarde
            
        Returns:
            Dictionnaire contenant les métadonnées de la sauvegarde
        """
        try:
            # Lire les premiers ko du fichier pour extraire uniquement les métadonnées
            with open(save_path, 'rb') as f:
                # Lire les 4 premiers octets pour vérifier la signature
                signature = f.read(4)
                if signature != b'MKRP':
                    return {"error": "Invalid save file format"}
                
                # Lire la taille des métadonnées
                meta_size_bytes = f.read(4)
                meta_size = int.from_bytes(meta_size_bytes, byteorder='little')
                
                # Lire et déchiffrer les métadonnées
                encrypted_meta = f.read(meta_size)
                decrypted_meta = self._decrypt_data(encrypted_meta)
                
                # Décompresser et charger les métadonnées
                meta_json = gzip.decompress(decrypted_meta).decode('utf-8')
                metadata = json.loads(meta_json)
                
                return {
                    "metadata": metadata,
                    "file_path": save_path,
                    "file_size": os.path.getsize(save_path),
                    "last_modified": datetime.fromtimestamp(os.path.getmtime(save_path)).strftime("%Y-%m-%d %H:%M:%S")
                }
        except Exception as e:
            return {
                "error": f"Error reading save file: {str(e)}",
                "file_path": save_path
            }
    
    def save_game(self, slot_name: str = "default", save_name: str = None) -> Dict[str, Any]:
        """
        Sauvegarde l'état actuel du jeu
        
        Args:
            slot_name: Nom du slot de sauvegarde
            save_name: Nom spécifique de la sauvegarde (si non fourni, utilise la date/heure)
            
        Returns:
            Dictionnaire indiquant le succès ou l'échec de la sauvegarde
        """
        try:
            # Définir le nom de la sauvegarde si non fourni
            if not save_name:
                save_name = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Mettre à jour les métadonnées
            self.current_save_metadata["save_name"] = save_name
            self.current_save_metadata["save_slot"] = slot_name
            self.current_save_metadata["last_save_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Récupérer les données de sauvegarde
            save_data = self._get_save_data()
            
            # Créer le répertoire du slot s'il n'existe pas
            slot_dir = os.path.join(self.save_directory, slot_name)
            os.makedirs(slot_dir, exist_ok=True)
            
            # Chemin du fichier de sauvegarde
            save_path = os.path.join(slot_dir, f"{save_name}.mkrp")
            
            # Extraire les métadonnées pour en-tête rapide
            metadata = save_data["metadata"]
            meta_json = json.dumps(metadata).encode('utf-8')
            compressed_meta = gzip.compress(meta_json, compresslevel=9)
            encrypted_meta = self._encrypt_data(compressed_meta)
            meta_size = len(encrypted_meta)
            
            # Compresser et chiffrer toutes les données
            compressed_data = self._compress_data(save_data)
            
            # Écrire le fichier avec signature et métadonnées séparées
            with open(save_path, 'wb') as f:
                # Signature du format de fichier (4 octets)
                f.write(b'MKRP')
                
                # Taille des métadonnées (4 octets)
                f.write(meta_size.to_bytes(4, byteorder='little'))
                
                # Métadonnées chiffrées
                f.write(encrypted_meta)
                
                # Données complètes chiffrées et compressées
                f.write(compressed_data)
            
            # Gérer les versions de sauvegarde (limiter le nombre par slot)
            self._manage_save_versions(slot_dir)
            
            # Réinitialiser le compteur de temps de jeu pour la prochaine session
            self._reset_play_time_counter()
            
            return {
                "success": True,
                "message": f"Jeu sauvegardé avec succès dans le slot {slot_name}",
                "save_path": save_path,
                "save_name": save_name,
                "save_time": self.current_save_metadata["last_save_time"]
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la sauvegarde: {str(e)}"
            }
    
    def quick_save(self) -> Dict[str, Any]:
        """
        Effectue une sauvegarde rapide
        
        Returns:
            Dictionnaire indiquant le succès ou l'échec de la sauvegarde rapide
        """
        return self.save_game("quicksave", "quicksave")
    
    def auto_save(self) -> Dict[str, Any]:
        """
        Effectue une sauvegarde automatique
        
        Returns:
            Dictionnaire indiquant le succès ou l'échec de la sauvegarde automatique
        """
        # Créer un nom unique pour l'auto-sauvegarde
        auto_save_name = f"autosave_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Sauvegarder dans le répertoire d'auto-sauvegarde
        result = self.save_game("auto", auto_save_name)
        
        # Gérer le nombre d'auto-sauvegardes
        self._manage_auto_saves()
        
        return result
    
    def _manage_save_versions(self, slot_dir: str) -> None:
        """
        Limite le nombre de sauvegardes par slot
        
        Args:
            slot_dir: Répertoire du slot à gérer
        """
        # Lister les fichiers du slot
        if not os.path.exists(slot_dir):
            return
            
        save_files = [f for f in os.listdir(slot_dir) if f.endswith('.mkrp')]
        
        # Si le nombre de sauvegardes dépasse la limite, supprimer les plus anciennes
        if len(save_files) > self.max_saves_per_slot:
            # Trier par date de modification
            save_files.sort(key=lambda x: os.path.getmtime(os.path.join(slot_dir, x)))
            
            # Supprimer les plus anciennes
            for i in range(len(save_files) - self.max_saves_per_slot):
                os.remove(os.path.join(slot_dir, save_files[i]))
    
    def _manage_auto_saves(self) -> None:
        """Limite le nombre d'auto-sauvegardes"""
        # Vérifier si le répertoire existe
        if not os.path.exists(self.auto_save_directory):
            return
            
        # Lister les auto-sauvegardes
        auto_saves = [f for f in os.listdir(self.auto_save_directory) if f.endswith('.mkrp')]
        
        # Si le nombre dépasse la limite, supprimer les plus anciennes
        if len(auto_saves) > self.max_auto_saves:
            # Trier par date de modification
            auto_saves.sort(key=lambda x: os.path.getmtime(os.path.join(self.auto_save_directory, x)))
            
            # Supprimer les plus anciennes
            for i in range(len(auto_saves) - self.max_auto_saves):
                os.remove(os.path.join(self.auto_save_directory, auto_saves[i]))
    
    def load_game(self, save_path: str) -> Dict[str, Any]:
        """
        Charge une sauvegarde
        
        Args:
            save_path: Chemin complet du fichier de sauvegarde
            
        Returns:
            Dictionnaire indiquant le succès ou l'échec du chargement et les données chargées
        """
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(save_path):
                return {
                    "success": False,
                    "message": f"Fichier de sauvegarde introuvable: {save_path}"
                }
            
            # Lire le fichier
            with open(save_path, 'rb') as f:
                # Vérifier la signature
                signature = f.read(4)
                if signature != b'MKRP':
                    return {
                        "success": False,
                        "message": "Format de fichier de sauvegarde invalide"
                    }
                
                # Lire la taille des métadonnées
                meta_size_bytes = f.read(4)
                meta_size = int.from_bytes(meta_size_bytes, byteorder='little')
                
                # Sauter les métadonnées, on les récupérera avec les données complètes
                f.seek(8 + meta_size)  # 4 (signature) + 4 (taille) + meta_size
                
                # Lire les données complètes
                compressed_data = f.read()
            
            # Décompresser et déchiffrer les données
            save_data = self._decompress_data(compressed_data)
            
            # Vérifier que les données sont valides
            if not save_data or "metadata" not in save_data:
                return {
                    "success": False,
                    "message": "Données de sauvegarde corrompues ou invalides"
                }
            
            # Mettre à jour les métadonnées actuelles
            self.current_save_metadata = save_data["metadata"]
            
            # Réinitialiser le compteur de temps de jeu pour la nouvelle session
            self._reset_play_time_counter()
            
            # Si un objet de jeu est connecté, restaurer son état
            if self.game:
                self._restore_game_state(save_data)
            
            return {
                "success": True,
                "message": f"Jeu chargé avec succès depuis {os.path.basename(save_path)}",
                "save_data": save_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors du chargement: {str(e)}"
            }
    
    def quick_load(self) -> Dict[str, Any]:
        """
        Charge la dernière sauvegarde rapide
        
        Returns:
            Dictionnaire indiquant le succès ou l'échec du chargement
        """
        quick_save_dir = os.path.join(self.save_directory, "quicksave")
        
        # Vérifier que le répertoire existe
        if not os.path.exists(quick_save_dir):
            return {
                "success": False,
                "message": "Aucune sauvegarde rapide disponible"
            }
        
        # Lister les sauvegardes rapides
        quick_saves = [f for f in os.listdir(quick_save_dir) if f.endswith('.mkrp')]
        
        if not quick_saves:
            return {
                "success": False,
                "message": "Aucune sauvegarde rapide disponible"
            }
        
        # Trier par date de modification (la plus récente en premier)
        quick_saves.sort(key=lambda x: os.path.getmtime(os.path.join(quick_save_dir, x)), reverse=True)
        
        # Charger la sauvegarde la plus récente
        return self.load_game(os.path.join(quick_save_dir, quick_saves[0]))
    
    def _restore_game_state(self, save_data: Dict[str, Any]) -> None:
        """
        Restaure l'état du jeu à partir des données de sauvegarde
        
        Args:
            save_data: Données de sauvegarde
        """
        # Restaurer l'état du joueur
        if "player" in save_data and hasattr(self.game, "player"):
            self.game.player = save_data["player"]
        
        # Restaurer l'état du monde
        world_state = save_data.get("world_state", {})
        for key, value in world_state.items():
            if hasattr(self.game, key):
                setattr(self.game, key, value)
        
        # Restaurer les quêtes
        quests = save_data.get("quests", {})
        if hasattr(self.game, "active_quests"):
            self.game.active_quests = quests.get("active_quests", [])
        if hasattr(self.game, "completed_quests"):
            self.game.completed_quests = quests.get("completed_quests", [])
        if hasattr(self.game, "failed_quests"):
            self.game.failed_quests = quests.get("failed_quests", [])
        if hasattr(self.game, "quest_states"):
            self.game.quest_states = quests.get("quest_states", {})
        
        # Restaurer les relations
        if "relationships" in save_data and hasattr(self.game, "relationships"):
            self.game.relationships = save_data["relationships"]
        
        # Restaurer l'inventaire et l'équipement
        if "inventory" in save_data and hasattr(self.game, "inventory"):
            self.game.inventory = save_data["inventory"]
        if "equipment" in save_data and hasattr(self.game, "equipment"):
            self.game.equipment = save_data["equipment"]
        
        # Restaurer les compétences
        if "skills" in save_data and hasattr(self.game, "skills"):
            self.game.skills = save_data["skills"]
        
        # Restaurer les drapeaux de jeu
        if "game_flags" in save_data and hasattr(self.game, "game_flags"):
            self.game.game_flags = save_data["game_flags"]
        
        # Restaurer la mémoire de l'IA
        if "ai_memory" in save_data and hasattr(self.game, "ai_manager"):
            ai_memory = save_data["ai_memory"]
            
            if "conversation_history" in ai_memory:
                self.game.ai_manager.conversation_history = ai_memory["conversation_history"]
            if "memory_by_character" in ai_memory:
                self.game.ai_manager.memory_by_character = ai_memory["memory_by_character"]
            if "world_state_memory" in ai_memory:
                self.game.ai_manager.world_state_memory = ai_memory["world_state_memory"]
            if "player_personality" in ai_memory:
                self.game.ai_manager.player_personality = ai_memory["player_personality"]
        
        # Restaurer les paramètres de contenu mature
        if "mature_content_settings" in save_data and hasattr(self.game, "mature_content_manager"):
            mature_settings = save_data["mature_content_settings"]
            mcm = self.game.mature_content_manager
            
            if "age_verified" in mature_settings:
                mcm.age_verified = mature_settings["age_verified"]
            if "content_enabled" in mature_settings:
                mcm.is_enabled = mature_settings["content_enabled"]
            if "maturity_level" in mature_settings:
                mcm.maturity_level = mature_settings["maturity_level"]
            if "filters" in mature_settings:
                mcm.filters = mature_settings["filters"]
        
        # Appeler une méthode spéciale de restauration si elle existe
        if hasattr(self.game, "restore_additional_state") and callable(getattr(self.game, "restore_additional_state")):
            self.game.restore_additional_state(save_data)
    
    def list_saves(self, slot_name: str = None) -> List[Dict[str, Any]]:
        """
        Liste toutes les sauvegardes disponibles
        
        Args:
            slot_name: Si fourni, liste uniquement les sauvegardes du slot spécifié
            
        Returns:
            Liste des informations sur les sauvegardes
        """
        saves_info = []
        
        try:
            # Si un slot spécifique est demandé
            if slot_name:
                slot_path = os.path.join(self.save_directory, slot_name)
                if os.path.exists(slot_path) and os.path.isdir(slot_path):
                    save_files = [f for f in os.listdir(slot_path) if f.endswith('.mkrp')]
                    
                    for save_file in save_files:
                        save_path = os.path.join(slot_path, save_file)
                        save_info = self._get_save_info(save_path)
                        save_info["slot_name"] = slot_name
                        saves_info.append(save_info)
            # Sinon, lister toutes les sauvegardes
            else:
                # Parcourir tous les slots
                for item in os.listdir(self.save_directory):
                    slot_path = os.path.join(self.save_directory, item)
                    
                    # Ignorer les fichiers, ne traiter que les répertoires
                    if not os.path.isdir(slot_path):
                        continue
                    
                    # Lister les sauvegardes de ce slot
                    save_files = [f for f in os.listdir(slot_path) if f.endswith('.mkrp')]
                    
                    for save_file in save_files:
                        save_path = os.path.join(slot_path, save_file)
                        save_info = self._get_save_info(save_path)
                        save_info["slot_name"] = item
                        saves_info.append(save_info)
            
            # Trier par date de modification (la plus récente en premier)
            saves_info.sort(key=lambda x: x.get("metadata", {}).get("last_save_time", ""), reverse=True)
            
            return saves_info
            
        except Exception as e:
            print(f"Erreur lors du listage des sauvegardes: {e}")
            return []
    
    def delete_save(self, save_path: str) -> Dict[str, Any]:
        """
        Supprime une sauvegarde
        
        Args:
            save_path: Chemin du fichier de sauvegarde à supprimer
            
        Returns:
            Dictionnaire indiquant le succès ou l'échec de la suppression
        """
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(save_path):
                return {
                    "success": False,
                    "message": f"Fichier de sauvegarde introuvable: {save_path}"
                }
            
            # Supprimer le fichier
            os.remove(save_path)
            
            return {
                "success": True,
                "message": f"Sauvegarde supprimée: {os.path.basename(save_path)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la suppression: {str(e)}"
            }
    
    def export_save(self, save_path: str, export_path: str = None) -> Dict[str, Any]:
        """
        Exporte une sauvegarde vers un fichier externe
        
        Args:
            save_path: Chemin du fichier de sauvegarde à exporter
            export_path: Chemin du fichier d'exportation (si non fourni, utilise le nom du fichier)
            
        Returns:
            Dictionnaire indiquant le succès ou l'échec de l'exportation
        """
        try:
            # Vérifier que le fichier source existe
            if not os.path.exists(save_path):
                return {
                    "success": False,
                    "message": f"Fichier de sauvegarde introuvable: {save_path}"
                }
            
            # Si aucun chemin d'exportation n'est fourni, créer un nom dans le répertoire courant
            if not export_path:
                base_name = os.path.basename(save_path)
                export_path = f"export_{base_name}"
            
            # Copier le fichier
            shutil.copy2(save_path, export_path)
            
            return {
                "success": True,
                "message": f"Sauvegarde exportée vers: {export_path}",
                "export_path": export_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'exportation: {str(e)}"
            }
    
    def import_save(self, import_path: str, slot_name: str = "imported") -> Dict[str, Any]:
        """
        Importe une sauvegarde depuis un fichier externe
        
        Args:
            import_path: Chemin du fichier de sauvegarde à importer
            slot_name: Nom du slot où importer la sauvegarde
            
        Returns:
            Dictionnaire indiquant le succès ou l'échec de l'importation
        """
        try:
            # Vérifier que le fichier source existe
            if not os.path.exists(import_path):
                return {
                    "success": False,
                    "message": f"Fichier à importer introuvable: {import_path}"
                }
            
            # Vérifier que c'est bien un fichier de sauvegarde valide
            with open(import_path, 'rb') as f:
                signature = f.read(4)
                if signature != b'MKRP':
                    return {
                        "success": False,
                        "message": "Format de fichier de sauvegarde invalide"
                    }
            
            # Créer le répertoire du slot s'il n'existe pas
            slot_dir = os.path.join(self.save_directory, slot_name)
            os.makedirs(slot_dir, exist_ok=True)
            
            # Nom du fichier importé
            import_name = f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mkrp"
            dest_path = os.path.join(slot_dir, import_name)
            
            # Copier le fichier
            shutil.copy2(import_path, dest_path)
            
            # Gérer les versions de sauvegarde
            self._manage_save_versions(slot_dir)
            
            return {
                "success": True,
                "message": f"Sauvegarde importée avec succès dans le slot {slot_name}",
                "import_path": dest_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de l'importation: {str(e)}"
            }
    
    def create_backup(self) -> Dict[str, Any]:
        """
        Crée une sauvegarde de tous les fichiers de sauvegarde
        
        Returns:
            Dictionnaire indiquant le succès ou l'échec de la sauvegarde
        """
        try:
            # Créer un dossier de backup s'il n'existe pas
            backup_dir = os.path.join(self.save_directory, "backup")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Nom du fichier de sauvegarde
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            backup_path = os.path.join(backup_dir, backup_name)
            
            # Créer une archive ZIP de toutes les sauvegardes
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Ajouter tous les fichiers de sauvegarde
                for root, _, files in os.walk(self.save_directory):
                    # Ignorer le répertoire backup lui-même pour éviter la récursion
                    if root == backup_dir:
                        continue
                        
                    for file in files:
                        if file.endswith('.mkrp'):
                            file_path = os.path.join(root, file)
                            # Ajouter le fichier à l'archive avec un chemin relatif
                            arcname = os.path.relpath(file_path, self.save_directory)
                            zipf.write(file_path, arcname)
            
            return {
                "success": True,
                "message": f"Sauvegarde créée: {backup_name}",
                "backup_path": backup_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la création de la sauvegarde: {str(e)}"
            }
    
    def restore_backup(self, backup_path: str) -> Dict[str, Any]:
        """
        Restaure une sauvegarde à partir d'une archive
        
        Args:
            backup_path: Chemin du fichier de sauvegarde à restaurer
            
        Returns:
            Dictionnaire indiquant le succès ou l'échec de la restauration
        """
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(backup_path):
                return {
                    "success": False,
                    "message": f"Fichier de sauvegarde introuvable: {backup_path}"
                }
            
            # Créer un répertoire temporaire pour l'extraction
            temp_dir = os.path.join(self.save_directory, "temp_restore")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # Extraire l'archive
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Copier les fichiers extraits vers les slots appropriés
            restored_files = 0
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.mkrp'):
                        # Déterminer le chemin source et destination
                        src_path = os.path.join(root, file)
                        rel_path = os.path.relpath(src_path, temp_dir)
                        
                        # Créer le répertoire de destination s'il n'existe pas
                        dest_dir = os.path.dirname(os.path.join(self.save_directory, rel_path))
                        os.makedirs(dest_dir, exist_ok=True)
                        
                        # Copier le fichier
                        shutil.copy2(src_path, os.path.join(self.save_directory, rel_path))
                        restored_files += 1
            
            # Supprimer le répertoire temporaire
            shutil.rmtree(temp_dir)
            
            return {
                "success": True,
                "message": f"Sauvegarde restaurée: {restored_files} fichiers",
                "restored_files": restored_files
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erreur lors de la restauration: {str(e)}"
            }
    
    def is_save_compatible(self, save_path: str) -> Dict[str, Any]:
        """
        Vérifie si une sauvegarde est compatible avec la version actuelle du jeu
        
        Args:
            save_path: Chemin du fichier de sauvegarde à vérifier
            
        Returns:
            Dictionnaire indiquant la compatibilité
        """
        try:
            # Extraire les informations de la sauvegarde
            save_info = self._get_save_info(save_path)
            
            # Vérifier s'il y a eu une erreur
            if "error" in save_info:
                return {
                    "compatible": False,
                    "message": save_info["error"]
                }
            
            # Comparer les versions
            save_version = save_info.get("metadata", {}).get("game_version", "0.0.0")
            current_version = self.current_save_metadata["game_version"]
            
            # Si les versions sont identiques, c'est compatible
            if save_version == current_version:
                return {
                    "compatible": True,
                    "message": "La sauvegarde est compatible avec la version actuelle du jeu."
                }
            
            # Vérifier si la sauvegarde est d'une version antérieure
            # (ici, une comparaison simpliste - dans un vrai jeu, utilisez la sémantique des versions)
            save_v = [int(x) for x in save_version.split('.')]
            current_v = [int(x) for x in current_version.split('.')]
            
            # Si la version majeure est la même, c'est probablement compatible
            if save_v[0] == current_v[0]:
                return {
                    "compatible": True,
                    "message": f"La sauvegarde (v{save_version}) est probablement compatible avec la version actuelle (v{current_version}).",
                    "warning": "Des différences mineures peuvent exister."
                }
            else:
                return {
                    "compatible": False,
                    "message": f"La sauvegarde (v{save_version}) n'est pas compatible avec la version actuelle du jeu (v{current_version}).",
                    "force_option": True
                }
            
        except Exception as e:
            return {
                "compatible": False,
                "message": f"Erreur lors de la vérification de compatibilité: {str(e)}"
            }