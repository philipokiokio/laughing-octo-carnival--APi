from fastapi import Header
from src.projects.project_service import project_service


def mixer_header(mixer_key: str = Header()):
    print(mixer_key)
    project = project_service.get_project_by_header(mixer_key)
    return project
