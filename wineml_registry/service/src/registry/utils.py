import os


def remove_file(path: str) -> None:
    os.unlink(path)


def resolve_model_version(model_version: str):
    # TODO: check if version naming convention is valid
    return model_version.replace(".", "_")


def resolve_artifact_path(
    namespace: str,
    model_name: str,
    model_version: str,
):
    return os.path.join(
        namespace,
        model_name,
        resolve_model_version(model_version),
    )