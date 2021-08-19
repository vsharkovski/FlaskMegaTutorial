from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


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
    return render_template("index.html", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # POST, form was submitted and correctly validated
        flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
        return redirect(url_for("index"))
    return render_template("login.html", form=form)
