# -*- coding:utf-8 -*-

import subprocess


def get_latest_git_tag():
    try:
        # Run the git command to get the latest tag
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # If the command is successful, return the tag
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Git error: {result.stderr.strip()}")

    except FileNotFoundError:
        raise Exception("Git is not installed or not available in the system PATH.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


__version__ = str(get_latest_git_tag())
