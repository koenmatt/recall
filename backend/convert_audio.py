import base64




def convert_file():

    # Path to your MP3 file
    file_path = '/Users/matthewkoen/Documents/recall/backend/I5olJSia.mp3'

    # Read the binary data from the file
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Encode the binary data to Base64
    base64_encoded_data = base64.b64encode(binary_data)

    # Convert the Base64 bytes to a string
    base64_string = base64_encoded_data.decode('utf-8')

    return base64_string