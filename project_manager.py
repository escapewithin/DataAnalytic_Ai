import os
import json
from datetime import datetime

PROJECTS_DIR = "projects"

def create_project(project_name):
    safe_name = project_name.replace(" ", "_").lower()
    project_path = os.path.join(PROJECTS_DIR, safe_name)
    os.makedirs(project_path, exist_ok=True)
    os.makedirs(os.path.join(project_path, "outputs"), exist_ok=True)

    metadata_path = os.path.join(project_path, "metadata.json")
    if not os.path.exists(metadata_path):
        metadata = {
            "project_name": project_name,
            "created_at": datetime.now().isoformat()
        }
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)

    return safe_name

def save_message(project_id, role, message):
    chat_path = os.path.join(PROJECTS_DIR, project_id, "chat_history.json")
    if os.path.exists(chat_path):
        with open(chat_path, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append({"role": role, "message": message})

    with open(chat_path, "w") as f:
        json.dump(history, f, indent=2)

def load_history(project_id):
    chat_path = os.path.join(PROJECTS_DIR, project_id, "chat_history.json")
    if os.path.exists(chat_path):
        with open(chat_path, "r") as f:
            return json.load(f)
    return []

def list_projects():
    if not os.path.exists(PROJECTS_DIR):
        return []
    return [name for name in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, name))]