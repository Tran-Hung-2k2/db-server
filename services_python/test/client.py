import requests

# Set the URL for the localhost server
url = 'http://localhost:7879/upload'

# Set the file path of the file you want to upload
file_path = 'dataset_200mb.csv'

# Additional data to include in the POST body
additional_data = {
    'user_id': 'duonghdt'
}

# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Set the files parameter with a tuple containing the filename and the file object
    files = {'file': (file_path, file)}

    # Make the request to upload the file using the POST method and multipart form data
    response = requests.post(url, files=files, data=additional_data)

    # Check the response status code
    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print("Failed to upload file. Status code:", response.status_code)
