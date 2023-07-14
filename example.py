from prefect import flow, task, get_run_logger
from prefect.deployments import Deployment
import httpx


@task(retries=3)
def get_stars(repo: str) -> int:
    url = f"https://api.github.com/repos/{repo}"
    count = httpx.get(url).json()["stargazers_count"]
    return count


@flow(name="GitHub Stars")
def github_stars():
    repo = "thatdevsherry/historia"
    logger = get_run_logger()
    result = get_stars(repo)
    logger.info(f"{repo} has {result} stars")


deployment = Deployment.build_from_flow(
    flow=github_stars,
    name="example-deployment",
    version=1,
    work_queue_name="demo",
    work_pool_name="default-agent-pool",
)
deployment.apply()
