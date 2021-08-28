from datetime import datetime

from flask import (
    render_template, flash, redirect, url_for, jsonify, current_app, request 
)
from flask_login import current_user, login_required
from guess_language import guess_language

from app import db
from app.models import User, Post
from app.translate import translate

from app.main import bp
from app.main.forms import EditProfileForm, EmptyForm, PostForm


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == "UNKNOWN" or len(language) > 5:
            language = ""

        post = Post(
            body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for("main.index"))

    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config["POSTS_PER_PAGE"], False)
    prev_url = url_for("main.index", page=posts.prev_num) \
        if posts.has_prev else None
    next_url = url_for("main.index", page=posts.next_num) \
        if posts.has_next else None
    return render_template(
        "index.html",
        form=form,
        posts=posts.items,
        prev_url=prev_url,
        next_url=next_url
    )


@bp.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False)
    prev_url = url_for("main.explore", page=posts.prev_num) \
        if posts.has_prev else None
    next_url = url_for("main.explore", page=posts.next_num) \
        if posts.has_next else None
    return render_template(
        "index.html",
        title="Explore",
        posts=posts.items,
        prev_url=prev_url,
        next_url=next_url
    )


@bp.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config["POSTS_PER_PAGE"], False)
    prev_url = url_for("main.user", username=username, page=posts.prev_num) \
        if posts.has_prev else None
    next_url = url_for("main.user", username=username, page=posts.next_num) \
        if posts.has_next else None
    form = EmptyForm()
    return render_template(
        "user.html",
        user=user,
        form=form,
        posts=posts.items,
        prev_url=prev_url,
        next_url=next_url
    )


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    
    return render_template("edit_profile.html", form=form)


@bp.route("/follow/<username>", methods=["POST"])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} not found.")
            return redirect(url_for("main.index"))

        if user == current_user:
            flash("You cannot follow yourself.")
            return redirect(url_for("main.user", username=username))

        current_user.follow(user)
        db.session.commit()
        flash(f"You are now following {username}!")
        return redirect(url_for("main.user", username=username))
    else:
        # the CSRF token is missing or invalid
        return redirect(url_for("main.index"))


@bp.route("/unfollow/<username>", methods=["POST"])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} not found.")
            return redirect(url_for("main.index"))

        if user == current_user:
            flash("You cannot unfollow yourself.")
            return redirect(url_for("main.user", username=username))

        current_user.unfollow(user)
        db.session.commit()
        flash(f"You have stopped following {username}!")
        return redirect(url_for("main.user", username=username))
    else:
        # the CSRF token is missing or invalid
        return redirect(url_for("main.index"))


@bp.route("/translate", methods=["POST"])
@login_required
def translate_text():
    return jsonify({"text": translate(
        request.form["text"],
        request.form["source_language"],
        request.form["dest_language"]
    )})
