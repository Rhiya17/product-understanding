"""Run the three pre-declared controlled Higgsfield attempts sequentially."""

from pathlib import Path
import subprocess
import sys


RUNS = (
    ("corrected-preview-run-01", 41001),
    ("corrected-preview-run-02", 41002),
    ("corrected-preview-run-03", 41003),
)


def main() -> None:
    runner = Path(__file__).resolve().parent / "run_poc.py"
    for label, seed in RUNS:
        subprocess.run(
            [
                sys.executable,
                str(runner),
                "--run-label",
                label,
                "--seed",
                str(seed),
                "--model",
                "dop-preview",
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
