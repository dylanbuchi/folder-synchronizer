import logging
import os
import sys
import time
from argparse import Namespace

from watchdog.observers import Observer

from constants.constants import LOG_DATE_FORMAT, LOG_FORMAT, ONE_MINUTE
from modules.folder_synchronizer.argument_parser import FolderSynchronizerArgumentParser
from modules.folder_synchronizer.event_handler import FolderSynchronizerEventHandler
from modules.folder_synchronizer.folder_synchronizer import FolderSynchronizer
from modules.folder_synchronizer.logger import FolderSynchronizerLogger
from modules.path_manager.path_manager import PathManager


def create_default_folders_for_sync(folder_sync_args: Namespace):
    """Create the source and replica folders if user does not provide folders arguments"""

    for path in (folder_sync_args.source, folder_sync_args.replica):
        if not os.path.exists(path):
            os.mkdir(path)


def main():
    """Main function for the folder synchronizer program"""

    folder_sync_args = FolderSynchronizerArgumentParser().parse_args()

    logging.basicConfig(
        filename=folder_sync_args.log,
        level=logging.INFO,
        datefmt=LOG_DATE_FORMAT,
        format=LOG_FORMAT,
    )

    create_default_folders_for_sync(folder_sync_args)

    source_path_manager = PathManager(folder_sync_args.source)
    replica_path_manager = PathManager(folder_sync_args.replica)

    folder_sync = FolderSynchronizer(
        source_path_manager,
        replica_path_manager,
    )

    folder_sync_event_handler = FolderSynchronizerEventHandler(
        FolderSynchronizerLogger()
    )

    observer = Observer()
    observer.schedule(
        folder_sync_event_handler, folder_sync_args.source, recursive=True
    )
    observer.start()

    sync_interval = ONE_MINUTE * folder_sync_args.sync_interval

    try:
        while True:
            folder_sync.run()
            time.sleep(sync_interval)

    except KeyboardInterrupt:
        print("Exiting program")
        observer.stop()
        sys.exit()

    except (FileNotFoundError, Exception) as error:
        print(error)

    observer.join()


if __name__ == "__main__":
    main()
