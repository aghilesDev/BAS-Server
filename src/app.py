import requests
from flask import Flask
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseUpload

from data_layer import ConfigurationFactory


app = Flask(__name__)

configuration_repository = ConfigurationFactory.get_instance()

clickup_api_key = configuration_repository.get("credentials").get("clickup_api_key")
drive_api_key = configuration_repository.get("credentials").get("drive_api_key")

folder_drive_location_id = configuration_repository.get("drive").get("folder_drive_location_id")
TEMPLATE_FILES = configuration_repository.get("drive").get("TEMPLATE_CONTENT_FILE")

team_id = configuration_repository.get("clickup").get("team_id")
space_id = configuration_repository.get("clickup").get("space_id")
clickup_folder_id = configuration_repository.get("clickup").get("folder_id")
list_id = configuration_repository.get("clickup").get("content_list_id")

clickupEvents = configuration_repository.get("clickup").get("content_clickupEvents")



@app.route('/webhook/clickupPostCreated', methods=['POST'])
def post_clickup_post():
    data = request.json()
    task_id = data['task_id']
    task = get_clickup_task_details(clickup_api_key,team_id, task_id)
    task_name = task["name"]
    folder_id = create_drive_folder(drive_api_key, folder_drive_location_id, task_name)

    update_clickup_task_drive_id_field(clickup_api_key, task_id, folder_id)
    for file_info in TEMPLATE_FILES:
        create_drive_file(drive_api_key, folder_id, file_info["name"],file_info["content"])

    response = {'status': 'success', 'message': 'Data received'}
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response)

# Click up methods
def update_clickup_task_drive_id_field(clickup_api_key,team_id, task_id, folder_id):
    pass


def get_clickup_task_details(clickup_api_key, team_id, task_id):
    url = "https://api.clickup.com/api/v2/task/" + task_id

    query = {
    "custom_task_ids": "true",
    "team_id": team_id,
    "include_subtasks": "flase"
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": clickup_api_key
    }

    response = requests.get(url, headers=headers, params=query)

    data = response.json()
    print(data)
    return data


# Drive methods 
def create_drive_folder(drive_api_key, parent_folder_id, floder_name):
    credentials = service_account.Credentials.from_service_account_info(
        {'api_key': {'api_key': drive_api_key}}
        )
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=credentials)
        folder_metadata = {
            'name': floder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }

        # pylint: disable=maybe-no-member
        folder = service.files().create(body=folder_metadata, fields='id'
                                      ).execute()
        print(F'Folder ID: "{folder.get("id")}".')
        return folder.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def create_drive_file(drive_api_key, folder_id, file_name,file_content):
    credentials = service_account.Credentials.from_service_account_info(
        {'api_key': {'api_key': drive_api_key}}
        )
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=credentials)
        file_metadata = {
            'name': floder_name,
            'parents': [folder_id]
        }
        file_content_encoded = io.BytesIO(FILE_CONTENT.encode())

        # pylint: disable=maybe-no-member
        media = MediaIoBaseUpload(file_content_encoded, mimetype='text/plain')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


if __name__ == '__main__':
    app.run(debug=True)
