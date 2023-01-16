from pydantic import BaseModel, BaseSettings, EmailStr
from enum import Enum


class AbstractModel(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True


class AbstractSettings(BaseSettings):
    class Config:
        env_file = ".env"


class ResponseModel(AbstractModel):
    message: str
    status: int


class MixPanelDataCenter(Enum):
    eu = "EU"
    other = "Others"


class RoleOptions(Enum):
    admin = "Admin"
    member = "Member"


class User(AbstractModel):
    first_name: str
    last_name: str
    email: EmailStr
