from flask import Flask, render_template, send_from_directory, redirect, url_for
from flask_frozen import Freezer
from shutil import copy
import yaml
import os


app = Flask(__name__)
freezer = Freezer(app=app)
src_config = os.path.join("static", "admin", "config.yml")
dest_config = os.path.join("build", "admin", "config.yml")


def load_data(filename):
    path = os.path.join("content", filename)
    with open(path, "r") as f:
        return yaml.safe_load(f)


@app.route("/")
def index():
    home = load_data("home.yml")
    get_started = load_data("get_started.yml")
    settings = load_data("settings.yml")
    faq = load_data("faq.yml")
    swiper1_data = [
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 1",
            "video_id": "ohymkBe4zhg",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 2",
            "video_id": "ohymkBe4zhg",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 3",
            "video_id": "ohymkBe4zhg",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 4",
            "video_id": "ohymkBe4zhg",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 5",
            "video_id": "ohymkBe4zhg",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 6",
            "video_id": "ohymkBe4zhg",
        },
    ]
    return render_template(
        "index.html",
        swiper1_data=swiper1_data,
        home=home,
        get_started=get_started,
        settings=settings,
        faq=faq,
    )


@app.route("/admin/")
@app.route("/admin/<path:path>")
def admin(path="index.html"):
    return send_from_directory("static/admin", path)


if __name__ == "__main__":
    app.config["FREEZER_BASE_URL"] = "https://tonikcreates.vercel.app/"
    freezer.init_app(app)
    freezer.freeze()
    copy(src_config, dest_config)
