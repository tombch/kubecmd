import logging
import argparse
from kubernetes import client, config
from importlib.metadata import version
from . import api

# Set up logging
logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.INFO,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--docker-container",
        type=str,
        required=True,
        help="The name of the Docker container to be used",
    )
    parser.add_argument(
        "-c",
        "--command",
        type=str,
        required=True,
        help="The command to be executed",
    )
    args = parser.parse_args()

    logging.info(f"kubecmd v{version('kubecmd')}")
    logging.info(f"Container: {args.docker_container}")
    logging.info(f"Command: {args.command}")

    # Load config and create a Kubernetes client
    config.load_incluster_config()
    batch_v1 = client.BatchV1Api()

    # Create a job ID and object
    job_id = api.create_job_id()
    job_object = api.create_job_object(
        job_id=job_id,
        image=args.docker_container,
        args=api.create_args(args.command),
    )

    # Submit the job to the cluster
    api.create_job(api_instance=batch_v1, job=job_object)
    logging.info("Job created successfully.")
    logging.info(f"Job ID: {job_id}")


if __name__ == "__main__":
    main()
