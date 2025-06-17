import requests
from flask import current_app

def create_project_with_tasks(name: str, tasks: list) -> str:
    base = current_app.config["ERPNEXT_URL"]
    auth  = (current_app.config["ERPNEXT_API_KEY"], current_app.config["ERPNEXT_API_SECRET"])

    # 1) Tạo Project
    proj_payload = {"doctype": "Project", "project_name": name}
    r1 = requests.post(f"{base}/Project", json=proj_payload, auth=auth)
    r1.raise_for_status()
    proj_id = r1.json().get("data", {}).get("name")

    # 2) Loop tạo Task
    for t in tasks:
        task_payload = {
            "doctype": "Task",
            "project": proj_id,
            "subject": t.get("title"),
            "description": t.get("description", "")
        }
        r2 = requests.post(f"{base}/Task", json=task_payload, auth=auth)
        r2.raise_for_status()

    return proj_id
