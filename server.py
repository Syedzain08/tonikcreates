from flask import Flask, render_template, send_from_directory, Response, url_for
from flask_frozen import Freezer
from shutil import copy
from dotenv import load_dotenv
from yaml import safe_load
from os import path, getenv


app = Flask(__name__)
freezer = Freezer(app=app)
src_config = path.join("static", "admin", "config.yml")
dest_config = path.join("build", "admin", "config.yml")


load_dotenv()
site_url = getenv("SITE_URL")


def load_data(filename):

    load_path = path.join("content", filename)
    with open(load_path, "r") as f:
        return safe_load(f)


@app.context_processor
def inject_settings():
    with open("content/settings.yml", "r") as f:
        settings = safe_load(f)

    with open("content/home.yml", "r") as f:
        home = safe_load(f)

    with open("content/seo.yml", "r") as f:
        seo = safe_load(f)

    return {
        "settings": settings,
        "hero": home.get("hero", {}),
        "seo": seo,
        "site_url": site_url,
    }


@app.route("/")
def index():
    home = load_data("home.yml")
    get_started = load_data("get_started.yml")
    settings = load_data("settings.yml")
    faq = load_data("faq.yml")
    portfolio = load_data("portfolio.yml")

    return render_template(
        "index.html",
        home=home,
        get_started=get_started,
        settings=settings,
        faq=faq,
        portfolio=portfolio,
    )


@app.route("/admin/")
@app.route("/admin/<path:path>")
def admin(path="index.html"):
    return send_from_directory("static/admin", path)


# -- Robots Route -- #
@app.route("/robots.txt")
def robots_txt():
    lines = [
        "User-agent: *",
        "Disallow:",
        f"Sitemap: {url_for('sitemap', _external=True)}",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


# --- Sitemap Route---- #
@app.route("/sitemap.xml")
def sitemap():
    urls = [
        {"loc": url_for("index", _external=True), "priority": "1.0"},
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{url['loc']}</loc>")
        xml.append(f"    <priority>{url['priority']}</priority>")
        xml.append("  </url>")
    xml.append("</urlset>")

    return Response("\n".join(xml), mimetype="text/xml")


if __name__ == "__main__":
    with open("static/admin/config.yml", "r") as f:
        config_content = f.read()

    import re

    config_content = re.sub(r"(site_url:\s*).*", f"\\1{site_url}", config_content)
    config_content = re.sub(r"(display_url:\s*).*", f"\\1{site_url}", config_content)
    config_content = re.sub(r"(base_url:\s*).*", f"\\1{site_url}", config_content)

    with open("static/admin/config.yml", "w") as f:
        f.write(config_content)

    app.config["FREEZER_BASE_URL"] = site_url
    freezer.init_app(app)
    freezer.freeze()
    copy(src_config, dest_config)
