from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Vlatko"}
    posts = [
        {
            "author": {"username": "John"},
            "body": "I am a Dog of War."
        },
        {
            "author": {"username": "Yalda"},
            "body": "I am a Sick Dog. They made me into the Devouring Song."
        }
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)