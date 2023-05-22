import os
import argparse
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileHandler(FileSystemEventHandler):
    def __init__(self, folder):
        super(FileHandler, self).__init__()
        self.folder = folder

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        extension = Path(file_path).suffix.lower()

        if extension:
            target_folder = self.folder / extension[1:]
        else:
            target_folder = self.folder / "sem_extensao"

        if not target_folder.exists():
            target_folder.mkdir()

        target_file = target_folder / Path(file_path).name
        shutil.move(file_path, target_file)


def create_folders_for_extensions(folder):
    extensions = set()

    for file in folder.iterdir():
        if file.is_file():
            extension = file.suffix.lower()
            extensions.add(extension)

    for extension in extensions:
        target_folder = folder / extension[1:]
        if not target_folder.exists():
            target_folder.mkdir()

    target_folder = folder / "sem_extensao"
    if not target_folder.exists():
        target_folder.mkdir()


def organize_files(folder):
    create_folders_for_extensions(folder)

    for file in folder.iterdir():
        if file.is_file():
            extension = file.suffix.lower()
            if extension:
                target_folder = folder / extension[1:]
            else:
                target_folder = folder / "sem_extensao"
            target_file = target_folder / file.name
            shutil.move(str(file), str(target_file))


def watch_folder(folder):
    event_handler = FileHandler(folder)
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monitor and organize files in a folder based on their extensions."
    )
    parser.add_argument("folder", type=str, help="Folder to monitor")

    args = parser.parse_args()

    folder = Path(args.folder)

    organize_files(folder)
    watch_folder(folder)
