import os


class PathManager:
    """Manage files and directories within a specified path"""

    def __init__(self, path: str):
        self.path = path

    def _get_path_to_modification_time(self, is_directory=False):
        """Returns a dictionary containing the relative paths and modification times of files or directories within the specified path"""
        path_to_modification_time = {}

        for root, directories, files in os.walk(self.path):
            paths = directories if is_directory else files

            for path in paths:
                full_path = os.path.join(root, path)
                relative_path = os.path.relpath(full_path, self.path)

                modification_time = os.path.getmtime(full_path)
                path_to_modification_time[relative_path] = modification_time

        return path_to_modification_time

    def get_file_to_modification_time(self):
        """Returns a dictionary containing the relative paths and modification times of files within the specified path"""

        return self._get_path_to_modification_time()

    def get_directory_to_modification_time(self):
        """Returns a dictionary containing the relative paths and modification times of directories within the specified path"""

        return self._get_path_to_modification_time(is_directory=True)
