import os
from pathlib import Path

PORT = int(os.getenv("PORT", 8050))
print(PORT)

CACHE_AGE = 60 * 60 * 24

PROJECT_DIR = Path(__file__).parent.resolve()
STATIC_DIR = PROJECT_DIR / "static"
print("PROJECT_DIR", PROJECT_DIR)
print("STATIC_DIR", STATIC_DIR)
