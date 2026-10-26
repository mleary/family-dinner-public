"""Generate one Quarto page per dinner from content/dinners/*/dinner.json.

Runs as Quarto's pre-render step. Input is what the private repo will sync:
content/dinners/<folder>/dinner.json plus menu.png. Output goes to
dinners/<folder>/ (generated, not committed).
"""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "dinners"
OUT = ROOT / "dinners"


def yaml_str(s):
    return json.dumps(s or "", ensure_ascii=False)


def credit(src):
    if not src or not src.get("book"):
        return ""
    parts = [f"from <em>{escape(src['book'])}</em>"]
    if src.get("author"):
        parts.append(f"by {escape(src['author'])}")
    line = " ".join(parts)
    if src.get("page"):
        line += f", p. {src['page']}"
    return line


def band(d):
    st = d.get("style") or {}
    when = date.fromisoformat(d["date"]).strftime("%A, %B %-d, %Y")
    style = (
        f"--band-bg:{st.get('bg', '#1E242B')};"
        f"--band-ink:{st.get('ink', '#FFFFFF')};"
        f"--band-accent:{st.get('accent', '#C9A24A')};"
        f"--band-font:'{st.get('display_font', 'Fraunces')}';"
    )
    theme = f'<p class="band-theme">{escape(d["theme"])}</p>' if d.get("theme") else ""
    return f"""```{{=html}}
<section class="dinner-band" style="{style}">
  <div>
    <p class="band-date">{when}</p>
    <h1>{escape(d['title'])}</h1>
    {theme}
    <p class="band-summary">{escape(d.get('summary') or '')}</p>
  </div>
  <a href="menu.png"><img src="menu.png" alt="Menu card for {escape(d['title'])}"></a>
</section>
```
"""


def courses(d):
    out = ['```{=html}', '<div class="courses">']
    for c in d.get("courses", []):
        cr = credit(c.get("source"))
        if cr and c.get("adaptations"):
            cr += " (adapted)"
        out.append('<div class="course">')
        out.append(f'<div class="course-label">{escape(c.get("label") or "")}</div>')
        out.append(f'<h3>{escape(c["dish"])}</h3>')
        if cr:
            out.append(f'<p class="credit">{cr}</p>')
        if c.get("notes"):
            out.append(f'<p class="course-notes">{escape(c["notes"])}</p>')
        if c.get("adaptations"):
            out.append("<ul>" + "".join(f"<li>{escape(a)}</li>" for a in c["adaptations"]) + "</ul>")
        out.append("</div>")
    out += ["</div>", "```"]
    return "\n".join(out)


def page(d, folder):
    st = d.get("style") or {}
    font = st.get("display_font")
    header = ""
    if font:
        fam = font.replace(" ", "+")
        header = (
            "include-in-header:\n"
            "  - text: |\n"
            f'      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fam}&display=swap">\n'
        )
    cats = d.get("tags") or []
    front = (
        "---\n"
        f"title: {yaml_str(d['title'])}\n"
        f"date: {d['date']}\n"
        f"dinner-weekday: {yaml_str(date.fromisoformat(d['date']).strftime('%A'))}\n"
        f"dinner-day: {yaml_str(date.fromisoformat(d['date']).strftime('%B %-d, %Y'))}\n"
        f"description: {yaml_str(d.get('summary'))}\n"
        "image: menu.png\n"
        f"categories: {json.dumps(cats, ensure_ascii=False)}\n"
        "title-block-style: none\n"
        f"{header}"
        "---\n\n"
    )
    body = band(d) + "\n## Menu\n\n" + courses(d) + "\n"
    notes = folder / "public.md"
    if notes.exists():
        body += "\n## Notes\n\n" + notes.read_text() + "\n"
    if d.get("guests"):
        body += f"\n*Guests: {escape(str(d['guests']))}*\n"
    return front + body


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for folder in sorted(p for p in SRC.iterdir() if p.is_dir()):
        d = json.loads((folder / "dinner.json").read_text())
        dest = OUT / folder.name
        dest.mkdir(parents=True)
        (dest / "index.qmd").write_text(page(d, folder))
        for f in folder.iterdir():
            if f.name not in ("dinner.json", "public.md"):
                shutil.copy2(f, dest / f.name)


if __name__ == "__main__":
    main()
