import subprocess


def execute_kubectl_command(command: str) -> tuple[int, str, str]:
    """Executes a kubectl command string and returns (code, stdout, stderr)."""
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)
