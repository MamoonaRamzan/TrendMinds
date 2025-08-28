from jinja2 import Template
from pathlib import Path

BASE_TEMPLATE = """# {{title}}
*{{subtitle}}*  
**Author:** {{author}} | **Week of:** {{week}}

---

## TL;DR
{{tldr}}

---

## Top {{top_n}} Stories
{% for s in stories %}
### {{loop.index}}) {{s.title}}
{{s.summary}}

**Why it matters:** {{s.why}}  
**Source:** {{s.url}}

---
{% endfor %}

## Quick Bites
{{quick_bites}}

## Further Reading
{% for fr in further %}
- [{{fr.title}}]({{fr.url}}) — {{fr.note}}
{% endfor %}

---

*Generated with LangChain RAG + Groq.*
"""

def render_newsletter(payload: dict) -> str:
    t = Template(BASE_TEMPLATE)
    return t.render(**payload)

def save_outputs(markdown_text: str, out_dir: str, file_md: str, file_html: str):
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Save markdown
    md_path = Path(out_dir) / file_md
    md_path.write_text(markdown_text, encoding="utf-8")

    # Convert markdown → simple HTML (lightweight)
    html_body = markdown_text.replace("\n", "<br>")
    html_template = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Newsletter</title>
  </head>
  <body style="font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; 
               max-width: 820px; margin: auto; padding: 32px; line-height:1.5">
    {body}
  </body>
</html>
"""
    html = html_template.format(body=html_body)

    # Save HTML
    html_path = Path(out_dir) / file_html
    html_path.write_text(html, encoding="utf-8")

    return str(md_path), str(html_path)
