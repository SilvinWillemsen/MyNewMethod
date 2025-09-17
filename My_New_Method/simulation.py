import json
import time


def check_should_cancel(json_file_path_in):
    try:
        if json_file_path_in is not None:
            with open(json_file_path_in, 'r') as json_file_to_check:
                data = json.load(json_file_to_check)

        # Update the specified field value
        if 'should_cancel' in data:
            return data['should_cancel']

    except Exception as e:
        print("check_should_cancel returned: " + str(e))

def simulation_method (json_file_path=None):

    result_container = {}
    with open(json_file_path, 'r') as json_file:
        result_container = json.load(json_file)

    # Example on how to extract simulation-specific settings from the .json
    simulation_settings = result_container["simulationSettings"]
    
    simulation_setting_1 = simulation_settings["mnm_1"]
    simulation_setting_2 = simulation_settings["mnm_2"]
    print(f"Simulation setting 1 = {simulation_setting_1}")
    print(f"Simulation setting 2 = {simulation_setting_2}")

    # Main simulation loop
    prev_percent_done = 0
    simulation_length = 150
    for i in range(simulation_length):
        percent_done = round(i * 100 / simulation_length)
        if result_container:
            if percent_done > prev_percent_done:
                # Checking whether the user has cancelled the simulation (only one time per percentage increase)
                if check_should_cancel(json_file_path):
                    print("breaking out loop")
                    break

                if result_container:
                    print(percent_done) # Print to the (Celery) log

                    # Write to the json file to visualise in the front-end
                    result_container['results'][0]['percentage'] = percent_done
                    with open(json_file_path, 'w') as percentage_update:
                        percentage_update.write(
                            json.dumps(result_container, indent=4)
                        )

        time.sleep (0.01)