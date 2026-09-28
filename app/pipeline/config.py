"""Load explicit local website settings before the server and worker start."""
import os
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parents[2] / '.env'
LOCAL_SETTINGS = {'SHOWME_SERVE_RESEARCH_MEDIA', 'SHOWME_VIDEO_PIPELINE'}


def load_local_settings(path=None):
    path = Path(path or ENV_FILE)
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        name, separator, value = line.partition('=')
        name = name.strip()
        if separator and name in LOCAL_SETTINGS:
            os.environ.setdefault(name, value.strip().strip('\"').strip("'"))
