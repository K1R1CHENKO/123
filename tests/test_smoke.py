import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SmokeTests(unittest.TestCase):
    def test_script_mode_runs_and_exits(self):
        with tempfile.TemporaryDirectory() as td:
            save_root = Path(td) / "save"
            cmd = [
                sys.executable,
                "-m",
                "Game.main",
                "--script",
                "scripts/smoke_commands.txt",
                "--max-ticks",
                "20",
                "--save-root",
                str(save_root),
                "--seed",
                "123",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertIn("Script run finished by quit command.", result.stdout)
            self.assertTrue((save_root / "player.json").exists())

    def test_compile_imports(self):
        import Game.main  # noqa: F401


if __name__ == "__main__":
    unittest.main()
