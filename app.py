from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    render_template,
)
from werkzeug.utils import secure_filename
from pathlib import Path

import tempfile
import mammoth
import os


# So far testing of the webapp has been successful on both Unix (Mac) and Windows


# Cleanup file names to be more 'UNIX' like
def space_underscore_replace(s: str) -> str:
    return s.replace(" ", "_")


# Produce an html converted tempfile that returns just the root path name


def docx_to_html(i_file: Path, o_dir: Path) -> Path:
    style_map = """highlight => mark"""
    basename: str = i_file.stem
    o_tmp_file = Path(f"{o_dir}/{space_underscore_replace(basename)}.html")
    with open(i_file, "rb") as docx_file:
        o_html = mammoth.convert_to_html(docx_file, style_map=style_map).value
        with open(o_tmp_file, "wb") as html_file:
            # This was needed to clean up any unicode that was showing up inside docx e.g. euro signs
            html_file.write(o_html.encode("ascii", "ignore"))
    return Path(o_tmp_file)


def check_uploads_dir_contents(uploads_dir: str) -> bool:
    for f_name in os.listdir(f"{uploads_dir}"):
        if f_name.endswith(".html"):
            return True
        else:
            return False


def get_html_files_from_uploads(uploads_dir: str) -> Path | None:
    for f_name in os.listdir(f"{uploads_dir}"):
        if f_name.endswith(".html"):
            return Path(f"{Path(uploads_dir).name}/{f_name}")
        else:
            return None


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"doc", "docx"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename) -> bool:
    allowed_file_output = (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )
    return allowed_file_output


@app.route("/", methods=["POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["file"]

        if (
            uploaded_file.filename != "" and allowed_file(uploaded_file.filename)
        ) and not os.path.isfile(
            f"{UPLOAD_FOLDER}/{space_underscore_replace(uploaded_file.filename)}"
        ):
            uploaded_file.save(
                f"{UPLOAD_FOLDER}/{space_underscore_replace(uploaded_file.filename)}"
            )
            new_html_file = docx_to_html(
                i_file=Path(
                    f"{UPLOAD_FOLDER}/{space_underscore_replace(uploaded_file.filename)}"
                ),
                o_dir=Path(UPLOAD_FOLDER),
            )
            return render_template(
                "root_frame.html",
                static_file_name=f"uploads/{Path(new_html_file).name}",
                dynamic_header=f"{space_underscore_replace(uploaded_file.filename)}",
                n=10,
            )

        elif uploaded_file.filename == "" and check_uploads_dir_contents(UPLOAD_FOLDER):
            return render_template(
                "root_frame.html",
                static_file_name=f"{get_html_files_from_uploads(UPLOAD_FOLDER)}",
                dynamic_header=f"{Path(get_html_files_from_uploads(UPLOAD_FOLDER)).stem}.docx",
                n=10,
            )

        else:
            return render_template(
                "root_frame.html",
                static_file_name="blank.html",
                dynamic_header="",
                n=10,
            )


# Start page - iframe is 'empty'
@app.route("/", methods=["GET"])
def index():
    # data: int = 4
    # if request.values.get("phrase_count_v") is not None:
    #     data = int(request.values.get("phrase_count_v"))
    # print(data)
    return render_template(
        "root_frame.html",
        static_file_name="blank.html",
        dynamic_header="",
        n=10,
        # n=int(data),
    )


@app.route("/clear", methods=["POST"])
def clear_page():
    return None


# @app.route("/slider", methods=["POST", "GET"])
# def slider():
#
#     return render_template(
#         "root_frame.html",
#         static_file_name="blank.html",
#         dynamic_header="",
#         n=5,
#     )
