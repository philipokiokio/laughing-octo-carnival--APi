from fastapi import Depends, Header, HTTPException, status

from src.projects.project_service import Project, project_service


def mixer_header(mixer_key: str = Header()):
    """_Using Mix-Key Header to get Project information from API Key_

    Args:
        mixer_key (str, optional): _description_. Defaults to Header().

    Returns:
        _type_: Project if it exists. Throws Exception if project does not exist.
    """
    # gets project based on API_KEY
    project = project_service.get_project_by_header(mixer_key)
    return project


def project_rate_header(project: Project = Depends(mixer_header)):
    """Depends on the Mixer header
    Throttles an endpoint if a project is freemium.
    Args:
        project (Project, optional): _description_. Defaults to Depends(mixer_header).

    Raises:
        HTTPException: Throttles the Endpoint based on the request and Project API Key count.

    Returns:
        _type_: Project is returned.
    """
    # checks if the project is premium.
    if project.is_premium is False:
        # check if Project Rate Limit data from Project.
        pj_rate = project_service.get_project_rate_limit(project.id)
        pj_rate_for_last_hour = project_service.pj_rate_repo.get_project_hour(
            project.id
        )

        # checks the rate limit count.
        if pj_rate_for_last_hour.count >= 2:
            raise HTTPException(
                detail=f"This Project has reached it maximum call for the hour: {pj_rate_for_last_hour.count}, check back in an hour",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # increases the count once the project rate limit is < 50.
        pj_rate.count += 1
        project_service.pj_rate_repo.update_project_rate(pj_rate)
        # returns project.
        return project
