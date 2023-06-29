import os


def registry_connector_resolver():
    """
    Check whether registry is Azure, AWS or GCP
    """

    if os.environ.get("AWS_ACCESS_KEY_ID"):
        return "aws"
    elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and (
        os.environ.get("GCP_GCS_BUCKET_NAME")
    ):
        return "gcp"
    elif os.environ.get("AZURE_STORAGE_CONNECTION_STRING") and (
        os.environ.get("AZURE_STORAGE_CONTAINER_NAME")
    ):
        return "azure"
    else:
        raise Exception("No registry type found")


def initiate_registry():
    """
    Initiate registry based on registry type
    """

    registry_connector = registry_connector_resolver()

    if registry_connector == "aws":
        from registry.aws import AWSRegistryController

        return AWSRegistryController(bucket_name=os.environ.get("AWS_S3_BUCKET_NAME"))
    elif registry_connector == "gcp":
        from registry.gcp import GCPRegistryController

        return GCPRegistryController(bucket_name=os.environ.get("GCP_GCS_BUCKET_NAME"))
    elif registry_connector == "azure":
        from registry.azure import AzureRegistryController

        return AzureRegistryController(
            connection_string=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
            container_name=os.environ.get("AZURE_STORAGE_CONTAINER_NAME"),
        )
    else:
        raise Exception("No registry type found")


registry_connector = initiate_registry()
