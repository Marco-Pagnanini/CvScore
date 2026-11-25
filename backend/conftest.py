"""Makes `import app` work however pytest is launched (pytest, python -m pytest, from any folder, Docker or not)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
