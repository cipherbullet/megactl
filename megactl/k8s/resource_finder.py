import subprocess


def get_resource_names(kind: str, namespace: str = "default") -> list[str]:
    """List resource names of a given kind and namespace using kubectl."""
    try:
        result = subprocess.check_output(
            ["kubectl", "get", kind, "-n", namespace, "-o", "jsonpath={.items[*].metadata.name}"],
            text=True
        )
        return result.strip().split()
    except Exception:
        return []
