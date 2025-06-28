import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI
from modules.brd_builder import build_brd

# Load settings
with open("config/settings.json") as f:
    settings = json.load(f)

# Set up OpenAI client
client = OpenAI(api_key=settings["openai_api_key"])

# Set up Streamlit UI
st.set_page_config(page_title="AI Workflow Assistant", layout="wide")
st.title("📊 AI Workflow Assistant for Junior Analysts")
st.caption("Ask about BRDs, data analysis, dashboards, or code. Projects are saved.")

# Directory to store project files
PROJECT_DIR = settings["default_project_path"]
os.makedirs(PROJECT_DIR, exist_ok=True)

# Load all saved projects
def get_all_projects():
    return sorted([f for f in os.listdir(PROJECT_DIR) if f.endswith(".json")])

def load_project(filename):
    with open(os.path.join(PROJECT_DIR, filename), "r") as f:
        return json.load(f)

def save_project(project_name, history):
    filepath = os.path.join(PROJECT_DIR, project_name + ".json")
    with open(filepath, "w") as f:
        json.dump(history, f, indent=2)

# Sidebar: Project Controls
st.sidebar.header("🗂️ Project Menu")
project_files = get_all_projects()
selected = st.sidebar.selectbox("Select Project", ["➕ New Project"] + project_files)

if selected == "➕ New Project":
    new_name = st.sidebar.text_input("New Project Name")
    if st.sidebar.button("Create"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        st.session_state.project_name = f"{new_name or 'Project'}_{timestamp}"
        st.session_state.history = []
        save_project(st.session_state.project_name, [])
        st.rerun()
else:
    st.session_state.project_name = selected.replace(".json", "")
    st.session_state.history = load_project(selected)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat interface
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Input + BRD trigger
user_input = st.chat_input("Ask a question or describe your task:")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    messages = [
        {"role": "system", "content": (
            "You are a helpful assistant for junior data/business analysts. "
            "Act like a senior analyst mentor. For every task, break it down into steps, offer guidance, and always end with:\n"
            "➡️ 'What would you like to do next? I can help you explore data, write a BRD, run code, or create a dashboard.'"
        )}
    ] + st.session_state.history

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )
    reply = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": reply})

    # Save progress
    save_project(st.session_state.project_name, st.session_state.history)
    st.rerun()

# BRD Builder (Phase 1 UI)
with st.sidebar.expander("📝 Write a BRD"):
    with st.form("brd_form"):
        project_name = st.text_input("Project Name")
        overview = st.text_area("Project Overview")
        objectives = st.text_area("Objectives")
        stakeholders = st.text_area("Stakeholders")
        kpis = st.text_area("Key KPIs", value=", ".join(settings["default_kpis"]))
        success = st.text_area("Success Criteria")
        risks = st.text_area("Risks or Constraints")
        submit = st.form_submit_button("Generate BRD")

    if submit:
        brd_data = {
            "project_overview": overview,
            "objectives": objectives,
            "stakeholders": stakeholders,
            "kpis": kpis,
            "success_criteria": success,
            "risks": risks
        }
        markdown = build_brd(brd_data)
        brd_filename = f"{project_name or 'BRD'}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        brd_path = os.path.join(PROJECT_DIR, brd_filename)
        with open(brd_path, "w") as f:
            f.write(markdown)
        st.success(f"✅ BRD saved as `{brd_filename}`.")
        with st.expander("📄 View BRD"):
            st.markdown(markdown)
        with open(brd_path, "rb") as f:
            st.download_button("⬇️ Download BRD", f, file_name=brd_filename)