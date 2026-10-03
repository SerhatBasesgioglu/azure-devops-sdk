import os

from dotenv import load_dotenv

from .client import AdoClient


def main() -> None:
    load_dotenv()
    url = os.environ["ADO_URL"]
    org = os.environ["ADO_ORG"]
    pat = os.environ["ADO_PAT"]
    base_url = f"{url}/{org}"
    client = AdoClient(base_url=base_url, pat=pat)

    try:
        for project in client.list_projects():
            print(project.name)
            for repo in client.list_repositories(project.id):
                print(repo.name)
    finally:
        client.close()
