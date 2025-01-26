from __future__ import annotations
from collections.abc import Iterable
import os
from typing import IO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

connection_string: str | None = os.getenv("AzureWebJobsStorage")
container_name: str = "your_container_name"

def upsert_blob(
    version: str,
    revision: str,
    data: str | bytes | Iterable[bytes] | IO[bytes]
) -> None:
    # Validate environment variable
    if connection_string is None:
        raise ValueError("AzureWebJobsStorage environment variable not set")
    
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(connection_string)
    container_client: ContainerClient = blob_service_client.get_container_client(container_name)
    
    blob_name: str = f"{version}_{revision}.json"
    blob_client: BlobClient = container_client.get_blob_client(blob_name)
    
    blob_client.upload_blob(data, overwrite=True)
    print(f"Blob '{blob_name}' uploaded successfully.")
