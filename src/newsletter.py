import os
import ssl
import markdown
from jinja2 import Template
from pathlib import Path
import smtplib
from .subscription import get_subscribers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



BASE_TEMPLATE = """# 📰 {{title}}
*{{subtitle}}*  
**Author:** {{author}} | **Week of:** {{week}}

---

## ⚡ TL;DR
{{tldr}}

---

## 🌟 Top {{top_n}} Stories
{% for s in stories %}
### {{loop.index}}) {{s.title}}
{{s.summary}}

🔑 **Why it matters:** {{s.why}}  
🔗 **Source:** [Read more]({{s.url}})

---
{% endfor %}

## 🍪 Quick Bites
{{quick_bites}}

---

## 📚 Further Reading
{% if further and further[0].url %}
{% for fr in further %}
- [{{ fr.title }}]({{ fr.url }}) — {{ fr.note }}
{% endfor %}
{% else %}
- {{ further[0].title }}
{% endif %}

---
"""


def render_newsletter(payload: dict) -> str:
    """Render newsletter in Markdown using Jinja2."""
    t = Template(BASE_TEMPLATE)
    return t.render(**payload)

def save_outputs(markdown_text: str, out_dir: str, file_md: str, file_html: str):
    """Save newsletter as Markdown and styled HTML."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Save Markdown
    md_path = Path(out_dir) / file_md
    md_path.write_text(markdown_text, encoding="utf-8")

    # Convert Markdown → proper HTML
    html_body = markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code"])
    html_template = f"""<!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Newsletter</title>
      <style>
        body {{
          font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          max-width: 800px;
          margin: auto;
          padding: 40px;
          background-color: #f4f6f9;
          color: #333;
        }}
        h1 {{
          color: #2c3e50;
          border-bottom: 3px solid #1a73e8;
          padding-bottom: 8px;
        }}
        h2 {{
          color: #1a73e8;
          margin-top: 30px;
        }}
        h3 {{
          color: #444;
        }}
        a {{
          color: #1a73e8;
          font-weight: 500;
        }}
        a:hover {{
          text-decoration: underline;
        }}
        .card {{
          background: white;
          padding: 20px;
          margin: 20px 0;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .footer {{
          text-align: center;
          margin-top: 40px;
          font-size: 0.9rem;
          color: #666;
        }}
      </style>
    </head>
    <body>
      <div class="card">
        {html_body}
      </div>
      <div class="footer">
        ✨ Curated by <b>TrendMinds</b> | AI-powered insights for the curious mind ✨
      </div>
    </body>
    </html>
    """

    html_path = Path(out_dir) / file_html
    html_path.write_text(html_template, encoding="utf-8")

    return str(md_path), str(html_path)

def send_email(html_path: str, config: dict, niche: str):
    """Send newsletter email if enabled in config.yml (per-niche dynamic subscribers)."""
    email_cfg = config.get("email", {})
    if not email_cfg.get("enabled", False):
        print("📭 Email sending disabled in config.yml")
        return

    smtp_server = email_cfg.get("smtp_server", "smtp.gmail.com")
    smtp_port = email_cfg.get("smtp_port", 465)

    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    receivers = get_subscribers(niche)

    if not receivers:
        print(f"⚠️ No subscribers for {niche}, skipping email.")
        return

    html_content = Path(html_path).read_text(encoding="utf-8")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{niche} Weekly Insight"
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)
    msg.attach(MIMEText(html_content, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())

    print(f"✅ Sent {niche} newsletter to {len(receivers)} subscribers.")
