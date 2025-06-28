from datetime import datetime

def build_brd(brd_data: dict) -> str:
    """
    Construct a markdown-formatted Business Requirements Document (BRD)
    from the provided answers.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# 📄 BRD: {brd_data.get('project_name', 'Unnamed Project')}\n",
        f"*Generated on {timestamp}*\n\n",
        "## 🧭 Project Overview\n",
        f"{brd_data.get('project_overview', 'N/A')}\n\n",
        "## 🎯 Objectives\n",
        f"{brd_data.get('objectives', 'N/A')}\n\n",
        "## 👥 Stakeholders\n",
        f"{brd_data.get('stakeholders', 'N/A')}\n\n",
        "## 📊 KPIs\n",
        f"{brd_data.get('kpis', 'N/A')}\n\n",
        "## 📈 Success Criteria\n",
        f"{brd_data.get('success_criteria', 'N/A')}\n\n",
        "## ⚠️ Risks and Constraints\n",
        f"{brd_data.get('risks', 'N/A')}\n\n",
    ]
    return "".join(lines)