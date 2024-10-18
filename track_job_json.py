import json

def update_job_json(file_path, job_data):
    # Read the existing JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Unpack the list into respective values for the 4 keys
    job_title, job_type, application_status, job_link = job_data

    # Append the new data to the respective lists
    data["Job Title"].append(job_title)
    data["Job Type"].append(job_type)
    data["Application Status"].append(application_status)
    data["Job Link"].append(job_link)

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
