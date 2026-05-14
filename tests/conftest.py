from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    # Legger prosjektroten på importstien slik at testene kan importere src-pakken.
    sys.path.insert(0, str(ROOT))
