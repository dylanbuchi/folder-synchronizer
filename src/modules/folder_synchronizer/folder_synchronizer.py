import os
import shutil
from typing import Callable

from modules.path_manager.path_manager import PathManager


class FolderSynchronizer:
    """A one-way sync process between two folders: source and replica"""

    def __init__(
        self,
        source_path_manager: PathManager,
        replica_path_manager: PathManager,
    ):
        self.source_path_manager = source_path_manager
        self.replica_path_manager = replica_path_manager

    def create_or_update_files_and_directories(self):
        """Creates or updates files and directories in the replica folder to match the source folder"""

        for (
            source_file_path,
            source_modification_time,
        ) in self.source_file_to_modification_time.items():
            source_file = os.path.join(self.source_path_manager.path, source_file_path)
            replica_file = os.path.join(
                self.replica_path_manager.path, source_file_path
            )

            if not os.path.exists(
                replica_file
            ) or source_modification_time > self.replica_file_to_modification_time.get(
                source_file_path, 0
            ):
                os.makedirs(os.path.dirname(replica_file), exist_ok=True)
                shutil.copy2(source_file, replica_file)

    def create_empty_dirs(self):
        """Creates empty directories in the replica folder to match the source folder"""

        for source_directory_path in self.source_directory_to_modification_time:
            source_directory = os.path.join(
                self.source_path_manager.path, source_directory_path
            )
            replica_directory = os.path.join(
                self.replica_path_manager.path, source_directory_path
            )

            if not os.path.exists(replica_directory) and not os.listdir(
                source_directory
            ):
                os.makedirs(replica_directory)

    def delete_items_not_in_source(
        self,
        source_items: dict[str, float],
        replica_items: dict[str, float],
        delete_func: Callable[[str], None],
    ):
        """Deletes items in the replica folder that are not present in the source folder"""

        for item in replica_items:
            if item not in source_items:
                item_to_remove = os.path.join(self.replica_path_manager.path, item)
                delete_func(item_to_remove)

    def delete_directories_not_in_source(self):
        """Deletes directories in the replica folder that are not present in the source folder"""

        self.delete_items_not_in_source(
            self.source_directory_to_modification_time,
            self.replica_directory_to_modification_time,
            shutil.rmtree,
        )

    def delete_files_not_in_source(self):
        """Deletes files in the replica folder that are not present in the source folder"""

        self.delete_items_not_in_source(
            self.source_file_to_modification_time,
            self.replica_file_to_modification_time,
            os.remove,
        )

    def update_source_file_and_directory_times(self):
        """Updates the modification times of files and directories in the source folder"""

        self.source_file_to_modification_time = (
            self.source_path_manager.get_file_to_modification_time()
        )
        self.source_directory_to_modification_time = (
            self.source_path_manager.get_directory_to_modification_time()
        )

    def update_replica_file_and_directory_times(self):
        """Updates the modification times of files and directories in the replica folder"""

        self.replica_file_to_modification_time = (
            self.replica_path_manager.get_file_to_modification_time()
        )
        self.replica_directory_to_modification_time = (
            self.replica_path_manager.get_directory_to_modification_time()
        )

    def run(self):
        """Runs the synchronization process between the source and replica folders"""

        self.update_source_file_and_directory_times()
        self.update_replica_file_and_directory_times()

        self.create_or_update_files_and_directories()
        self.create_empty_dirs()

        self.delete_files_not_in_source()
        self.delete_directories_not_in_source()
