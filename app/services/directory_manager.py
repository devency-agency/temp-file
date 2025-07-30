from flask import current_app
import os
import time
import threading
from datetime import datetime, timedelta
from ..services.log_handler import setup_logging
from typing import Optional

logger = setup_logging()

class DirectoryManager:
    """
    Manages the periodic cleanup of old folders in a specified directory.

    Args:
        folder_path (str): The root directory to monitor and clean.
        interval (int): Time interval (in seconds) between cleanups. Default is 3600 (1 hour).
        lifetime (int): Folder lifetime (in seconds) before deletion. Default is 86400 (24 hours).
    """
    def __init__(self, folder_path: str, interval: int = 3600, lifetime: int = 86400) -> None:
        self.folder_path = folder_path
        self.interval = interval
        self.lifetime = lifetime
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        """Starts the background thread that performs folder cleanup."""
        self.thread.start()

    def _run(self) -> None:
        """Continuously cleans old folders at specified intervals."""
        while True:
            self._clean_old_folders()
            time.sleep(self.interval)

    def _clean_old_folders(self) -> None:
        """
        Deletes folders older than the configured lifetime.
        Logs and handles any errors during deletion.
        """
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.lifetime)

        # Cleans old folders (hidden)

    def _delete_folder(self, folder_path: str) -> None:
        """
        Deletes the contents of a folder and the folder itself.

        Args:
            folder_path (str): The path of the folder to delete.
        """
        try:

            # Deleting the folder (hidden)
            logger.info(f"Successfully deleted folder: {folder_path} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            logger.error(f"Failed to delete folder {folder_path}: {e}")
