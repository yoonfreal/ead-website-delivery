from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_site import validate_site

class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "style.css").write_text("body {}", encoding="utf-8")
    def tearDown(self):
        self.temp.cleanup()
    def page(self, html):
        (self.root / "index.html").write_text(html, encoding="utf-8")
    def test_valid_page(self):
        self.page('<title>Demo</title><h1>Demo</h1><link rel="stylesheet" href="style.css">')
        self.assertTrue(validate_site(self.root).startswith("PASS"))
    def test_missing_heading_is_rejected(self):
        self.page('<title>Demo</title><link rel="stylesheet" href="style.css">')
        with self.assertRaisesRegex(ValueError, "exactly one h1"):
            validate_site(self.root)
    def test_missing_asset_is_rejected(self):
        self.page('<title>Demo</title><h1>Demo</h1><link rel="stylesheet" href="missing.css">')
        with self.assertRaisesRegex(ValueError, "stylesheet"):
            validate_site(self.root)
    def test_empty_title_is_rejected(self):
        self.page('<title> </title><h1>Demo</h1><link rel="stylesheet" href="style.css">')
        with self.assertRaisesRegex(ValueError, "title"):
            validate_site(self.root)

if __name__ == "__main__":
    unittest.main()
