from fastapi import APIRouter, status, Header, Depends, HTTPException
from src.projects import schemas, project_service, models
from src.projects.mixer_handler import project_rate_header
from src.app.utils.mixers import Mixer
from src.auth.oauth import get_current_user

project_service = project_service.project_service


project_router = APIRouter(prefix="/api/v1/project", tags={"Org Projects on Mixer"})


@project_router.post(
    "/{org_slug}/create/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MessageProjectResp,
)
def create_project(
    org_slug: str,
    project: schemas.ProjectCreate,
    current_user: dict = Depends(get_current_user),
):
    resp = project_service.create_project(org_slug, project, current_user)
    return resp


@project_router.get(
    "s/{org_slug}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageListProjectResp,
)
def get_projects(org_slug: str, current_user: dict = Depends(get_current_user)):
    resp = project_service.get_projects(org_slug)
    return resp


@project_router.get(
    "/org/{org_slug}/{slug}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageProjectResp,
)
def fetch_project(
    org_slug: str, slug: str, current_user: dict = Depends(get_current_user)
):
    resp = project_service.get_project(org_slug, slug)
    return resp


@project_router.delete(
    "/org/{org_slug}/{slug}/delete/", status_code=status.HTTP_204_NO_CONTENT
)
def delete_project(
    org_slug: str, slug: str, current_user: dict = Depends(get_current_user)
):
    resp = project_service.delete_project(slug, org_slug)
    return resp


@project_router.patch(
    "/org/{org_slug}/{slug}/update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageProjectResp,
)
def update_project(
    org_slug: str,
    slug: str,
    update_project: schemas.ProjectUpdate,
    current_user: dict = Depends(get_current_user),
):

    resp = project_service.update_project(org_slug, slug, update_project)

    return resp


@project_router.post(
    "/events/mixpanel/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def single_event(
    event: schemas.SingleEvent, project: dict = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.track_single_event(event.distinct_id, event.event)

    resp = {
        "message": "event sent successfully to Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Event was not sent successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/events/mixpanel/props/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def event_props(
    event: schemas.EventProp, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.track_events(event.distinct_id, event.event, event.properties)

    resp = {
        "message": "event sent successfully to Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Event was not sent successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/distinct-id/mixpanel/update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def update_distinct_id(
    event: schemas.Alias, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.create_alias(event.distinct_id, event.new_id)

    resp = {
        "message": "Alias updated successfully to Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Alias was not updated successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


# @project_router.post(
#     "/distinct-id/mixpanel/merge/",
#     status_code=status.HTTP_200_OK,
#     response_model=schemas.ResponseModel,
# )
# def merge_distinct_ids(
#     event: schemas.Merger, project: models.Project = Depends(project_rate_header)
# ):

#     mixer = Mixer(project.mixpanel_key, project.data_center)
#     bool = mixer.merge_alias(event.distinct_id, event.distinct_id_)

#     resp = {
#         "message": "Alias merged successfully to Mix Pannel",
#         "status": status.HTTP_200_OK,
#     }

#     if not bool:
#         raise HTTPException(
#             detail="Alias was not merged successfully",
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )

#     return resp


@project_router.post(
    "/people/mixpanel/props/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def create_people_props(
    event: schemas.PeopleProp, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.people_prop(event.distinct_id, event)

    resp = {
        "message": "People Props was created successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="People Props was not created successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/add/prop/once/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def set_people_prop_once(
    event: schemas.PeopleProp_, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.people_set_(event.distinct_id, event.data)

    resp = {
        "message": "People Prop set once in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="People Prop was not set once successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/increment/prop/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def increment_people_prop(
    event: schemas.PeopleProp_, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.increment_people(event.distinct_id, event.data)

    resp = {
        "message": "People Prop was incremented successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="People Prop was not incremented successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/append/prop/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def append_people_prop(
    event: schemas.PeopleProp_, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.append_to_people(event.distinct_id, event.data)

    resp = {
        "message": "People Prop of Array was Appended to successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="People Prop of Array was not Appended successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/union/prop/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def union_people_prop(
    event: schemas.PeopleUnion, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.union_people(event.distinct_id, event.data)

    resp = {
        "message": "People Prop of Array was added successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="People Prop of Array was not added successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/unset/prop/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def unset_people_prop(
    event: schemas.PeopleUnset, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.unset_people(event.distinct_id, event.prop)

    resp = {
        "message": "People Prop removed successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="People Prop was not removed successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/remove/prop/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def remove_people_prop(
    event: schemas.PeopleProp_, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.remove_people_prop(event.distinct_id, event.data)

    resp = {
        "message": "People Prop removed successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="People Prop was not removed successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/delete/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def delete_people_prop(
    event: schemas.Distinct, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.delete_people(event.distinct_id)

    resp = {
        "message": "Person deleted successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Person was not deleted successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/charge/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def charge_people_prop(
    event: schemas.ChargePeople, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.charge_people(event.distinct_id, event.amount, event.data)

    resp = {
        "message": "Person Charged successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Person was not charged successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/people/mixpanel/clear/charge/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def clear_people_charge(
    event: schemas.Distinct, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.clear_people_charge(event.distinct_id)

    resp = {
        "message": "Person charge cleared successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Person charge was not cleared successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/group/mixpanel/prop/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def create_group(
    event: schemas.GroupProp, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.set_group(event.group_key, event.group_id, event.data)

    resp = {
        "message": "Group Profile created successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Group Profile was not created successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/group/mixpanel/once/prop/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def create_group_once(
    event: schemas.GroupProp, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.set_group_(event.group_key, event.group_id, event.data)

    resp = {
        "message": "Group Profile Prop set once successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Group Profile Prop was not set successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/group/mixpanel/union/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def group_union(
    event: schemas.GroupProp, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.union_group(event.group_key, event.group_id, event.data)

    resp = {
        "message": "Group Profile merged successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Group Profile was not merged successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/group/mixpanel/unset/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def group_unset(
    event: schemas.GroupUnset, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.unset_group(event.group_key, event.group_id, event.property)

    resp = {
        "message": "Group Props removed successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Group Props was not removed successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/group/mixpanel/remove/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def group_remove(
    event: schemas.GroupProp, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.remove_group(event.group_key, event.group_id, event.data)

    resp = {
        "message": "Group Prop removed successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Group Prop was not removed successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


@project_router.post(
    "/group/mixpanel/delete/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseModel,
)
def delete_group(
    event: schemas.BaseGroup, project: models.Project = Depends(project_rate_header)
):

    mixer = Mixer(project.mixpanel_key, project.data_center)
    bool = mixer.delete_group(event.group_key, event.group_id)

    resp = {
        "message": "Group deleted successfully in Mix Pannel",
        "status": status.HTTP_200_OK,
    }

    if not bool:
        raise HTTPException(
            detail="Group was not deleted successfully",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return resp


# @project_router.post(
#     "/groups/mixpanel/update/",
#     status_code=status.HTTP_200_OK,
#     response_model=schemas.ResponseModel,
# )
# def update_groups(
#     event: schemas.GroupMessage, project: models.Project = Depends(project_rate_header)
# ):

#     mixer = Mixer(project.mixpanel_key, project.data_center)
#     bool = mixer.update_groups(event.message)

#     resp = {
#         "message": "Groups Updated successfully in Mix Pannel",
#         "status": status.HTTP_200_OK,
#     }

#     if not bool:
#         raise HTTPException(
#             detail="Group was not updated successfully",
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )

#     return resp
