import os
import ssl
import markdown
from jinja2 import Template
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



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
          font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
          max-width: 820px;
          margin: auto;
          padding: 32px;
          line-height: 1.6;
          background-color: #f9f9f9;
        }}
        h1, h2, h3 {{
          color: #333;
        }}
        a {{
          color: #1a73e8;
          text-decoration: none;
        }}
        a:hover {{
          text-decoration: underline;
        }}
      </style>
    </head>
    <body>
      {html_body}
    </body>
    </html>
    """

    html_path = Path(out_dir) / file_html
    html_path.write_text(html_template, encoding="utf-8")

    return str(md_path), str(html_path)

def send_email(html_path: str, config: dict):
    """Send newsletter email if enabled in config.yml (with secrets from env)."""
    email_cfg = config.get("email", {})
    if not email_cfg.get("enabled", False):
        print("📭 Email sending disabled in config.yml")
        return

    smtp_server = email_cfg.get("smtp_server", "smtp.gmail.com")
    smtp_port = email_cfg.get("smtp_port", 465)

    # 🔑 Read secrets from environment instead of config.yml
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    receivers = os.getenv("RECEIVER_EMAILS", "").split(",")

    if not sender or not password or not receivers:
        raise ValueError("❌ Missing email credentials in environment variables.")

    # Read the newsletter content
    html_content = Path(html_path).read_text(encoding="utf-8")

    # Build MIME email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = config.get("branding", {}).get("title", "Weekly Newsletter")
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)

    # Attach HTML version
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())

    print(f"✅ Newsletter sent to: {', '.join(receivers)}")
