import os
import subprocess
import sys
from tempfile import mkdtemp
from shutil import rmtree


class TestGenerateRadarChart:
    """Tests for the generate radar chart helper tool."""

    def test_generate_radar_chart(self):
        """Test the generate radar chart tool."""
        # WHEN we generate a radar chart
        # THEN a radar chart is generated
        for p in sys.path:
            print(p)
        out_dir = mkdtemp()
        out_path = os.path.join(out_dir, "./test.png")
        data = {"labels": ["A", "B", "C"], "data": {"A": 3, "B": 5, "C": 2}}
        subprocess.call([
            "tools/generate_radar_plot.py",
            "--data", str(data).replace("'", '"'),
            "--output", out_path
        ])
        assert os.path.exists(out_path)
        rmtree(out_dir)
