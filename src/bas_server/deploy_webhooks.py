import requests

configuration_repository = ConfigurationFactory.get_instance()

clickupApiKey = configuration_repository.get("credentials").get("clickup_api_key")

team_id = configuration_repository.get("clickup").get("team_id")
space_id = configuration_repository.get("clickup").get("space_id")
clickup_folder_id = configuration_repository.get("clickup").get("folder_id")
list_id = configuration_repository.get("clickup").get("content_list_id")

clickupEvents = configuration_repository.get("clickup").get("content_clickupEvents")



def create_clickup_webhook(clickupApiKey, endpoint, events, teamId, spaceId, folderId, listId):
    url = "https://api.clickup.com/api/v2/team/" + teamId + "/webhook"
    headers = {
    "Content-Type": "application/json",
    "Authorization": clickupApiKey
    }
    payload = {
        "endpoint": "https://automation.aghilesgoumeziane.com/webhook/clickupPostCreated",
        "events": events,
        "space_id": spaceId,
        "folder_id": folderId,
        "list_id": listId
}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    print(data)
    webhookId = data['id']
    return webhookId



create_clickup_webhook(clickupApiKey, endpoint, events, teamId, spaceId, folderId, listId)
