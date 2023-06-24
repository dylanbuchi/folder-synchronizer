from watchdog.events import FileSystemEvent, FileSystemEventHandler

from .logger import FolderSynchronizerLogger


class FolderSynchronizerEventHandler(FileSystemEventHandler):
    """Event handler for syncing folders"""

    def __init__(
        self,
        logger: FolderSynchronizerLogger,
    ):
        self.logger = logger

    def handle_event(self, event: FileSystemEvent, event_type: str):
        """Handle a file or directory system event"""
        if event.is_directory:
            self.logger.log(f"Directory {event.src_path} has been {event_type}")
        else:
            self.logger.log(f"File {event.src_path} has been {event_type}")

    def on_modified(self, event: FileSystemEvent):
        self.handle_event(event, "updated")

    def on_created(self, event: FileSystemEvent):
        self.handle_event(event, "created")

    def on_deleted(self, event: FileSystemEvent):
        self.handle_event(event, "deleted")
