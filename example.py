from prefect import flow, task
from typing import List
import httpx
from prefect.deployments import Deployment


@task(retries=3)
def get_stars(repo: str):
    url = f"https://api.github.com/repos/{repo}"
    count = httpx.get(url).json()["stargazers_count"]
    print(f"{repo} has {count} stars!")


@flow(name="GitHub Stars")
def github_stars(repos: List[str]):
    for repo in repos:
        get_stars(repo)


deployment = Deployment.build_from_flow(
    flow=github_stars,
    name="example-deployment",
    version=1,
    work_queue_name="demo",
    work_pool_name="default-agent-pool",
)
deployment.apply()
