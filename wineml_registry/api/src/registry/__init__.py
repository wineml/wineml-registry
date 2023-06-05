import os


def registry_type_resolver():
    """
    Check whether registry is Azure, AWS or GCP
    """

    if os.environ.get("AWS_ACCESS_KEY_ID"):
        return "aws"
    elif os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
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

    registry_type = registry_type_resolver()

    # if registry_type == 'aws':
    #     from .aws import AWSRegistryController
    #     return AWSRegistryController(
    #         aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    #         aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    #         bucket_name=os.environ.get('BUCKET_NAME'))
    # elif registry_type == 'gcp':
    #     from .gcp import GCPRegistryController
    #     return GCPRegistryController(
    #         credentials=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
    #         bucket_name=os.environ.get('BUCKET_NAME'))
    if registry_type == "azure":
        from .azure import AzureRegistryController

        return AzureRegistryController(
            connection_string=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
            container_name=os.environ.get("AZURE_STORAGE_CONTAINER_NAME"),
        )
    else:
        raise Exception("No registry type found")


registry_client = initiate_registry()
