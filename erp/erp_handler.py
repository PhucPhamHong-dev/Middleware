from typing import Dict
from utils.erp_client import ERPClient

def handle_intent(intent_obj: Dict) -> Dict:
    """
    Handle the intent by interacting with the ERP system.

    Args:
        intent_obj (Dict): A dictionary containing 'intent', 'task_name', and 'project_name'.

    Returns:
        Dict: A dictionary indicating the status and result of the operation.
    """
    intent = intent_obj.get("intent")
    task_name = intent_obj.get("task_name")
    project_name = intent_obj.get("project_name")

    erp_client = ERPClient(base_url="http://erpnext.local", api_key="your_api_key", api_secret="your_api_secret")

    if intent == "create_task":
        project = erp_client.get_project_by_name(project_name)
        if not project:
            return {"status": "error", "message": f"Project '{project_name}' not found."}
        task = erp_client.create_task(task_name=task_name, project_id=project["name"])
        return {"status": "success", "task": task}
    else:
        return {"status": "error", "message": "Unsupported intent."}