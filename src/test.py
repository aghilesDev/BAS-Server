from bas_server.services import create_drive_folder, create_drive_file, update_clickup_task_drive_id_field,\
    get_clickup_task_details
from bas_server.data_layer import ConfigurationFactory

configuration_repository = ConfigurationFactory.get_instance()

clickup_api_key = configuration_repository.get("credentials").get("clickup_api_key")
drive_api_key = configuration_repository.get("credentials").get("drive_api_key")


# _____________  Test Drive Functions _____________

def test_create_drive_folder(drive_api_key):
    folder_drive_location_id = \
        configuration_repository.get("drive").get("folder_drive_location_id")
    task_name = "BAS - Test"
    create_drive_folder(drive_api_key, folder_drive_location_id, task_name)


def test_create_drive_file(drive_api_key):
    folder_id = "124igQIb9ENgiuxAxHOGo1RfSek7VPM1a"
    file_name = "file test"
    file_content = "file Content"
    create_drive_file(drive_api_key, folder_id, file_name, file_content)


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
    folder_id = "1BH1rXhPqmOtIZTtiKk9XNNeHYI1-67w1 - Test2"
    field_id = "8e669106-cbe8-41a2-bff8-da08b7ccbda1"
    update_clickup_task_drive_id_field(clickup_api_key, team_id, task_id, field_id, folder_id)

# _____________ Test Automation Process _____________ 

def test_clickup_post(drive_api_key, clickup_api_key):
    task_id = 0
    task = get_clickup_task_details(clickup_api_key,team_id, task_id)
    task_name = task["name"]
    folder_id = create_drive_folder(drive_api_key, folder_drive_location_id, task_name)

    update_clickup_task_drive_id_field(clickup_api_key, task_id, folder_id)
    for file_info in TEMPLATE_FILES:
        create_drive_file(drive_api_key, folder_id, file_info["name"],file_info["content"])

    response = {'status': 'success', 'message': 'Data received'}
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response)


def run_test(drive_api_key, clickup_api_key):
    test_create_drive_file(drive_api_key)


run_test(drive_api_key, clickup_api_key)
