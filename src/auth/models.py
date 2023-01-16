from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.app.utils.models_utils import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)


class RefreshToken(AbstractModel):
    __tablename__ = "user_refresh_token"
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, nullable=False)
    user = relationship("User", passive_deletes=True)
