# Single source of truth: reads crystals.json (hand-edited), then writes
# data.json (what the lookup page and chart load, with the derived cleaning and
# cleanse text filled in) and review.html (Kristen's fact-check sheet).
# Run after any edit to crystals.json: python3 build.py
import json, html
data = json.load(open("crystals.json"))["crystals"]
def cleaning(c):
    # Physical cleaning comes first. Toothbrush only for stones hard enough not
    # to scratch; delicate stones get a cloth or soft makeup brush.
    h = c["hardness"].split("-")[0]
    soft = c["fragility"] == "delicate" or not h.replace(".", "").isdigit() or float(h) < 5
    if soft:
        tool = "Dust it with a soft, dry cloth or a soft makeup brush (no toothbrush; it can scratch)."
    else:
        tool = "Wipe it with a soft cloth, or use a soft toothbrush for crevices."
    if c["water"] == "rinse":
        return tool + " If it gets dusty, a quick rinse under cool water is fine; dry it right away."
    return tool + " Keep it dry."

CLEANSE_ALL = ["Sound (singing bowl, bell, chime)", "Smoke (sage, palo santo, incense)", "Intention (hold it, breathe slowly, picture it clearing)"]

def cleanse(c):
    # Moonlight is for charging, not cleansing (Kristen). Water is never a cleanse.
    return ([] if c.get("noSelenitePlate") else ["Selenite plate (several hours or overnight)"]) + CLEANSE_ALL

WATER = {"rinse": "💧 Quick rinse OK", "dry": "🚫 Keep dry"}
SUN = {"safe": "Sun-safe", "fades": "☀️ Can fade in sun"}
FRAG = {"sturdy": "Sturdy", "careful": "🤲 Handle with care", "delicate": "⚠️ Delicate"}
rows = []
for c in sorted(data, key=lambda c: (c["water"] != "rinse", c["name"])):
    rows.append("<tr><td><b>{}</b><div class=al>{}</div></td><td>{}<div class=al>{}</div></td><td>{}</td><td>{}<div class=al>Mohs {}</div></td><td>{}{}</td><td>{}</td><td>{}</td></tr>".format(
        html.escape(c["name"]), html.escape(", ".join(c["aliases"])),
        WATER[c["water"]], html.escape(cleaning(c)), SUN[c["sun"]], FRAG[c["fragility"]], c["hardness"],
        html.escape(c["note"]),
        "<div class=warn>⚠️ " + html.escape(c["warn"]) + "</div>" if c.get("warn") else "",
        "<br>".join(cleanse(c)),
        ("collections/" + c["shop"]) if c["shop"] else "<span class=al>store search</span>"))
page = """<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Crystal Care Review</title><style>
:root{--bg:#faf7f2;--fg:#1c1c1c;--soft:#6b6460;--line:#e4ddd5;--warn:#9b2c2c}
@media (prefers-color-scheme:dark){:root{--bg:#161412;--fg:#eee8e2;--soft:#a39b94;--line:#3a342f;--warn:#f0a0a0}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,sans-serif;padding:24px 16px}
h1{font-size:22px;margin:0 0 6px}p{color:var(--soft);max-width:70ch}
.wrap{overflow-x:auto}table{border-collapse:collapse;min-width:1000px}
th,td{border-bottom:1px solid var(--line);padding:10px 8px;text-align:left;vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--soft);position:sticky;top:0;background:var(--bg)}
.al{color:var(--soft);font-size:12px}.warn{color:var(--warn);margin-top:6px}
</style></head><body><h1>Crystal Care Lookup: review sheet</h1>
<p>Every entry for the care tool, quartz-family stones first. Check each row; anything you'd change, tell me the crystal and what to fix. Cleaning (cloth, brush, quick rinse where safe) is listed first. Water is only ever for cleaning off dust, never for cleansing. When in doubt, entries err on the side of caution.</p>
<div class=wrap><table><tr><th>Crystal</th><th>Cleaning</th><th>Sun</th><th>Handling</th><th>Care note</th><th>Cleanse with</th><th>Shop link</th></tr>
""" + "\n".join(rows) + "</table></div><p><b>Good crystal habits</b> (shown on every crystal): Crystals aren't for chewing. Keep them out of your mouth, keep them away from pets and little ones who might chew them, and wash your hands after handling raw pieces.</p><p>{} crystals.</p></body></html>".format(len(data))
open("review.html", "w").write(page)

out = []
for c in sorted(data, key=lambda c: c["name"]):
    item = {k: v for k, v in c.items() if k != "noSelenitePlate"}
    item["cleaning"] = cleaning(c)
    item["cleanse"] = cleanse(c)
    out.append(item)
json.dump({"crystals": out}, open("data.json", "w"), ensure_ascii=False, indent=1)
print(len(data), "crystals")
