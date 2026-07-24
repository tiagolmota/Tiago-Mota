# Python Patterns

## Project Style
- Type hints everywhere: `def fn(x: str) -> list[int]:`
- Dataclasses or Pydantic for data structures
- `pathlib.Path` over `os.path`
- f-strings over `.format()` or `%`
- Context managers (`with`) for file I/O, DB connections

## Common Patterns
```python
# Read CSV
import csv
with open("file.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

# JSON roundtrip
import json
data = json.loads(text)
out = json.dumps(data, ensure_ascii=False, indent=2)

# Path handling
from pathlib import Path
p = Path("graphify-out/obsidian")
p.mkdir(parents=True, exist_ok=True)
(p / "file.md").write_text(content, encoding="utf-8")

# Regex
import re
matches = re.findall(r'\*\*(.*?)\*\*', text)
```

## Data Science (when needed)
- `pandas` for tabular data
- `matplotlib`/`seaborn` for charts
- `scikit-learn` for ML
- `numpy` for arrays

## Security (scripting context)
- Never `eval()` or `exec()` with user input
- Use `subprocess.run([...], shell=False)` — never `shell=True` with user data
- Secrets via `os.environ` or `.env` + `python-dotenv`, never hardcoded
