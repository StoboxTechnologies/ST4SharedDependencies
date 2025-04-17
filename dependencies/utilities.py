import toml

from dependencies.settings.conf import Env
from dependencies.settings.conf import settings


def get_version_and_project_name(file_path: str) -> tuple[str, str]:
    if settings.ENV == Env.TESTING:
        return '0.0.0', 'stobox_dependencies'

    with open(file_path, 'r') as file:
        data = toml.load(file)
    version = data['tool']['poetry']['version']
    project_name = data['tool']['poetry']['name']
    return version, project_name
