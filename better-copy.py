import subprocess
import click
import sys
import typing as t


def exec_command(command: t.List[str]) -> None:
    """
    Execute a command and stream its output to stdout and stderr.

    :param command: the command to execute
    :type command: List[str]
    """
    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        sys.stdout.write(result.stdout.decode())
        sys.stderr.write(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr.decode())
        sys.exit(e.returncode)


@click.command()
@click.option("-c", "--copy", "action", flag_value="copy", help="Copy files")
@click.option("-m", "--move", "action", flag_value="move", help="Move files")
@click.argument("source")
@click.argument("destination")
def better_copy(action: t.Optional[str], source: str, destination: str) -> None:
    """
    Copy or move files from source to destination with progress information.

    :param action: Action to take, either "copy" or "move"
    :type action: str
    :param source: Source directory or file
    :type source: str
    :param destination: Destination directory or file
    :type destination: str
    """
    if not action:
        click.echo(
            "You must specify whether to copy (--copy or -c) or move (--move or -m)."
        )
        sys.exit(1)

    if action == "copy":
        click.echo(f"Copying from {source} to {destination}...")
        # Use rsync to copy files with progress information
        command = ["rsync", "-avh", "--progress", source, destination]

    elif action == "move":
        click.echo(f"Moving from {source} to {destination}...")
        # Use rsync to move files with progress information
        command = [
            "rsync",
            "-avh",
            "--progress",
            "--remove-source-files",
            source,
            destination,
        ]

    exec_command(command)


if __name__ == "__main__":
    better_copy()
