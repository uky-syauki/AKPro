from flask import render_template, url_for, jsonify

from app import app
from app.models import Pertanyaan

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    data = Pertanyaan.query.all()
    return render_template("test.html", qs1=data[:10], qs2=data[10:20], qs3=data[20:])

