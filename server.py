from flask import Flask, render_template
from flask_frozen import Freezer


app = Flask(__name__)
freezer = Freezer(app=app)


@app.route("/")
def index():
    swiper1_data = [
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 1",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 2",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 3",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 4",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 5",
        },
        {
            "image": "https://img.youtube.com/vi/ohymkBe4zhg/maxresdefault.jpg",
            "title": "Slide 6",
        },
    ]
    return render_template("index.html", swiper1_data=swiper1_data)


if __name__ == "__main__":
    app.config["FREEZER_BASE_URL"] = "https://tonikcreates.vercel.app/"
    freezer.init_app(app)
    freezer.freeze()
