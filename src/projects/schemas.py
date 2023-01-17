from src.app.utils.schemas_utils import AbstractModel, ResponseModel, MixPanelDataCenter
from typing import List, Optional, Dict


class ProjectCreate(AbstractModel):
    name: str
    mixpanel_key: Optional[str]
    data_center: Optional[MixPanelDataCenter]


class Org(AbstractModel):
    name: str
    slug: str


class User(AbstractModel):
    first_name: str
    last_name: str


class PjRate(AbstractModel):
    count: int


class ProjectResp(ProjectCreate):
    id: int
    slug: str
    api_key: str
    org: Optional[Org]
    is_premium: bool
    creator: Optional[User]
    count_per_hour: List[PjRate]


class ProjectUpdate(AbstractModel):
    name: Optional[str]
    mixpanel_key: Optional[str]
    data_center: Optional[MixPanelDataCenter]


class MessageProjectResp(ResponseModel):
    data: ProjectResp


class MessageListProjectResp(ResponseModel):
    data: List[ProjectResp]


class Distinct(AbstractModel):
    distinct_id: str


class SingleEvent(AbstractModel):
    distinct_id: str
    event: str


class EventProp(SingleEvent):
    properties: dict


class Alias(AbstractModel):
    distinct_id: str
    new_id: str


class Merger(AbstractModel):
    distinct_id: str
    distinct_id_: str


class PeopleProp(AbstractModel):
    distinct_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    extra_props: Optional[dict]


class PeopleProp_(Distinct):
    data: dict


class PeopleUnion(Distinct):
    data: Dict[str, List]


class PeopleUnset(Distinct):
    prop: List[str]


class ChargePeople(Distinct):
    amount: float
    data: dict | None


class BaseGroup(AbstractModel):
    group_key: str
    group_id: str


class GroupProp(BaseGroup):

    data: dict


class GroupUnset(BaseGroup):
    property: List[str]


class GroupMessage(AbstractModel):
    message: str
