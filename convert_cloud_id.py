import argparse
import base64
import re

def decode_and_modify(data):
    # Decode the base64 data
    decoded_data = base64.b64decode(data).decode('utf-8')
    
    # Verify the format <fqdn>:443<code>
    if not re.match(r'^[^:]+:443[^:]*$', decoded_data):
        raise ValueError('The decoded data is not in the expected format "<fqdn>:443<code>"')
    
    # Remove the ':443' portion from the decoded data
    modified_data = decoded_data.replace(':443', '')
    
    return modified_data

def encode_and_format(name, modified_data):
    # Base64 encode the modified data
    encoded_data = base64.b64encode(modified_data.encode('utf-8')).decode('utf-8')
    
    # Return the data in the original format "<name>:<base64_encoded_string>"
    return f"{name}:{encoded_data}"

def main():
    parser = argparse.ArgumentParser(description='Process a cloud ID.')
    parser.add_argument('-c', '--cloud-id', required=True, help='The cloud ID in the format "<name>:<base64_encoded_data>"')
    
    args = parser.parse_args()
    
    # Split the cloud_id into name and data
    try:
        name, data = args.cloud_id.split(':')
    except ValueError:
        print("The cloud ID must be in the format '<name>:<base64_encoded_data>'.")
        return

    try:
        # Decode and modify the data
        modified_data = decode_and_modify(data)
        
        # Encode and format the modified data
        result = encode_and_format(name, modified_data)
        
        print(f"Modified cloud ID: {result}")
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()

