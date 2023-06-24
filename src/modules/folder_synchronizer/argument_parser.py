import argparse
import os


class FolderSynchronizerArgumentParser:
    """Parse command line arguments for folder synchronization"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Sync two folders one-way: source and replica",
        )

        self.parser.add_argument(
            "--source",
            type=str,
            help="Path to the source folder",
            default=f"{os.getcwd()}/tests/source",
        )
        self.parser.add_argument(
            "--replica",
            type=str,
            help="Path to the replica folder",
            default=f"{os.getcwd()}/tests/replica",
        )
        self.parser.add_argument(
            "--sync_interval",
            type=int,
            help="Interval between syncs in minutes",
            default=1,
        )
        self.parser.add_argument(
            "--log",
            type=str,
            help="Path to the log file",
            default="./folder_synchronizer.log",
        )

    def parse_args(self):
        """Parse command line arguments"""
        return self.parser.parse_args()
