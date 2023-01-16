from src.projects.project_repository import project_repo, Project
from src.projects import schemas
from src.app.utils.slugger import slug_gen
from fastapi import status, HTTPException
from src.organization.org_repository import org_repo
from fastapi.encoders import jsonable_encoder


class ProjectService:
    def __init__(self):
        self.project_repo = project_repo
        self.org_repo = org_repo

    def project_does_not_exist(self):
        raise HTTPException(
            detail="This Project does not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    def orm_call(project: Project):
        project_ = jsonable_encoder(project)

        if project.org:
            project_["org"] = project.org
        if project.creator:
            project_["creator"] = project.creator
        return project_

    def org_check(self, org_slug):
        org_check = self.org_repo.get_org(org_slug)
        if not org_check:
            raise HTTPException(
                detail="Org does not Exist", status_code=status.HTTP_404_NOT_FOUND
            )

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
            projects_.append(project)

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
                "This Project does not have a Mix Pannel Key",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return project

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
