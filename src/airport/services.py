import os
import uuid

from django.template.loader import render_to_string
from playwright.sync_api import sync_playwright


def generate_and_send_pdf(user, context: dict, template_name: str) -> str:
    html_string = render_to_string(template_name, context)

    static_root = os.path.abspath("static")
    static_url = f"file:///{static_root.replace(os.sep, '/')}"

    html_string = html_string.replace('href="/static/', f'href="{static_url}/')
    html_string = html_string.replace('src="/static/', f'src="{static_url}/')

    os.makedirs("tmp", exist_ok=True)
    html_path = os.path.join("tmp", f"{uuid.uuid4().hex}.html")
    pdf_path = os.path.join("tmp", f"{uuid.uuid4().hex}.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_string)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_path)}", wait_until="networkidle")
        page.pdf(path=pdf_path, format="A4", print_background=True)
        browser.close()

    os.remove(html_path)

    return pdf_path
