import uuid
from kubernetes import client


def create_job_id() -> str:
    """
    Create a kubecmd job ID.
    """

    return f"kubecmd-{uuid.uuid4()}"


def create_args(command: str) -> list[str]:
    """
    Convert command string into a list of args.
    """

    return [x for x in command.split(" ") if x]


def create_job_object(job_id: str, image: str, args: list[str]) -> client.V1Job:
    """
    Create a Kubernetes job object.
    """

    # Create a container
    container = client.V1Container(
        name=job_id,
        image=image,
        args=args,
        resources=client.V1ResourceRequirements(
            requests={"cpu": "1", "memory": "200Mi"},
            limits={"cpu": "1", "memory": "200Mi"},
        ),
    )

    # Create a spec template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "kubecmd"}),
        spec=client.V1PodSpec(
            security_context=client.V1PodSecurityContext(
                run_as_non_root=True,
                run_as_user=1000,
                run_as_group=1000,
                fs_group=1000,
            ),
            restart_policy="Never",
            node_selector={"hub.jupyter.org/node-purpose": "user"},
            containers=[container],
        ),
    )

    # Create the job specification
    spec = client.V1JobSpec(
        ttl_seconds_after_finished=120,
        backoff_limit=5,
        template=template,
    )

    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_id),
        spec=spec,
    )

    return job


def create_job(api_instance: client.BatchV1Api, job: client.V1Job) -> None:
    """
    Create a Kubernetes job.
    """

    api_instance.create_namespaced_job(
        body=job,
        namespace="default",
    )
