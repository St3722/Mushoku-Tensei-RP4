# fix_imports.py - Script pour corriger les problèmes d'importation
import os
import sys
import importlib.util
import json

def check_module(module_path, class_name):
    """Vérifie si un module contient bien la classe attendue"""
    print(f"Vérification de {os.path.basename(module_path)} pour la classe {class_name}...")
    
    if not os.path.exists(module_path):
        print(f"❌ Le fichier {module_path} n'existe pas!")
        return False

    try:
        with open(module_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Vérifier si la classe est définie dans le fichier
        if f"class {class_name}" in content:
            print(f"✅ La classe {class_name} existe dans le fichier!")
            return True
        else:
            print(f"❌ La classe {class_name} n'est pas définie dans le fichier!")
            
            # Chercher des classes alternatives qui pourraient être utilisées
            import re
            classes = re.findall(r"class\s+(\w+)", content)
            if classes:
                print(f"   Classes trouvées dans le fichier: {', '.join(classes)}")
            
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
        return False

def fix_class_name(module_path, wrong_class_name, correct_class_name):
    """Corrige le nom d'une classe dans un fichier"""
    try:
        with open(module_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remplacer le nom de la classe
        new_content = content.replace(f"class {wrong_class_name}", f"class {correct_class_name}")
        
        # Sauvegarder le fichier modifié
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"✅ Nom de classe corrigé: {wrong_class_name} → {correct_class_name}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la correction du nom de classe: {e}")
        return False

def create_init_file(directory):
    """Crée un fichier __init__.py pour faciliter l'importation"""
    try:
        init_path = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, "w", encoding="utf-8") as f:
                f.write("# Ce fichier permet à Python de reconnaître ce dossier comme un package\n")
            print(f"✅ Fichier {init_path} créé!")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du fichier __init__.py: {e}")
        return False

def check_json_file(json_path):
    """Vérifie si un fichier JSON est correctement formaté"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        if not content:
            print(f"❌ Le fichier {os.path.basename(json_path)} est vide!")
            return False
        
        # Essayer de parser le JSON
        try:
            json.loads(content)
            print(f"✅ Le fichier {os.path.basename(json_path)} est un JSON valide!")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Erreur dans le fichier JSON {os.path.basename(json_path)}: {e}")
            
            # Afficher les premiers caractères pour diagnostic
            print(f"   Début du fichier: {repr(content[:50])}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier {os.path.basename(json_path)}: {e}")
        return False

def fix_empty_json(json_path, default_content):
    """Corrige un fichier JSON vide ou mal formaté"""
    try:
        # Vérifier si le fichier existe et est vide ou invalide
        needs_fixing = False
        
        if not os.path.exists(json_path):
            needs_fixing = True
        else:
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                
                if not content:
                    needs_fixing = True
                else:
                    try:
                        json.loads(content)
                        # Le JSON est valide, pas besoin de correction
                    except json.JSONDecodeError:
                        needs_fixing = True
            except:
                needs_fixing = True
        
        if needs_fixing:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(default_content, f, ensure_ascii=False, indent=2)
            print(f"✅ Fichier JSON {os.path.basename(json_path)} corrigé!")
            return True
        
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la correction du fichier JSON: {e}")
        return False

def diagnose_and_fix():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.join(base_dir, "modules")
    data_dir = os.path.join(base_dir, "data")
    
    # S'assurer que les dossiers existent
    os.makedirs(modules_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    print("\n==== DIAGNOSTIC ET CORRECTION DES PROBLÈMES D'IMPORTATION ====\n")
    
    # 1. Vérifier les modules Python et les classes
    modules_to_check = [
        {"file": "save_manager.py", "class": "SaveManager"},
        {"file": "character_progression.py", "class": "CharacterProgression"},
        {"file": "interface_cli.py", "class": "InterfaceCLI"},
        {"file": "ai_manager.py", "class": "AIManager"}
    ]
    
    # Créer un fichier __init__.py dans le dossier modules
    create_init_file(modules_dir)
    
    # Vérifier chaque module
    for module in modules_to_check:
        module_path = os.path.join(modules_dir, module["file"])
        if not check_module(module_path, module["class"]):
            print(f"⚠️ Problème avec {module['file']}! Vérifiez le nom de la classe...")
    
    # 2. Vérifier les fichiers JSON
    json_files = ["interactions.json", "npcs.json", "items.json", "quests.json", 
                 "locations.json", "combat.json", "skills.json", "events.json",
                 "progression.json", "mature.json"]
    
    print("\n==== DIAGNOSTIC ET CORRECTION DES FICHIERS JSON ====\n")
    
    # Contenu par défaut pour les fichiers JSON
    default_json_content = {
        "interactions.json": {"dialogues": {"welcome": {"text": "Bienvenue dans le jeu!", "options": []}}},
        "npcs.json": {"default_npc": {"name": "Villageois", "dialogue": "Bonjour aventurier!"}},
        "items.json": {"potion": {"name": "Potion de soin", "effect": {"health": 50}}},
        "quests.json": {"quest_1": {"name": "Première quête", "description": "Une quête simple"}},
        "locations.json": {"village": {"name": "Village de départ", "description": "Point de départ"}},
        "combat.json": {"enemies": {"goblin": {"hp": 30, "damage": 5}}},
        "skills.json": {"attack": {"name": "Attaque", "damage": 10}},
        "events.json": {"start": {"description": "Le début de l'aventure"}},
        "progression.json": {"levels": {"1": {"xp": 0}, "2": {"xp": 100}}},
        "mature.json": {"settings": {"enabled": False}}
    }
    
    # Vérifier et corriger chaque fichier JSON
    for json_file in json_files:
        json_path = os.path.join(data_dir, json_file)
        if not check_json_file(json_path):
            print(f"⚠️ Tentative de correction de {json_file}...")
            if json_file in default_json_content:
                fix_empty_json(json_path, default_json_content[json_file])
    
    print("\n==== NETTOYAGE DES FICHIERS CACHE ====\n")
    
    # 3. Nettoyer les fichiers cache
    pycache_dir = os.path.join(modules_dir, "__pycache__")
    if os.path.exists(pycache_dir):
        for file in os.listdir(pycache_dir):
            if file.endswith(".pyc"):
                try:
                    os.remove(os.path.join(pycache_dir, file))
                    print(f"✅ Fichier cache supprimé: {file}")
                except:
                    print(f"❌ Impossible de supprimer le fichier cache: {file}")
    
    print("\n==== DIAGNOSTIC TERMINÉ ====\n")
    print("Si certains problèmes persistent, voici les actions à entreprendre manuellement:")
    print("1. Pour les modules Python: Vérifiez que chaque fichier contient la classe appropriée")
    print("2. Pour les fichiers JSON: Vérifiez qu'ils contiennent des données JSON valides")
    print("3. Redémarrez votre environnement Python pour effacer toute mise en cache")
    
    return True

if __name__ == "__main__":
    try:
        diagnose_and_fix()
    except Exception as e:
        print(f"❌ Erreur générale lors du diagnostic: {e}")
    
    print("\nAppuyez sur Entrée pour quitter...")
    input()