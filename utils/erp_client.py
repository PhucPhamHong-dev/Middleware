import requests
from typing import Optional

class ERPClient:
    """
    A client to interact with the ERP system via REST API.
    """

    def __init__(self, base_url: str, api_key: str, api_secret: str):
        """
        Initialize the ERPClient with authentication details.

        Args:
            base_url (str): The base URL of the ERP system.
            api_key (str): The API key for authentication.
            api_secret (str): The API secret for authentication.
        """
        self.base_url = base_url
        self.auth = (api_key, api_secret)

    def get_project_by_name(self, project_name: str) -> Optional[dict]:
        """
        Retrieve a project by its name.

        Args:
            project_name (str): The name of the project.

        Returns:
            Optional[dict]: The project data if found, else None.
        """
        response = requests.get(
            f"{self.base_url}/api/resource/Project",
            params={"filters": f'[["project_name", "=", "{project_name}"]]'},
            auth=self.auth
        )
        if response.status_code == 200 and response.json().get("data"):
            return response.json()["data"][0]
        return None

    def create_task(self, task_name: str, project_id: str) -> dict:
        """
        Create a new task under a specified project.

        Args:
            task_name (str): The name of the task.
            project_id (str): The ID of the project.

        Returns:
            dict: The created task data.
        """
        data = {
            "subject": task_name,
            "project": project_id
        }
        response = requests.post(
            f"{self.base_url}/api/resource/Task",
            json=data,
            auth=self.auth
        )
        return response.json()
