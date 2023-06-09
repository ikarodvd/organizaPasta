import os
import argparse
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def on_created(event, folders):
    if event.is_directory:
        return

    file_path = event.src_path
    extension = Path(file_path).suffix.lower()

    if extension:
        target_folder = find_target_folder(extension[1:], folders)
    else:
        target_folder = find_target_folder("sem_extensao", folders)

    if not target_folder.exists():
        target_folder.mkdir()

    target_file = target_folder / Path(file_path).name

    try:
        shutil.move(file_path, target_file)
        print(f"Arquivo movido com sucesso: {file_path} -> {target_file}")
    except Exception as e:
        print(f"Erro ao mover o arquivo: {file_path} -> {target_file}")
        print(f"Detalhes do erro: {str(e)}")


def find_target_folder(extension, folders):
    for folder in folders:
        target_folder = folder / extension
        if target_folder.exists():
            return target_folder
    return folders[0] / extension


def create_folders_for_extensions(folders):
    extensions = set()

    for folder in folders:
        for file in folder.iterdir():
            if file.is_file():
                extension = file.suffix.lower()
                extensions.add(extension)

    for folder in folders:
        for extension in extensions:
            target_folder = folder / extension[1:]
            if not target_folder.exists():
                target_folder.mkdir()

    for folder in folders:
        target_folder = folder / "sem_extensao"
        if not target_folder.exists():
            target_folder.mkdir()


def organize_files(folders):
    create_folders_for_extensions(folders)

    for folder in folders:
        for file in folder.iterdir():
            if file.is_file():
                extension = file.suffix.lower()
                if extension:
                    target_folder = folder / extension[1:]
                else:
                    target_folder = folder / "sem_extensao"
                target_file = target_folder / file.name
                shutil.move(str(file), str(target_file))


def watch_folders(folders):
    event_handler = FileSystemEventHandler()
    event_handler.on_created = lambda event: on_created(event, folders)

    observer = Observer()
    for folder in folders:
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
        description="Monitora e organiza arquivos em uma pasta baseando-se em suas extensões."
    )
    parser.add_argument(
        "--folders",
        nargs="*",
        default=[Path(os.getcwd())],
        help="Pastas para monitorar",
    )

    args = parser.parse_args()

    folders = [Path(folder) for folder in args.folders]

    organize_files(folders)
    watch_folders(folders)
