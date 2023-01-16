from src.app.utils.models_utils import AbstractModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, text
from sqlalchemy.orm import relationship


class Project(AbstractModel):
    __tablename__ = "projects"

    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)

    org_id = Column(
        Integer, ForeignKey("orgnization.id", ondelete="CASCADE"), nullable=False
    )
    api_key = Column(String, nullable=False)
    data_center = Column(String, nullable=True)
    mixpanel_key = Column(String, nullable=True)

    is_premium = Column(Boolean, server_default=text("false"))
    created_by = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    org = relationship("Organization")
    creator = relationship("User")


class ProjectRateLimit(AbstractModel):
    __tablename__ = "project_rate_limit"

    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    count = Column(Integer, nullable=False, default=0)
