import subprocess

resource_cache = {
    "pods": [],
    "deployments": [],
    "namespaces": []
}


def fetch_cluster_context() -> None:
    """Refresh cache of pods, deployments, and namespaces using kubectl."""
    for kind in ["pods", "deployments"]:
        try:
            out = subprocess.check_output(
                ["kubectl", "get", kind, "-A", "-o", "jsonpath={.items[*].metadata.name}"],
                text=True
            )
            resource_cache[kind] = out.strip().split()
        except Exception:
            resource_cache[kind] = []

    try:
        out = subprocess.check_output(
            ["kubectl", "get", "namespaces", "-o", "jsonpath={.items[*].metadata.name}"],
            text=True
        )
        resource_cache["namespaces"] = out.strip().split()
    except Exception:
        resource_cache["namespaces"] = []
