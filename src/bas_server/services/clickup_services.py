import requests
import json




def update_clickup_task_drive_id_field(clickupApiKey,team_id, task_id, field_id, folder_id):
    url = "https://api.clickup.com/api/v2/task/" + task_id + "/field/" + field_id
    query = {
    "custom_task_ids": "true",
    "team_id": team_id
    }

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": clickupApiKey
    }

    payload = {
    "value": folder_id
    }

    response = requests.post(url, json=payload, headers=HEADERS, params=query)

    data = response.json()
    print(data)
    return True


def get_clickup_task_details(clickupApiKey, team_id, task_id):
    url = "https://api.clickup.com/api/v2/task/" + task_id

    query = {
    "custom_task_ids": "true",
    "team_id": team_id,
    "include_subtasks": "flase"
    }

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": clickupApiKey
    }
    response = requests.get(url, headers=HEADERS, params=query)

    data = response.json()
    print(data)
    return data