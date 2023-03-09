from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseUpload


def create_drive_folder(driveApiKey, parent_folder_id, floder_name):
    CLIENT_SECRETS_FILE = 'src/data/drive_oath_key.json'
    scopes = ['https://www.googleapis.com/auth/drive']
    # Create the flow object
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)

    # Run the flow and get the credentials
    credentials = flow.run_local_server(port=0)
    try:
        # create drive api client
        service = build('drive', 'v3',  credentials=credentials)
        folder_metadata = {
            'name': floder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }

        # pylint: disable=maybe-no-member
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(F'Folder: "{folder}".')
        print(F'Folder ID: "{folder.get("id")}".')
        return folder.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def create_drive_file(driveApiKey, folder_id, file_name, file_content):
    CLIENT_SECRETS_FILE = 'src/data/drive_oath_key.json'
    scopes = ['https://www.googleapis.com/auth/drive']
    # Create the flow object

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
    print("stop")
    # Run the flow and get the credentials
    # TODO: run it when the application is initializing, and use everywhere
    credentials = flow.run_local_server(port=0)


    try:
        # create drive api client
        service = build('drive', 'v3',  credentials=credentials)
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        file_content_encoded = io.BytesIO(file_content.encode())

        # pylint: disable=maybe-no-member
        media = MediaIoBaseUpload(file_content_encoded, mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None