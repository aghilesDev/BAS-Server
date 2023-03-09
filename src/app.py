from flask import Flask
from flask import request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseUpload

from bas_server.services import create_drive_folder, create_drive_file, update_clickup_task_drive_id_field,\
    get_clickup_task_details, anthentifiate_google_cloud
from bas_server.data_layer import ConfigurationFactory
from bas_server.credential_store import CredentialStoreFactory


app = Flask(__name__)


def initialize_application():
    # load the configuration of the application
    configuration_repository = ConfigurationFactory.get_instance()
    # Authentificate to google cloud
    google_key_file = configuration_repository.get("credentials").get("google_key_file")
    google_credentials = anthentifiate_google_cloud(google_key_file)
    # store the credentials of APIs in the credential store
    clickup_api_key = configuration_repository.get("credentials").get("clickup_api_key") 
    CredentialStoreFactory.initialize(clickup_api_key, google_credentials)

initialize_application()

@app.route('/webhook/clickupPostCreated', methods=['POST'])
def post_clickup_post():
    data = request.get_json( )
    task_id = data['task_id']
    # load parameters from configuration
    configuration_repository = ConfigurationFactory.get_instance()
    template_files = configuration_repository.get("drive").get("TEMPLATE_CONTENT_FILE")
    field_id = configuration_repository.get("clickup").get("custom_field_id")
    folder_drive_location_id = configuration_repository.get("drive").get("folder_drive_location_id")
    team_id = configuration_repository.get("clickup").get("team_id")
    # get credentials from credential store
    credential_store = CredentialStoreFactory.get_instance()
    clickup_api_key = credential_store.clickup_api_key
    google_credentials = credential_store.google_credentials
    # retrive name using clickup api
    task = get_clickup_task_details(clickup_api_key,team_id, task_id)
    task_name = task["name"]
    # create folder in google drive using the task name retrived
    folder_id = create_drive_folder(google_credentials, folder_drive_location_id, task_name)
    # store the created folder id in the clickup task
    update_clickup_task_drive_id_field(clickup_api_key, team_id, task_id, field_id, folder_id)
    # create files in the new folder folowing the template given in the configuration
    for file_info in template_files:
        create_drive_file(google_credentials, folder_id, file_info["name"],file_info["content"])
    # respond to the request
    response = {'status': 'success', 'message': 'Data received'}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
