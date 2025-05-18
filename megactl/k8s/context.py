import subprocess


def get_kube_contexts() -> list[str]:
    """Returns a list of available kube contexts."""
    try:
        output = subprocess.check_output(
            ["kubectl", "config", "get-contexts", "--output=name"],
            text=True
        )
        return output.strip().splitlines()
    except Exception:
        return []
