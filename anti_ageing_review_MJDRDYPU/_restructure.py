"""Move Tables 1-3 and figure legends to after the References section,
and strip embedded figure images from the manuscript body (figures go in a
separate file). Idempotent-ish: run once on the current _manuscript_R1.md."""
from pathlib import Path
import re

p = Path("_manuscript_R1.md")
t = p.read_text(encoding="utf-8")

# 1. Capture the display block (Table 1 ... Figure 4 legend) sitting in Results.
start = t.index("**Table 1. Intervention credibility ranking")
end_marker = "Marker size is proportional to the number of human studies."
end = t.index(end_marker) + len(end_marker)
block = t[start:end]

# Remove the block from the body (and tidy the surrounding blank lines).
body = (t[:start] + t[end:]).replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n")

# 2. From the captured block, separate the three tables (caption + grid) from
#    the figure legends, and drop the ![](...) image lines.
lines = block.splitlines()
tables_md, legends_md = [], []
i = 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("!["):            # image line -> drop (figures are a separate file)
        i += 1
        continue
    if ln.startswith("**Figure"):       # figure legend (single paragraph)
        legends_md.append(ln)
        i += 1
        continue
    # everything else (table captions + pipe tables + blanks) -> tables section
    tables_md.append(ln)
    i += 1

tables_section = "\n".join(l for l in tables_md).strip()
legends_section = "\n\n".join(legends_md).strip()

tail = (
    "\n\n# Tables\n\n"
    "*Tables are placed after the references for typesetting; each is cited at "
    "first mention in the text.*\n\n"
    + tables_section
    + "\n\n# Figure Legends\n\n"
    "*Figures are provided as a separate file (Figures 1–4). Legends are listed "
    "here and each figure is cited at first mention in the text.*\n\n"
    + legends_section
    + "\n"
)

body = body.rstrip() + tail
p.write_text(body, encoding="utf-8")
print("Restructured. Tables kept:", tables_section.count("| Rank") + tables_section.count("| Ref"),
      "| legends:", legends_section.count("**Figure"))
