from bas_server.services import create_drive_folder, create_drive_file, update_clickup_task_drive_id_field,\
    get_clickup_task_details,anthentifiate_google_cloud
from bas_server.data_layer import ConfigurationFactory
from bas_server.credential_store import CredentialStoreFactory

 # load the configuration of the application
configuration_repository = ConfigurationFactory.get_instance()

clickup_api_key = configuration_repository.get("credentials").get("clickup_api_key")
google_key_file = configuration_repository.get("credentials").get("google_key_file")


# Initialize the Application

# Authentificate to google cloud
google_credentials = anthentifiate_google_cloud(google_key_file)
CredentialStoreFactory.initialize(clickup_api_key, google_credentials)

# _____________  Test Drive Functions _____________

def test_create_drive_folder(google_credentials):
    folder_drive_location_id = \
        configuration_repository.get("drive").get("folder_drive_location_id")
    task_name = "BAS - Test"
    create_drive_folder(google_credentials,folder_drive_location_id, task_name)


def test_create_drive_file(google_credentials):
    folder_id = "124igQIb9ENgiuxAxHOGo1RfSek7VPM1a"
    file_name = "file test"
    file_content = "file Content"
    create_drive_file(folder_id, file_name, file_content)


# _____________ Test Clickup Functions _____________

def test_get_clickup_task_details(clickup_api_key):
    team_id = configuration_repository.get("clickup").get("team_id")
    task_id = "860q5mz3w"
    task = get_clickup_task_details(clickup_api_key, team_id, task_id)
    print(f"Task name is: '{task['name']}' ")
    print(f"custom field: '{task['custom_fields']}' ")


def test_update_clickup_task_drive_id_field(clickup_api_key):
    team_id = configuration_repository.get("clickup").get("team_id")
    task_id = '860q5mz3w'
    folder_id = "1BH1rXhPqmOtIZTtiKk9XNNeHYI1-67w1 - 2"
    field_id = "8e669106-cbe8-41a2-bff8-da08b7ccbda1"
    update_clickup_task_drive_id_field(clickup_api_key, team_id, task_id, field_id, folder_id)

# _____________ Test Automation Process _____________ 

def test_clickup_post(clickup_api_key,google_credentials):
    task_id = "860q5z2tx"

    template_files = configuration_repository.get("drive").get("TEMPLATE_CONTENT_FILE")
    field_id = configuration_repository.get("clickup").get("custom_field_id")
    folder_drive_location_id = configuration_repository.get("drive").get("folder_drive_location_id")
    team_id = configuration_repository.get("clickup").get("team_id")

    task = get_clickup_task_details(clickup_api_key,team_id, task_id)
    task_name = task["name"]
    folder_id = create_drive_folder(google_credentials, folder_drive_location_id, task_name)

    update_clickup_task_drive_id_field(clickup_api_key, team_id, task_id, field_id, folder_id)
    for file_info in template_files:
        create_drive_file(google_credentials,folder_id, file_info["name"],file_info["content"])



def run_test(lickup_api_key):
    test_clickup_post(clickup_api_key,google_credentials)


run_test(clickup_api_key)
