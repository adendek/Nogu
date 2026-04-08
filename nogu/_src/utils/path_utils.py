import os
from pathlib import Path

from loguru import logger


def find_project_root() -> Path:
    """Recursively search for the project's root directory identified by a 'writeoff' directory.

    Starts from the given directory and moves up the directory tree until it finds a
    directory containing a 'writeoff' folder, indicating the root of a Git repository. If
    such a directory is not found before reaching the top of the directory tree, empty path
    is returned.

    Returns:
    Path : The path to the project's root directory if found; otherwise, empty path.

    Example:
    >>> find_project_root()
    Path('/Users/gnnvb/Documents/projects/nogu')

    Note:
        The original implementation was inspired by a solution found at https://stackoverflow.com/a/78142023/1877600,
        which searched for a.git folder.
        However, as discussed in https://github.com/bayer-int/HawkAI/pull/154#discussion_r1683968169,
        the .git folder may not always be present, especially in cases where the code is obtained from a package manager
        similar to PyPI. To ensure compatibility with future scenarios,
        the decision was made to search for a `hawkai` folder instead.
    """

    def do_find_project_root(current_dir: Path):
        if os.path.exists(os.path.join(current_dir, "nogu")):
            logger.debug(f"Found project root: {current_dir}")
            return current_dir
        else:
            # Move up one directory level
            current_dir = current_dir.parent
            # If the current directory is at a top-level, return None
            if len(current_dir.parents) < 2:
                logger.warning(
                    "Project root directory was not at a top-level. Returning empty"
                    " path."
                )
                return Path()
            return do_find_project_root(current_dir)

    return do_find_project_root(Path(__file__))


if __name__ == "__main__":
    inventory_query_path = find_project_root() / "_src/etl/sql/extract_inventory.sql"
    print(inventory_query_path)
