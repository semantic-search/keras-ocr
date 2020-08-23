import os
from azure.storage.blob import BlobServiceClient


def getData(ConnectionString, container_name, blob_name):
    """
    Returns the content of the blob in container.
    """
    blob_service_client = BlobServiceClient.from_connection_string(ConnectionString)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    return blob_client.download_blob().readall()
