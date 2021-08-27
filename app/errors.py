from flask import render_template

from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template(
        "error.html",
        error_header="File not found",
        error_message=""
    ), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(
        "error.html",
        error_header="An unexpected error has occured",
        error_message="The administrator has been notified. Sorry for the inconvenience!"
    ), 500
