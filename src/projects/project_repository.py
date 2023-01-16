from src.app.utils.base_repository import BaseRepo
from src.projects.models import Project


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


project_repo = ProjectRepository()
