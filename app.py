import os
from pathlib import Path

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import tempfile
import mammoth

docx_path = Path("/Volumes/stuff/graphRagSandbox/assets/SmartBear_TOU-10FEB2023.docx")
non_logging_output_dir_path = Path("/Volumes/stuff/graphRagSandbox/static")

out_temp_file = tempfile.NamedTemporaryFile(prefix="SmartBear_",
                                            suffix=".html",
                                            delete=False,
                                            dir=non_logging_output_dir_path)


with open(docx_path, "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value
    with open(out_temp_file.name, "wb") as out_file:
        print(html.encode("ascii", errors="ignore"))
        out_file.write(html.encode("ascii", "ignore"))


UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(f"static/{uploaded_file.filename}")
    return render_template("root_frame.html",
                           static_file_name=f"{Path(out_temp_file.name).name}",
                           dynamic_header=f"{uploaded_file.filename}")


@app.route("/")
def index():
    return render_template("root_frame.html",
                           static_file_name="blank.html",
                           dynamic_header="DYNAMIC_HEADER_VALUE")
