"""Build the Finance Cover Desk page from brain.json.

Edit brain.json (rhythm, deadlines, holidays), run this, then republish
dashboard.html to the same artifact URL.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
brain = json.loads((HERE / "brain.json").read_text())
payload = json.dumps(brain, ensure_ascii=False).replace("</", "<\\/")
template = (HERE / "dashboard.template.html").read_text()
assert "__BRAIN_JSON__" in template
(HERE / "dashboard.html").write_text(template.replace("__BRAIN_JSON__", payload))
print(f"Built dashboard.html: {len(brain['rhythm'])} rhythm items, {len(brain['deadlines'])} deadlines")
