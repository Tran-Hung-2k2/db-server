import requests
import json


def submit_job_to_livy(livy_url, job_file_path, job_args=None):
    """
    Submit a job to a Spark cluster using Livy.

    Args:
    - livy_url (str): The URL of the Livy server.
    - job_file_path (str): The local file path of the Spark job script to submit.
    - job_args (list, optional): Arguments to pass to the Spark job script.

    Returns:
    - dict: JSON response containing information about the submitted job.
    """
    # Prepare the job submission request data
    data = {
        "file": "local://"
        + job_file_path  # Prefix with "file://" to indicate local file path
    }
    if job_args:
        data["args"] = job_args

    # Send the job submission request to Livy
    response = requests.post(
        f"{livy_url}/batches", json=data, headers={"Content-Type": "application/json"}
    )

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to submit job. Status code:", response.status_code)
        print("Response:", response.text)
        return None

    # Parse and return the response
    return json.loads(response.text)


if __name__ == "__main__":
    # Livy server URL
    livy_url = "http://localhost:8089"  # Replace with your Livy server URL

    # Path to the Spark job script
    job_file_path = "/home/duonghdt/Desktop/Python/db-server/services_python/livy_service/simple_job.py"

    # Arguments for the Spark job (optional)
    job_args = ["arg1", "arg2"]  # Replace with your job arguments if any

    # Submit the job to Livy
    job_response = submit_job_to_livy(livy_url, job_file_path, job_args)

    # Check if the job submission was successful
    print(job_response)
