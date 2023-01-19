from datetime import datetime

from mixpanel import Consumer, Mixpanel

from src.app.utils.schemas_utils import MixPanelDataCenter


class Mixer:
    def __init__(
        self,
        token,
        data_center,
    ):
        self.token: str = token
        self.data_center: str | None = data_center

    def gravity(self):
        if self.data_center:
            if self.data_center == MixPanelDataCenter.eu.value:
                return self.core_eu()
            else:
                return self.core_()

    def core_(self) -> Mixpanel:
        core = Mixpanel(self.token)
        return core

    def core_eu(self) -> Mixpanel:
        core_eu = Mixpanel(
            self.token,
            consumer=Consumer(api_host="api-eu.mixpanel.com"),
        )
        return core_eu

    def track_single_event(self, distinct_id, event: str):

        # if mixpanel is EU
        mp: Mixpanel = self.gravity()
        mp.track(distinct_id, event)

        return True

    def track_events(self, distinct_id, event: str, properties: dict):

        mp: Mixpanel = self.gravity()

        mp.track(distinct_id, event, properties)

        return True

    def create_alias(self, distinct_id, new_id):
        mp: Mixpanel = self.gravity()
        mp.alias(new_id, distinct_id)

        return True

    # def merge_alias(self, distinct_id, distinct_id_):

    #     mp: Mixpanel = self.gravity()
    #     mp.merge(
    #         "89675d90ffe325c2a33f67764d404395",
    #         distinct_id1=distinct_id,
    #         distinct_id2=distinct_id_,
    #     )

    #     return True

    def people_prop(self, distinct_id: any, data):

        mp: Mixpanel = self.gravity()

        mixer_data = {}
        mixer_data["$first_name"] = data.first_name
        mixer_data["$last_name"] = data.last_name
        mixer_data["$email"] = data.email
        mixer_data["$phone_number"] = data.phone_number

        if data.extra_props:
            mixer_data.update(data.extra_props)

        mp.people_set(distinct_id, mixer_data, meta={"$ignor_time": True, "$ip": 0})

        return True

    def people_set_(self, distinct_id: any, data: dict):

        mp: Mixpanel = self.gravity()

        mp.people_set_once(distinct_id, data)

        return True

    def increment_people(self, distinct_id, data: dict):

        mp: Mixpanel = self.gravity()

        mp.people_increment(distinct_id, data)
        return True

    def append_to_people(self, distinct_id, data: dict):

        mp: Mixpanel = self.gravity()

        mp.people_append(distinct_id, data)

        return True

    def union_people(self, distinct_id, data: dict):

        mp: Mixpanel = self.gravity()

        mp.people_union(distinct_id, data)

        return True

    def unset_people(self, distinct_id, data: dict):

        mp: Mixpanel = self.gravity()

        mp.people_unset(distinct_id, data)

        return True

    def remove_people_prop(self, distinct_id, data: dict):

        mp: Mixpanel = self.gravity()

        mp.people_remove(distinct_id, data)

        return True

    def delete_people(self, distinct_id):

        mp: Mixpanel = self.gravity()

        mp.people_delete(distinct_id)

        return True

    def charge_people(self, distinct_id, amount: float, data: dict | None):

        mp: Mixpanel = self.gravity()

        if data:
            mp.people_track_charge(distinct_id, amount, data)
        else:
            mp.people_track_charge(distinct_id, amount)

        return True

    def clear_people_charge(self, distinct_id):
        mp: Mixpanel = self.gravity()

        mp.people_clear_charges(distinct_id)

        return True

    def set_group(self, group_key: str, group_id: str, data: dict):

        mp: Mixpanel = self.gravity()

        mp.group_set(group_key, group_id, data)

        return True

    def set_group_(self, group_key: str, group_id: str, data: dict):

        mp: Mixpanel = self.gravity()

        mp.group_set_once(group_key, group_id, data)

        return True

    def union_group(self, group_key: str, group_id: str, data: dict):

        mp: Mixpanel = self.gravity()

        mp.group_union(group_key, group_id, data)

        return True

    def unset_group(self, group_key: str, group_id: str, data):

        mp: Mixpanel = self.gravity()

        mp.group_unset(group_key, group_id, data)

        return True

    def remove_group(self, group_key: str, group_id: str, data: dict):

        mp: Mixpanel = self.gravity()

        mp.group_remove(group_key, group_id, data)

        return True

    def delete_group(self, group_key: str, group_id: str):

        mp: Mixpanel = self.gravity()

        mp.group_delete(group_key, group_id)

        return True

    # def update_groups(self, message: str):

    #     mp: Mixpanel = self.gravity()
    #     print(message)
    #     mp.group_update(message=message)

    #     return True
