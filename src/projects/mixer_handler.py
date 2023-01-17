from fastapi import Header, Depends, HTTPException, status
from src.projects.project_service import project_service, Project


def mixer_header(mixer_key: str = Header()):
    project = project_service.get_project_by_header(mixer_key)
    return project


def project_rate_header(project: Project = Depends(mixer_header)):
    if project.is_premium is False:
        pj_rate = project_service.get_project_rate_limit(project.id)
        pj_rate_for_last_hour = project_service.pj_rate_repo.get_project_hour(
            project.id
        )

        if pj_rate_for_last_hour.count >= 50:
            raise HTTPException(
                detail="This Project has reached it maximum call for the hour, check back in an hour",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        pj_rate.count += 1
        project_service.pj_rate_repo.update_project_rate(pj_rate)
        return project
