
from google.cloud import storage

def initialise_gcp():
    try:
        client = storage.Client()
        bucket = client.bucket('text2epub-storage')
        return client, bucket
    except Exception as e:
        raise e

def retrieve_file(file_name, bucket):
    try:
        blob = bucket.blob(f'input/{file_name}')
        file_bytes = blob.download_as_bytes()
        print(f"File {file_name} downloaded to memory")
        return file_bytes
    except Exception as e:
        raise e

def upload_file(file_name, file_path, bucket):
    try:
        blob = bucket.blob(f'input/{file_name}')
        blob.upload_from_filename(file_path)
        print(f"File {file_name} uploaded from {file_path} to blob storage")
    except Exception as e:
        raise e
    
