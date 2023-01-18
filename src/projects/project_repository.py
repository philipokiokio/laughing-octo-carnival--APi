from src.app.utils.base_repository import BaseRepo
from src.projects.models import Project, ProjectRateLimit
from datetime import datetime, timedelta
from sqlalchemy import and_


class ProjectRepository(BaseRepo):
    def base_query(self):
        return self.db.query(Project)

    def get_projects(self, org_id):
        return self.base_query().filter(Project.org_id == org_id).all()

    def get_project(self, slug, org_id):
        return (
            self.base_query()
            .filter(Project.slug == slug, Project.org_id == org_id)
            .first()
        )

    def get_project_name(self, name, org_id):
        return (
            self.base_query()
            .filter(Project.name.ilike(name), Project.org_id == org_id)
            .first()
        )

    def create_project(self, project_data: dict) -> Project:
        new_project = Project(**project_data)
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)
        return new_project

    def update_project(self, project_update: Project) -> Project:
        self.db.commit()
        self.db.refresh(project_update)
        return project_update

    def delete_project(self, project: Project):
        self.db.delete(project)
        self.db.commit()

    def get_project_by_header(self, header_key: str):
        return self.base_query().filter(Project.api_key == header_key).first()


class ProjectRateRepo(BaseRepo):
    def base_query(self):
        return self.db.query(ProjectRateLimit)

    def get_project_rate(self, project_id: int):

        return (
            self.base_query().filter(ProjectRateLimit.project_id == project_id).first()
        )

    def get_project_hour(self, project_id):

        return (
            self.base_query()
            .filter(
                ProjectRateLimit.project_id == project_id,
                and_(
                    ProjectRateLimit.date_updated <= datetime.now(),
                    ProjectRateLimit.date_updated > datetime.now() - timedelta(hours=1),
                ),
            )
            .first()
        )

    def update_pj_rate_base_hour(self, pj_rate: ProjectRateLimit):

        pj_rate.count = 0

        self.db.commit()
        self.db.refresh(pj_rate)
        return True

    def get_all_pj_rate(self):
        return self.base_query().all()

    def create_project_rate(self, new_project_rate) -> ProjectRateLimit:
        new_pj_rate = ProjectRateLimit(**new_project_rate)
        self.db.add(new_pj_rate)
        self.db.commit()
        self.db.refresh(new_pj_rate)
        return new_pj_rate

    def update_project_rate(self, project_rate: ProjectRateLimit) -> ProjectRateLimit:

        self.db.commit()
        self.db.refresh(project_rate)
        return project_rate


project_repo = ProjectRepository()
pj_rate_repo = ProjectRateRepo()
