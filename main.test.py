import unittest
from pathlib import Path
import shutil
import tempfile
import time
from watchdog.observers import Observer

from main import create_folders_for_extensions, organize_files, FileHandler


class TestOrganizeFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.source_dir = self.temp_dir / "source"
        self.target_dir = self.temp_dir / "target"

        self.source_dir.mkdir()
        self.target_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_create_folders_for_extensions(self):
        file1 = self.source_dir / "file1.txt"
        file2 = self.source_dir / "file2.jpg"
        file3 = self.source_dir / "file3.py"
        file4 = self.source_dir / "file4.docx"

        file1.touch()
        file2.touch()
        file3.touch()
        file4.touch()

        create_folders_for_extensions(self.target_dir)

        self.assertTrue((self.target_dir / "txt").is_dir())
        self.assertTrue((self.target_dir / "jpg").is_dir())
        self.assertTrue((self.target_dir / "py").is_dir())
        self.assertTrue((self.target_dir / "docx").is_dir())
        self.assertTrue((self.target_dir / "sem_extensao").is_dir())

    def test_organize_files(self):
        file1 = self.source_dir / "file1.txt"
        file2 = self.source_dir / "file2.jpg"
        file3 = self.source_dir / "file3.py"
        file4 = self.source_dir / "file4.docx"

        file1.touch()
        file2.touch()
        file3.touch()
        file4.touch()

        organize_files(self.source_dir)

        self.assertFalse(file1.exists())
        self.assertFalse(file2.exists())
        self.assertFalse(file3.exists())
        self.assertFalse(file4.exists())

        self.assertTrue((self.source_dir / "txt" / "file1.txt").exists())
        self.assertTrue((self.source_dir / "jpg" / "file2.jpg").exists())
        self.assertTrue((self.source_dir / "py" / "file3.py").exists())
        self.assertTrue((self.source_dir / "docx" / "file4.docx").exists())
        self.assertTrue((self.source_dir / "sem_extensao" / "file5").exists())

    def test_watch_folder(self):
        file1 = self.source_dir / "file1.txt"
        file2 = self.source_dir / "file2.jpg"

        file1.touch()
        file2.touch()

        event_handler = FileHandler(self.target_dir)
        observer = Observer()
        observer.schedule(event_handler, self.source_dir, recursive=True)
        observer.start()

        time.sleep(2)

        self.assertFalse(file1.exists())
        self.assertFalse(file2.exists())

        self.assertTrue((self.target_dir / "txt" / "file1.txt").exists())
        self.assertTrue((self.target_dir / "jpg" / "file2.jpg").exists())

        observer.stop()
        observer.join()


if __name__ == "__main__":
    unittest.main()
