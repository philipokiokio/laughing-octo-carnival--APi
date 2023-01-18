from src.projects.project_repository import (
    project_repo,
    Project,
    pj_rate_repo,
    ProjectRateLimit,
)
from src.projects import schemas
from src.app.utils.slugger import slug_gen
from fastapi import status, HTTPException
from src.organization.org_repository import org_repo
from fastapi.encoders import jsonable_encoder


class ProjectService:
    def __init__(self):
        self.project_repo = project_repo
        self.org_repo = org_repo
        self.pj_rate_repo = pj_rate_repo

    def project_does_not_exist(self):
        raise HTTPException(
            detail="This Project does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    def orm_call(self, project: Project):
        project_ = jsonable_encoder(project)

        if project.org:
            project_["org"] = project.org
        if project.creator:
            project_["creator"] = project.creator

        project_["count_per_hour"] = project.pj_rate
        return project_

    def org_check(self, org_slug):
        org_check = self.org_repo.get_org(org_slug)
        if not org_check:
            raise HTTPException(
                detail="Org does not Exist", status_code=status.HTTP_404_NOT_FOUND
            )
        return org_check

    def create_project(
        self,
        org_slug: str,
        create_project: schemas.ProjectCreate,
        current_user,
    ) -> schemas.MessageProjectResp:

        org_check = self.org_check(org_slug)

        create_project_ = create_project.dict()
        project_check = self.project_repo.get_project_name(
            create_project.name, org_check.id
        )
        if project_check:
            raise HTTPException(
                detail="Project Exists", status_code=status.HTTP_409_CONFLICT
            )

        create_project_["slug"] = slug_gen()[:8]
        create_project_["api_key"] = slug_gen()[:14]
        create_project_["org_id"] = org_check.id
        create_project_["created_by"] = current_user.id

        new_project = self.project_repo.create_project(create_project_)

        project_rate_data = {"project_id": new_project.id, "count": 0}
        self.pj_rate_repo.create_project_rate(project_rate_data)

        new_project_ = self.orm_call(new_project)
        return {
            "message": "Project Created Successfully",
            "data": new_project_,
            "status": status.HTTP_201_CREATED,
        }

    def get_project(self, org_slug: str, slug: str) -> schemas.MessageProjectResp:
        org_check = self.org_check(org_slug)

        project = self.project_repo.get_project(slug, org_check.id)

        if not project:
            raise HTTPException(
                detail="This Project does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        project_ = self.orm_call(project)
        return {
            "message": "Project retrieved Successful",
            "data": project_,
            "status": status.HTTP_200_OK,
        }

    def get_projects(self, org_slug) -> schemas.MessageListProjectResp:
        org_check = self.org_check(org_slug)

        projects = self.project_repo.get_projects(org_check.id)

        if not projects:
            raise HTTPException(
                detail="Projects do not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        projects_ = []
        for project in projects:
            projects_.append(self.orm_call(project))

        return {
            "message": "Projects retrieved Successful",
            "data": projects_,
            "status": status.HTTP_200_OK,
        }

    def delete_project(self, slug: str, org_slug: str):
        org_check = self.org_check(org_slug)

        project = self.project_repo.get_project(slug, org_check.id)
        if not project:
            raise HTTPException(
                detail="This Project does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        self.project_repo.delete_project(project)

        return {"status": status.HTTP_204_NO_CONTENT}

    def get_project_by_header(self, header: str):
        project = project_repo.get_project_by_header(header)
        if not project:
            self.project_does_not_exist()

        project: Project = project
        if not project.mixpanel_key:
            raise HTTPException(
                detail="This Project does not have a Mix Pannel Key",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return project

    def get_project_rate_limit(self, project_id) -> ProjectRateLimit:
        pj_rate = self.pj_rate_repo.get_project_rate(project_id)
        if not pj_rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project Rate Info does not exist",
            )
        return pj_rate

    def get_pjs_rate_limit(self):
        pj_rates = pj_rate_repo.get_all_pj_rate()

        if not pj_rates:
            return "No Projects to Revert base count"
        for pj_rate in pj_rates:
            pj_rate_repo.update_pj_rate_base_hour(pj_rate)
        return "Project Rates for all project count is reverted to 0"

    def update_project(
        self, org_slug: str, slug: str, update_project: schemas.ProjectUpdate
    ):
        org_check = self.org_check(org_slug)

        project = self.project_repo.get_project(slug, org_check.id)
        if not project:
            self.project_does_not_exist()
        update_project_ = update_project.dict(exclude_unset=True)
        for key, value in update_project_.items():
            setattr(project, key, value)

        updated_project = self.project_repo.update_project(project)
        project_ = self.orm_call(updated_project)
        return {
            "message": "Project updated successfully",
            "data": project_,
            "status": status.HTTP_200_OK,
        }


project_service = ProjectService()
