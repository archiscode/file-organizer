import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from organizer import category_for, organize, unique_destination  # noqa: E402


class OrganizerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def make(self, *names):
        for name in names:
            (self.folder / name).write_text("x")

    def test_category_for(self):
        self.assertEqual(category_for(Path("photo.JPG")), "Images")
        self.assertEqual(category_for(Path("report.pdf")), "Documents")
        self.assertEqual(category_for(Path("weird.xyz")), "Other")

    def test_files_are_moved(self):
        self.make("a.png", "b.pdf", "c.xyz")
        organize(self.folder)
        self.assertTrue((self.folder / "Images" / "a.png").exists())
        self.assertTrue((self.folder / "Documents" / "b.pdf").exists())
        self.assertTrue((self.folder / "Other" / "c.xyz").exists())

    def test_dry_run_changes_nothing(self):
        self.make("a.png")
        moves = organize(self.folder, dry_run=True)
        self.assertEqual(len(moves), 1)
        self.assertTrue((self.folder / "a.png").exists())
        self.assertFalse((self.folder / "Images").exists())

    def test_no_overwrite(self):
        self.make("a.png")
        (self.folder / "Images").mkdir()
        (self.folder / "Images" / "a.png").write_text("old")
        organize(self.folder)
        self.assertTrue((self.folder / "Images" / "a_1.png").exists())
        self.assertEqual((self.folder / "Images" / "a.png").read_text(), "old")

    def test_hidden_files_and_folders_ignored(self):
        self.make(".hidden.txt")
        (self.folder / "sub").mkdir()
        self.assertEqual(organize(self.folder), [])

    def test_unique_destination(self):
        self.make("a.txt")
        self.assertEqual(unique_destination(self.folder / "a.txt").name, "a_1.txt")

    def test_not_a_folder(self):
        with self.assertRaises(NotADirectoryError):
            organize(self.folder / "missing")


if __name__ == "__main__":
    unittest.main()
