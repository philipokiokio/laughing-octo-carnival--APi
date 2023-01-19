from datetime import datetime, timedelta

from sqlalchemy import or_

from src.app.utils.base_repository import BaseRepo
from src.projects.models import Project, ProjectRateLimit


class ProjectRepository(BaseRepo):
    def base_query(self):
        """Gets the base query for Project

        Returns:
            _type_: query(Project)
        """
        return self.db.query(Project)

    def get_projects(self, org_id: int):
        """Gets Project based on Org Id.

        Args:
            org_id (int): organization id

        Returns:
            _type_: Projects
        """
        return self.base_query().filter(Project.org_id == org_id).all()

    def get_project(self, slug: str, org_id: int):
        """Get Project based on project slug and Organization id

        Args:
            slug (str): Project slug
            org_id (int): Organization id

        Returns:
            _type_: The DB Record if any.
        """
        return (
            self.base_query()
            .filter(Project.slug == slug, Project.org_id == org_id)
            .first()
        )

    def get_project_name(self, name, org_id):
        """Get Project based on project name and Organization id

        Args:
            name (str): Project name
            org_id (int): Organization id

        Returns:
            _type_: The DB Record if any.
        """
        return (
            self.base_query()
            .filter(Project.name.ilike(name), Project.org_id == org_id)
            .first()
        )

    def create_project(self, project_data: dict) -> Project:
        """Create new Project

        Args:
            project_data (dict): Project data

        Returns:
            Project: DB record of Project.
        """
        new_project = Project(**project_data)
        self.db.add(new_project)
        self.db.commit()
        self.db.refresh(new_project)
        return new_project

    def update_project(self, project_update: Project) -> Project:
        """Update a Record of Project

        Args:
            project_update (Project): SQLAlchemy object representing a DB record

        Returns:
            Project: _description_
        """
        self.db.commit()
        self.db.refresh(project_update)
        return project_update

    def delete_project(self, project: Project):
        """Delete Project from Table

        Args:
            project (Project): SQLAlchemy Object.
        """
        self.db.delete(project)
        self.db.commit()

    def get_project_by_header(self, header_key: str):
        """Get Project based on the API-KEY associated with a project.


        Args:
            header_key (str)

        Returns:
            _type_: DB query for this record
        """
        return self.base_query().filter(Project.api_key == header_key).first()


class ProjectRateRepo(BaseRepo):
    """Project Rate Limit ORM

    Args:
        BaseRepo (_type_): Inhert the DB instance
    """

    def base_query(self):
        """Base Table query

        Returns:
            _type_: Table query
        """
        return self.db.query(ProjectRateLimit)

    def get_project_rate(self, project_id: int):
        """Get Project Rate Limit instance in the DB.

        Args:
            project_id (int): id of the Projet instance.

        Returns:
            _type_: Project Rate Limit instance
        """
        return (
            self.base_query().filter(ProjectRateLimit.project_id == project_id).first()
        )

    def get_project_hour(self, project_id):
        """Return Project RateLimit based on the current hour

        Args:
            project_id (_type_): Project Id

        Returns:
            _type_: Project Rate Limit instance
        """
        return (
            self.base_query()
            .filter(
                ProjectRateLimit.project_id == project_id,
                or_(
                    ProjectRateLimit.date_updated <= datetime.now(),
                    ProjectRateLimit.date_updated > datetime.now() - timedelta(hours=1),
                ),
            )
            .first()
        )

    def update_pj_rate_base_hour(self, pj_rate: ProjectRateLimit):
        """Reverting project Rate Limit back to the hour default

        Args:
            pj_rate (ProjectRateLimit): SQLAlchemy Object instance

        Returns:
            _type_: True when done successfully updated.
        """
        pj_rate.count = 0

        self.db.commit()
        self.db.refresh(pj_rate)
        return True

    def get_all_pj_rate(self):
        """Returns all Project Rate Limit data.

        Returns:
            _type_: Project Rate Limit for all
        """
        return self.base_query().all()

    def create_project_rate(self, new_project_rate: dict) -> ProjectRateLimit:
        """Create Project Rate Limit

        Args:
            new_project_rate (dict): Project Rate Limit.

        Returns:
            ProjectRateLimit: DB instance of ProjectRateLimit.
        """
        new_pj_rate = ProjectRateLimit(**new_project_rate)
        self.db.add(new_pj_rate)
        self.db.commit()
        self.db.refresh(new_pj_rate)
        return new_pj_rate

    def update_project_rate(self, project_rate: ProjectRateLimit) -> ProjectRateLimit:
        """Updating project Rate Limit

        Args:
            pj_rate (ProjectRateLimit): SQLAlchemy Object instance

        Returns:
            _type_: Updated SQLAlchemy Object Record
        """
        self.db.commit()
        self.db.refresh(project_rate)
        return project_rate


project_repo = ProjectRepository()
pj_rate_repo = ProjectRateRepo()
