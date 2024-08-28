from flask import Flask, request, redirect, url_for, send_from_directory, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("root_frame.html")
