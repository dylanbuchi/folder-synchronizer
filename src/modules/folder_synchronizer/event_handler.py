from datetime import datetime, timedelta

from watchdog.events import FileSystemEvent, FileSystemEventHandler

from modules.folder_synchronizer.logger import FolderSynchronizerLogger


class FolderSynchronizerEventHandler(FileSystemEventHandler):
    """Event handler for syncing folders"""

    def __init__(
        self,
        logger: FolderSynchronizerLogger,
    ):
        self.logger = logger
        self.last_updated_event = datetime.now()

    def handle_event(self, event: FileSystemEvent, event_type: str):
        """Handle a file or directory system event"""
        if event.is_directory:
            self.logger.log(f"Directory {event.src_path} has been {event_type}")
        else:
            self.logger.log(f"File {event.src_path} has been {event_type}")

    def on_modified(self, event: FileSystemEvent):
        # check to avoid duplicate updated event logs
        if datetime.now() - self.last_updated_event < timedelta(seconds=1):
            return

        self.last_updated_event = datetime.now()
        self.handle_event(event, "updated")

    def on_created(self, event: FileSystemEvent):
        self.handle_event(event, "created")

    def on_deleted(self, event: FileSystemEvent):
        self.handle_event(event, "deleted")
