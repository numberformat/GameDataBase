"""(c) 2025 Neeraj Verma — MIT License. https://noami.us"""

from pathlib import Path
import sys

base = Path("data/3nf")
systems = [p for p in base.iterdir() if p.is_dir()]

if not systems:
    print("No systems generated")
    sys.exit(1)

for s in systems:
    g = s / "games.csv"
    if not g.exists():
        print(f"Missing games.csv in {s.name}")
        sys.exit(1)

print("Quality checks passed")
